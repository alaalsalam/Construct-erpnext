import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe.utils import flt, nowdate


class CommissionEntry(Document):
	def autoname(self):
		self.name = make_autoname("COM-.YYYY.-.#####")

	def validate(self):
		self.posting_date = self.posting_date or nowdate()
		self.validate_transaction_reference()
		self.validate_amounts()
		self.validate_duplicate()

	def validate_transaction_reference(self):
		if not (self.sales_contract or self.lease_contract or self.sales_invoice or self.payment_entry):
			frappe.throw(_("Commission Entry requires at least one source transaction reference."))

	def validate_amounts(self):
		if flt(self.commission_base_amount) < 0:
			frappe.throw(_("Commission Base Amount cannot be negative."))
		if flt(self.commission_percent) < 0:
			frappe.throw(_("Commission Percent cannot be negative."))
		if flt(self.fixed_amount) < 0:
			frappe.throw(_("Fixed Amount cannot be negative."))
		self.commission_amount = (flt(self.commission_base_amount) * flt(self.commission_percent) / 100) + flt(self.fixed_amount)
		if flt(self.commission_amount) < 0:
			frappe.throw(_("Commission Amount cannot be negative."))

	def validate_duplicate(self):
		filters = {
			"broker": self.broker,
			"commission_rule": self.commission_rule,
			"status": ["!=", "Cancelled"],
			"name": ["!=", self.name],
		}
		for fieldname in ("sales_contract", "lease_contract", "sales_invoice", "payment_entry"):
			if self.get(fieldname):
				filters[fieldname] = self.get(fieldname)
		if frappe.db.exists("Commission Entry", filters):
			frappe.throw(_("A Commission Entry already exists for this broker, rule, and transaction."))
