from frappe.model.document import Document
from frappe.model.naming import make_autoname


class ReminderSetting(Document):
	def autoname(self):
		self.name = make_autoname("REMSET-.YYYY.-.#####")
