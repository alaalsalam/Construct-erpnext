import frappe
from frappe import _
from frappe.model.document import Document


class RealEstateProject(Document):
	def validate(self):
		if not self.project:
			frappe.throw(_("Project is required."))
		existing = frappe.db.exists(
			"Real Estate Project",
			{"project": self.project, "name": ["!=", self.name]},
		)
		if existing:
			frappe.throw(_("A Real Estate Project already exists for this ERPNext Project."))
		if not self.company:
			self.company = frappe.db.get_value("Project", self.project, "company")
