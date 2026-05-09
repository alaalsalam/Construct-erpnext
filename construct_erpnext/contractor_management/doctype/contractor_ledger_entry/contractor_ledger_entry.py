import frappe
from frappe import _
from frappe.model.document import Document


class ContractorLedgerEntry(Document):
	def validate(self):
		if not self.project:
			frappe.throw(_("Project is required."))
		if not self.contractor:
			frappe.throw(_("Contractor is required."))
		if not self.transaction_type:
			frappe.throw(_("Transaction Type is required."))
		if not self.posting_date:
			self.posting_date = frappe.utils.today()

	def before_save(self):
		if self.is_new():
			return
		if "System Manager" not in frappe.get_roles():
			frappe.throw(_("Contractor Ledger Entries are immutable. Create a reversal entry instead."))
