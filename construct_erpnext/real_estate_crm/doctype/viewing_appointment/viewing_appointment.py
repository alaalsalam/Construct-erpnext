import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.naming import make_autoname


class ViewingAppointment(Document):
	def autoname(self):
		self.name = make_autoname("VA-.YYYY.-.#####")

	def validate(self):
		if self.requirement:
			requirement = frappe.get_doc("Customer Requirement", self.requirement)
			if self.customer and requirement.customer and self.customer != requirement.customer:
				frappe.throw(_("Customer must match the linked Customer Requirement."))
			if self.lead and requirement.lead and self.lead != requirement.lead:
				frappe.throw(_("Lead must match the linked Customer Requirement."))
