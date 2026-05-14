from frappe.model.document import Document
from frappe.model.naming import make_autoname


class AutomationLog(Document):
	def autoname(self):
		self.name = make_autoname("AUTOLOG-.YYYY.-.#####")
