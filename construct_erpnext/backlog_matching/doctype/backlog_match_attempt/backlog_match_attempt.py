from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe.utils import now_datetime


class BacklogMatchAttempt(Document):
	def autoname(self):
		self.name = make_autoname("BMA-.YYYY.-.#####")

	def validate(self):
		self.attempt_date = self.attempt_date or now_datetime()
