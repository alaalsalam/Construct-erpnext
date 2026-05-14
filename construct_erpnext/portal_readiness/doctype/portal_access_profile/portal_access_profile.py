from frappe.model.document import Document
from frappe.model.naming import make_autoname


class PortalAccessProfile(Document):
	def autoname(self):
		self.name = make_autoname("PAP-.YYYY.-.#####")
