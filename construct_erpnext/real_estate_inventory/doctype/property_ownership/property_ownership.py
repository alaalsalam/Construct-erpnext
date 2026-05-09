import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt

from construct_erpnext.real_estate_inventory.inventory_utils import validate_ownership_percentages


class PropertyOwnership(Document):
	def validate(self):
		if not self.unit:
			frappe.throw(_("Unit is required."))
		if not self.property_owner:
			frappe.throw(_("Owner is required."))
		if flt(self.ownership_percentage) <= 0 or flt(self.ownership_percentage) > 100:
			frappe.throw(_("Ownership Percentage must be greater than 0 and up to 100."))
		if self.unit and not self.real_estate_project:
			self.real_estate_project = frappe.db.get_value("Unit", self.unit, "real_estate_project")
		validate_ownership_percentages(self.unit, self)

	def on_update(self):
		validate_ownership_percentages(self.unit, self)

	def on_trash(self):
		validate_ownership_percentages(self.unit)
