from frappe.model.document import Document
from frappe.utils import add_days, getdate, today


class GuaranteeRegister(Document):
	def validate(self):
		if not self.status:
			self.status = "Active"
		if not self.alert_before_days:
			self.alert_before_days = 60
		if self.status in ("Released", "Encashment Requested", "Encashment Completed", "Cancelled"):
			return
		if self.expiry_date:
			if getdate(self.expiry_date) < getdate(today()):
				self.status = "Expired"
			elif getdate(self.expiry_date) <= getdate(add_days(today(), self.alert_before_days)):
				self.status = "Expiring Soon"
