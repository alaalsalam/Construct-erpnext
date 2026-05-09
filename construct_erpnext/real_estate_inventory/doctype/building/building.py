import frappe
from frappe import _
from frappe.model.document import Document


class Building(Document):
	def validate(self):
		if not self.building_name:
			frappe.throw(_("Building Name is required."))
		if self.real_estate_project:
			self.project = frappe.db.get_value("Real Estate Project", self.real_estate_project, "project")
		existing = frappe.db.exists(
			"Building",
			{
				"real_estate_project": self.real_estate_project,
				"building_code": self.building_code,
				"name": ["!=", self.name],
			},
		)
		if existing:
			frappe.throw(_("Building Code must be unique per Real Estate Project."))
