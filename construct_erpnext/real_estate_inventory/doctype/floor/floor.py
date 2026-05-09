import frappe
from frappe import _
from frappe.model.document import Document


class Floor(Document):
	def validate(self):
		if not self.building:
			frappe.throw(_("Building is required."))
		if self.building:
			self.real_estate_project = frappe.db.get_value("Building", self.building, "real_estate_project")
		existing = frappe.db.exists(
			"Floor",
			{
				"building": self.building,
				"floor_code": self.floor_code,
				"name": ["!=", self.name],
			},
		)
		if existing:
			frappe.throw(_("Floor Code must be unique per Building."))
