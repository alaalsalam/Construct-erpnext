from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe.utils import nowdate


class BacklogRequest(Document):
	def autoname(self):
		self.name = make_autoname("BLR-.YYYY.-.#####")

	def validate(self):
		self.waiting_since = self.waiting_since or nowdate()
