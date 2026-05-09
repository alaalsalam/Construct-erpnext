import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import add_months, flt, getdate


class RetentionRegister(Document):
	def validate(self):
		if not self.retained_on:
			self.retained_on = frappe.utils.today()
		if not self.defect_liability_months:
			self.defect_liability_months = 12
		if not self.release_due_date and self.retained_on:
			self.release_due_date = add_months(self.retained_on, self.defect_liability_months)
		self.remaining_retention_amount = flt(self.retention_amount) - flt(self.released_amount)
		if flt(self.released_amount) > flt(self.retention_amount):
			frappe.throw(_("Released Amount cannot exceed Retention Amount."))
		if flt(self.released_amount) and self.release_due_date and getdate() < getdate(self.release_due_date) and not self.remarks:
			frappe.throw(_("Remarks are required when releasing retention before Release Due Date."))
		if not self.status:
			self.status = "Held"
		if flt(self.remaining_retention_amount) <= 0 and self.status != "Cancelled":
			self.status = "Released"
		elif flt(self.released_amount) > 0 and self.status == "Held":
			self.status = "Partially Released"
