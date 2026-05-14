import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class CommissionRule(Document):
	def validate(self):
		if flt(self.commission_percent) < 0:
			frappe.throw(_("Commission Percent cannot be negative."))
		if flt(self.fixed_amount) < 0:
			frappe.throw(_("Fixed Amount cannot be negative."))
		if not flt(self.commission_percent) and not flt(self.fixed_amount):
			frappe.throw(_("Commission Rule requires either Commission Percent or Fixed Amount."))
