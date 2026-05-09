import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import get_datetime, now_datetime

from construct_erpnext.measurement_ipc.measurement_utils import (
	recalculate_measurement_book_totals,
)


class MeasurementBook(Document):
	def validate(self):
		self.validate_dates()
		self.sync_status_fields()
		self.set_people_and_dates()
		self.validate_locked_state()
		self.calculate_totals()

	def validate_dates(self):
		if (
			self.measurement_period_start
			and self.measurement_period_end
			and self.measurement_period_start > self.measurement_period_end
		):
			frappe.throw(_("Measurement Period Start cannot be after Measurement Period End."))

	def sync_status_fields(self):
		if not self.status and not self.workflow_state:
			self.status = "Draft"
			self.workflow_state = "Draft"
		elif self.workflow_state and self.workflow_state != self.status:
			self.status = self.workflow_state
		elif self.status and not self.workflow_state:
			self.workflow_state = self.status

	def set_people_and_dates(self):
		if not self.measured_by:
			self.measured_by = frappe.session.user
		if self.status in ("Submitted", "Under Verification", "Verified", "Locked") and not self.submitted_by:
			self.submitted_by = frappe.session.user
		if self.status in ("Verified", "Locked"):
			if not self.verified_by:
				self.verified_by = frappe.session.user
			if not self.verified_on:
				self.verified_on = now_datetime()
		if self.status == "Locked":
			if not self.locked_by:
				self.locked_by = frappe.session.user
			if not self.locked_on:
				self.locked_on = now_datetime()

	def validate_locked_state(self):
		if not self.name or self.is_new():
			return
		previous_status = frappe.db.get_value("Measurement Book", self.name, "status")
		if previous_status == "Locked" and "System Manager" not in frappe.get_roles():
			frappe.throw(_("Locked Measurement Books can only be changed by System Manager."))

	def calculate_totals(self):
		if self.is_new():
			self.total_entries = len(frappe.get_all("Measurement Entry", {"measurement_book": self.name}))
			return

		totals = frappe.db.sql(
			"""
			SELECT
				COUNT(name) AS total_entries,
				COALESCE(SUM(current_measured_qty), 0) AS total_current_measured_qty,
				COALESCE(SUM(accepted_qty), 0) AS total_accepted_qty,
				COALESCE(SUM(measured_amount), 0) AS total_measured_amount
			FROM `tabMeasurement Entry`
			WHERE measurement_book = %(measurement_book)s
				AND status != 'Cancelled'
			""",
			{"measurement_book": self.name},
			as_dict=True,
		)[0]
		self.total_entries = totals.total_entries
		self.total_current_measured_qty = totals.total_current_measured_qty
		self.total_accepted_qty = totals.total_accepted_qty
		self.total_measured_amount = totals.total_measured_amount

	def on_update(self):
		recalculate_measurement_book_totals(self.name)
