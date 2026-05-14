from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe.utils import nowdate


class RealEstateFollowUp(Document):
	def autoname(self):
		self.name = make_autoname("REFU-.YYYY.-.#####")

	def validate(self):
		self.follow_up_date = self.follow_up_date or nowdate()
