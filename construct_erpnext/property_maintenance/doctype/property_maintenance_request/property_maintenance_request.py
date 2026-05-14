from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe.utils import flt, nowdate


class PropertyMaintenanceRequest(Document):
	def autoname(self):
		self.name = make_autoname("PMR-.YYYY.-.#####")

	def validate(self):
		self.request_date = self.request_date or nowdate()
		if flt(self.estimated_cost) < 0:
			self.estimated_cost = 0
		if flt(self.actual_cost) < 0:
			self.actual_cost = 0
