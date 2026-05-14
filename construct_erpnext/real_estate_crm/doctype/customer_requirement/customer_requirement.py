import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe.utils import flt, nowdate


class CustomerRequirement(Document):
	def autoname(self):
		self.name = make_autoname("REQ-.YYYY.-.#####")

	def validate(self):
		self.requirement_date = self.requirement_date or nowdate()
		self.validate_ranges()

	def validate_ranges(self):
		if flt(self.preferred_area_min) and flt(self.preferred_area_max):
			if flt(self.preferred_area_max) < flt(self.preferred_area_min):
				frappe.throw(_("Preferred Area Max cannot be less than Preferred Area Min."))
		if flt(self.budget_min) and flt(self.budget_max):
			if flt(self.budget_max) < flt(self.budget_min):
				frappe.throw(_("Budget Max cannot be less than Budget Min."))
