import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt

from construct_erpnext.real_estate_inventory.inventory_utils import (
	sync_unit_status,
	update_related_counts,
)
from construct_erpnext.unit_costing.allocation_utils import get_profitability_status


class Unit(Document):
	def validate(self):
		self.fetch_project()
		self.validate_unique_unit_code()
		sync_unit_status(self)
		self.calculate_margin()

	def after_insert(self):
		update_related_counts(self.real_estate_project, self.building, self.floor)

	def on_update(self):
		update_related_counts(self.real_estate_project, self.building, self.floor)

	def on_trash(self):
		update_related_counts(self.real_estate_project, self.building, self.floor)

	def fetch_project(self):
		if self.real_estate_project:
			self.project = frappe.db.get_value("Real Estate Project", self.real_estate_project, "project")

	def validate_unique_unit_code(self):
		existing = frappe.db.exists(
			"Unit",
			{
				"building": self.building,
				"floor": self.floor,
				"unit_code": self.unit_code,
				"name": ["!=", self.name],
			},
		)
		if existing:
			frappe.throw(_("Unit Code must be unique per Building and Floor."))

	def calculate_margin(self):
		self.expected_margin = flt(self.expected_sale_price) - flt(self.allocated_cost)
		self.expected_margin_percent = (
			self.expected_margin / flt(self.expected_sale_price) * 100
			if flt(self.expected_sale_price)
			else 0
		)
		self.profitability_status = get_profitability_status(
			self.expected_sale_price, self.expected_margin_percent
		)
