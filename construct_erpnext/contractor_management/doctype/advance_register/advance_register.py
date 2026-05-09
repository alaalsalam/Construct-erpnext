import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class AdvanceRegister(Document):
	def validate(self):
		self.outstanding_advance_amount = flt(self.advance_amount) - flt(self.recovered_amount)
		if flt(self.recovered_amount) > flt(self.advance_amount):
			frappe.throw(_("Recovered Amount cannot exceed Advance Amount."))
		if not self.status:
			self.status = "Active"
		if flt(self.outstanding_advance_amount) <= 0 and flt(self.advance_amount) > 0:
			self.status = "Fully Recovered"
