import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class ConstructionWorkItem(Document):
	def validate(self):
		self.validate_quantities()
		self.validate_unique_boq_row()
		self.calculate_tracking_values()

	def validate_quantities(self):
		if flt(self.planned_quantity) < 0:
			frappe.throw(_("Planned Quantity cannot be negative."))
		if flt(self.certified_qty) > flt(self.planned_quantity):
			frappe.throw(_("Certified Qty cannot exceed Planned Quantity."))

	def validate_unique_boq_row(self):
		if not self.construction_boq or not self.boq_item_row_id:
			return

		existing = frappe.db.exists(
			"Construction Work Item",
			{
				"construction_boq": self.construction_boq,
				"boq_item_row_id": self.boq_item_row_id,
				"name": ["!=", self.name],
			},
		)
		if existing:
			frappe.throw(
				_(
					"Construction Work Item already exists for this Construction BOQ item row."
				)
			)

	def calculate_tracking_values(self):
		self.remaining_qty = flt(self.planned_quantity) - flt(self.certified_qty)
		self.progress_percent = (
			flt(self.certified_qty) / flt(self.planned_quantity) * 100
			if flt(self.planned_quantity)
			else 0
		)
		self.variance_amount = flt(self.planned_amount) - flt(self.actual_cost)
		self.procurement_variance_qty = flt(self.planned_quantity) - flt(self.ordered_qty)
		self.procurement_variance_amount = flt(self.planned_amount) - flt(
			self.committed_amount
		)
		if not self.procurement_status:
			self.procurement_status = "Not Requested"
		if not self.measurement_status:
			self.measurement_status = "Not Measured"
		if not self.certification_status:
			self.certification_status = "Not Certified"
