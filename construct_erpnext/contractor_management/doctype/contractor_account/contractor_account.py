import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class ContractorAccount(Document):
	def validate(self):
		if not self.project:
			frappe.throw(_("Project is required."))
		if not self.contractor:
			frappe.throw(_("Contractor is required."))
		if not self.status:
			self.status = "Active"
		if not self.account_name:
			self.account_name = self.get_account_name()
		self.validate_active_duplicate()
		for fieldname in (
			"current_advance_balance",
			"total_certified_amount",
			"total_retention_held",
			"total_retention_released",
			"total_advance_paid",
			"total_advance_recovered",
			"total_deductions",
			"total_invoiced_amount",
			"total_paid_amount",
			"outstanding_balance",
		):
			if flt(self.get(fieldname)) < 0 and fieldname != "outstanding_balance":
				frappe.throw(_("{0} cannot be negative.").format(self.meta.get_label(fieldname)))

	def get_account_name(self):
		project_name = frappe.db.get_value("Project", self.project, "project_name") or self.project
		contractor_name = (
			frappe.db.get_value("Supplier", self.contractor, "supplier_name")
			or self.contractor
		)
		return f"{contractor_name} - {project_name}"

	def validate_active_duplicate(self):
		if self.status != "Active":
			return
		filters = {
			"project": self.project,
			"contractor": self.contractor,
			"subcontract": self.subcontract or "",
			"status": "Active",
			"name": ["!=", self.name],
		}
		if frappe.db.exists("Contractor Account", filters):
			frappe.throw(_("An active Contractor Account already exists for this Project, Contractor, and Subcontract."))
