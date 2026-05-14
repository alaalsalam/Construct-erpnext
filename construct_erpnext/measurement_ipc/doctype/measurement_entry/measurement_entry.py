import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, now_datetime, today

from construct_erpnext.measurement_ipc.measurement_utils import (
	get_previous_measured_qty,
	recalculate_measurement_book_totals,
	recalculate_work_item_measurement,
)


class MeasurementEntry(Document):
	def validate(self):
		self.validate_locked_state()
		self.validate_ipc_link()
		self.pull_work_item_details()
		self.calculate_quantities()
		self.validate_status()

	def validate_locked_state(self):
		if not self.name or self.is_new():
			return
		previous_status = frappe.db.get_value("Measurement Entry", self.name, "status")
		if previous_status == "Locked" and "System Manager" not in frappe.get_roles():
			frappe.throw(_("Locked Measurement Entries can only be changed by System Manager."))

	def validate_ipc_link(self):
		if not self.interim_payment_certificate:
			return
		ipc_status = frappe.db.get_value(
			"Interim Payment Certificate",
			self.interim_payment_certificate,
			["docstatus", "status"],
			as_dict=True,
		)
		if ipc_status and ipc_status.docstatus == 1 and "System Manager" not in frappe.get_roles():
			frappe.throw(_("Measurement Entries linked to submitted IPCs cannot be changed."))

	def pull_work_item_details(self):
		if not self.construction_work_item:
			return
		work_item = frappe.get_doc("Construction Work Item", self.construction_work_item)
		self.project = work_item.project
		self.construction_boq = work_item.construction_boq
		self.subcontract = work_item.subcontract or self.subcontract
		self.wbs_element = work_item.wbs_element
		self.cost_code = work_item.cost_code
		self.item_code = work_item.item_code
		if not self.description:
			self.description = work_item.description
		self.uom = work_item.uom
		self.planned_quantity = work_item.planned_quantity
		if not self.unit_rate:
			self.unit_rate = work_item.unit_rate
		self.previous_measured_qty = get_previous_measured_qty(
			self.construction_work_item, self.name
		)

		if self.measurement_book:
			book = frappe.get_doc("Measurement Book", self.measurement_book)
			self.company = book.company
			if not self.contractor:
				self.contractor = book.contractor
			if not self.subcontract:
				self.subcontract = book.subcontract

	def calculate_quantities(self):
		if not self.measurement_method:
			self.measurement_method = "Direct Quantity"
		if not self.number_of_units:
			self.number_of_units = 1

		if self.measurement_method == "Direct Quantity":
			self.calculated_qty = flt(self.current_measured_qty)
		elif self.measurement_method == "Length":
			self.calculated_qty = flt(self.length) * flt(self.number_of_units)
		elif self.measurement_method == "Area":
			self.calculated_qty = (
				flt(self.length) * flt(self.width) * flt(self.number_of_units)
			)
		elif self.measurement_method == "Volume":
			self.calculated_qty = (
				flt(self.length)
				* flt(self.width)
				* flt(self.height)
				* flt(self.number_of_units)
			)
		elif self.measurement_method == "Count":
			self.calculated_qty = flt(self.number_of_units)
		else:
			self.calculated_qty = flt(self.current_measured_qty)

		if not flt(self.current_measured_qty):
			self.current_measured_qty = self.calculated_qty
		if not flt(self.accepted_qty):
			self.accepted_qty = self.calculated_qty

		self.cumulative_measured_qty = flt(self.previous_measured_qty) + flt(
			self.accepted_qty
		)
		self.remaining_qty = flt(self.planned_quantity) - flt(self.cumulative_measured_qty)
		self.measured_amount = flt(self.accepted_qty) * flt(self.unit_rate)
		self.variance_qty = flt(self.cumulative_measured_qty) - flt(self.planned_quantity)
		self.variance_percent = (
			flt(self.variance_qty) / flt(self.planned_quantity) * 100
			if flt(self.planned_quantity)
			else 0
		)

	def validate_status(self):
		if flt(self.accepted_qty) < 0:
			frappe.throw(_("Accepted Qty cannot be negative."))
		if flt(self.cumulative_measured_qty) > flt(self.planned_quantity) and not self.variance_reason:
			frappe.throw(_("Variance Reason is required when measured quantity exceeds planned quantity."))
		if self.status == "Rejected" and not self.rejection_reason:
			frappe.throw(_("Rejection Reason is required for rejected Measurement Entries."))
		if self.status in ("Verified", "Locked"):
			if not self.verified_by:
				self.verified_by = frappe.session.user
			if not self.verified_on:
				self.verified_on = now_datetime()
		if not self.measurement_date:
			self.measurement_date = today()
		if not self.measured_by:
			self.measured_by = frappe.session.user
		if self.status in ("Submitted", "Verified", "Locked") and not self.submitted_by:
			self.submitted_by = frappe.session.user
		if not self.status:
			self.status = "Draft"

	def on_update(self):
		recalculate_work_item_measurement(self.construction_work_item)
		recalculate_measurement_book_totals(self.measurement_book)
		if self.subcontract:
			from construct_erpnext.contractor_management.agreement_utils import (
				update_agreement_from_measurement_entry,
			)

			update_agreement_from_measurement_entry(self)

	def on_trash(self):
		recalculate_work_item_measurement(self.construction_work_item)
		recalculate_measurement_book_totals(self.measurement_book)
