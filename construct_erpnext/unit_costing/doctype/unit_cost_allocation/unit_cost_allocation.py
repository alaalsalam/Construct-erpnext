import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt

from construct_erpnext.unit_costing.allocation_utils import (
	apply_unit_allocation,
	calculate_unit_allocation,
	get_project_cost_source,
)


class UnitCostAllocation(Document):
	def validate(self):
		self.fetch_project()
		self.fetch_source_amount()
		if not self.allocation_status:
			self.allocation_status = "Draft"
		if self.allocation_status in ("Draft", "Calculated", "Reviewed", "Applied"):
			calculate_unit_allocation(self)
			self.calculate_totals()
			self.validate_totals()
		if self.allocation_status == "Draft" and self.lines:
			self.allocation_status = "Calculated"

	def on_update(self):
		if self.allocation_status == "Applied":
			apply_unit_allocation(self)

	def fetch_project(self):
		if not self.real_estate_project:
			frappe.throw(_("Real Estate Project is required."))
		project, company = frappe.db.get_value(
			"Real Estate Project", self.real_estate_project, ["project", "company"]
		)
		self.project = project
		if not self.company:
			self.company = company

	def fetch_source_amount(self):
		if self.cost_source != "Manual Amount" or not flt(self.source_amount):
			self.source_amount = get_project_cost_source(
				self.real_estate_project,
				self.cost_source,
				self.project_financial_snapshot,
				self.source_amount,
			)

	def calculate_totals(self):
		self.total_allocated_amount = sum(flt(row.allocated_amount) for row in self.lines)
		self.unallocated_amount = flt(self.source_amount) - flt(self.total_allocated_amount)

	def validate_totals(self):
		if self.allocation_status == "Applied" and flt(self.source_amount) <= 0:
			frappe.throw(_("Source Amount must be greater than zero before Applied."))
		if flt(self.total_allocated_amount) > flt(self.source_amount) + 0.01:
			frappe.throw(_("Total Allocated Amount cannot exceed Source Amount."))
