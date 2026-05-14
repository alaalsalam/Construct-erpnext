import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, getdate, now_datetime

from construct_erpnext.measurement_ipc.ipc import (
	CERTIFIED_IPC_STATUSES,
	get_previous_certified_qty,
	measurement_entry_has_active_ipc,
	recalculate_work_items_from_ipc,
)


class InterimPaymentCertificate(Document):
	def validate(self):
		self.validate_dates()
		self.sync_status_fields()
		self.set_audit_fields()
		self.calculate_lines()
		self.calculate_totals()
		self.validate_lines()
		self.validate_payment_difference()

	def validate_dates(self):
		if self.period_start and self.period_end and getdate(self.period_start) > getdate(self.period_end):
			frappe.throw(_("Period Start cannot be after Period End."))

	def sync_status_fields(self):
		if not self.status:
			self.status = self.workflow_state or "Draft"
		if not self.workflow_state:
			self.workflow_state = self.status
		if self.workflow_state != self.status:
			self.status = self.workflow_state

	def set_audit_fields(self):
		now = now_datetime()
		user = frappe.session.user
		if self.status in ("Submitted", "Under Review", "Certified", "Approved") and not self.submitted_by:
			self.submitted_by = user
			self.submitted_on = now
		if self.status in ("Under Review", "Certified", "Approved") and not self.reviewed_by:
			self.reviewed_by = user
			self.reviewed_on = now
		if self.status in ("Certified", "Approved") and not self.certified_by:
			self.certified_by = user
			self.certified_on = now
		if self.status == "Approved" and not self.approved_by:
			self.approved_by = user
			self.approved_on = now

	def calculate_lines(self):
		for line in self.lines:
			if line.measurement_entry:
				self.pull_measurement_line_details(line)
			if not flt(line.current_certified_qty):
				line.current_certified_qty = flt(line.current_measured_qty)
			if not flt(line.retention_percent):
				line.retention_percent = flt(self.retention_percent)

			line.previous_certified_qty = get_previous_certified_qty(
				line.construction_work_item, self.name
			)
			line.total_certified_qty = flt(line.previous_certified_qty) + flt(
				line.current_certified_qty
			)
			line.remaining_qty = flt(line.boq_qty) - flt(line.total_certified_qty)
			line.current_amount = flt(line.current_certified_qty) * flt(line.unit_rate)
			line.previous_certified_amount = flt(line.previous_certified_qty) * flt(
				line.unit_rate
			)
			line.total_certified_amount = flt(line.total_certified_qty) * flt(line.unit_rate)
			line.retention_amount = flt(line.current_amount) * flt(line.retention_percent) / 100
			line.net_line_amount = flt(line.current_amount) - flt(line.retention_amount)

	def pull_measurement_line_details(self, line):
		entry = frappe.get_doc("Measurement Entry", line.measurement_entry)
		work_item = frappe.get_doc("Construction Work Item", entry.construction_work_item)
		line.measurement_book = entry.measurement_book
		line.construction_work_item = work_item.name
		line.subcontract = entry.subcontract or work_item.subcontract or self.subcontract
		line.agreement_item_reference = work_item.agreement_item_reference
		line.construction_boq = work_item.construction_boq
		line.wbs_element = work_item.wbs_element
		line.cost_code = work_item.cost_code
		line.item_code = work_item.item_code
		line.description = entry.description or work_item.description
		line.uom = work_item.uom
		line.boq_qty = work_item.planned_quantity
		line.current_measured_qty = entry.accepted_qty
		if not flt(line.current_certified_qty):
			line.current_certified_qty = entry.accepted_qty
		if not flt(line.unit_rate):
			line.unit_rate = entry.unit_rate or work_item.unit_rate
		line.engineer_comment = entry.engineer_comment
		line.qs_comment = entry.qs_comment

	def calculate_totals(self):
		self.gross_amount = sum(flt(line.current_amount) for line in self.lines)
		self.previous_certified_amount = sum(
			flt(line.previous_certified_amount) for line in self.lines
		)
		self.current_certified_amount = self.gross_amount
		self.total_certified_amount = sum(
			flt(line.total_certified_amount) for line in self.lines
		)
		self.retention_amount = sum(flt(line.retention_amount) for line in self.lines)
		child_deductions = sum(flt(row.amount) for row in self.deductions)
		total_deductions = (
			flt(self.retention_amount)
			+ flt(self.advance_recovery_amount)
			+ flt(self.penalty_amount)
			+ flt(self.withholding_tax_amount)
			+ flt(self.other_deduction_amount)
			+ child_deductions
		)
		self.net_payable = flt(self.gross_amount) - total_deductions
		self.payment_difference_amount = flt(self.net_payable) - flt(self.paid_amount)
		if not self.subcontract:
			agreements = {line.subcontract for line in self.lines if line.subcontract}
			if len(agreements) == 1:
				self.subcontract = agreements.pop()

	def validate_lines(self):
		if self.status in ("Approved", "Invoice Created", "Partially Paid", "Paid", "Closed") and not self.lines:
			frappe.throw(_("Cannot approve IPC with no lines."))
		if self.status == "Rejected" and not self.rejection_reason:
			frappe.throw(_("Rejection Reason is required for rejected IPC."))

		seen_entries = set()
		for line in self.lines:
			if flt(line.current_certified_qty) < 0:
				frappe.throw(_("Row {0}: Current Certified Qty cannot be negative.").format(line.idx))
			if line.measurement_entry:
				if line.measurement_entry in seen_entries:
					frappe.throw(_("Measurement Entry {0} is repeated in this IPC.").format(line.measurement_entry))
				seen_entries.add(line.measurement_entry)
				entry_status, accepted_qty = frappe.db.get_value(
					"Measurement Entry", line.measurement_entry, ["status", "accepted_qty"]
				)
				if entry_status not in ("Verified", "Locked"):
					frappe.throw(_("Row {0}: Measurement Entry must be Verified or Locked.").format(line.idx))
				if measurement_entry_has_active_ipc(line.measurement_entry, self.name):
					frappe.throw(_("Measurement Entry {0} is already linked to an active IPC.").format(line.measurement_entry))
				if flt(line.current_certified_qty) > flt(accepted_qty) and not (line.variation_reference or line.remarks):
					frappe.throw(_("Row {0}: Remarks or Variation Reference is required when certified qty exceeds accepted measurement qty.").format(line.idx))
			if flt(line.total_certified_qty) > flt(line.boq_qty) and not (line.variation_reference or line.remarks):
				frappe.throw(_("Row {0}: Remarks or Variation Reference is required when certified qty exceeds BOQ qty.").format(line.idx))

	def validate_payment_difference(self):
		if self.status in ("Partially Paid", "Paid"):
			if flt(self.paid_amount) < flt(self.net_payable) and not self.payment_difference_reason:
				frappe.throw(_("Payment Difference Reason is required when paid amount is below net payable."))

	def on_submit(self):
		if self.status not in CERTIFIED_IPC_STATUSES:
			self.db_set("status", "Approved", update_modified=False)
			self.db_set("workflow_state", "Approved", update_modified=False)
		self.link_measurement_entries()
		recalculate_work_items_from_ipc(self)
		from construct_erpnext.contractor_management.ledger_utils import update_ledger_from_ipc

		update_ledger_from_ipc(self)
		from construct_erpnext.contractor_management.agreement_utils import update_agreement_from_ipc

		update_agreement_from_ipc(self)

	def on_cancel(self):
		if self.purchase_invoice and frappe.db.get_value("Purchase Invoice", self.purchase_invoice, "docstatus") == 1:
			frappe.throw(_("Cannot cancel IPC because linked Purchase Invoice is submitted."))
		self.release_measurement_entries()
		recalculate_work_items_from_ipc(self)
		from construct_erpnext.contractor_management.ledger_utils import reverse_ledger_for_reference

		reverse_ledger_for_reference("Interim Payment Certificate", self.name)
		from construct_erpnext.contractor_management.agreement_utils import update_agreement_from_ipc

		update_agreement_from_ipc(self)

	def link_measurement_entries(self):
		for line in self.lines:
			if line.measurement_entry:
				frappe.db.set_value(
					"Measurement Entry",
					line.measurement_entry,
					{
						"interim_payment_certificate": self.name,
						"ipc_line_reference": line.name,
					},
					update_modified=False,
				)

	def release_measurement_entries(self):
		for line in self.lines:
			if line.measurement_entry:
				frappe.db.set_value(
					"Measurement Entry",
					line.measurement_entry,
					{
						"interim_payment_certificate": None,
						"ipc_line_reference": None,
					},
					update_modified=False,
				)

	@frappe.whitelist()
	def create_purchase_invoice(self):
		if self.docstatus != 1 or self.status not in ("Approved", "Invoice Created"):
			frappe.throw(_("Purchase Invoice can only be created from an approved IPC."))
		if self.purchase_invoice:
			return self.purchase_invoice

		service_item = get_contractor_service_item()
		invoice = frappe.new_doc("Purchase Invoice")
		invoice.company = self.company
		invoice.supplier = self.contractor
		company_currency = frappe.db.get_value("Company", self.company, "default_currency")
		if company_currency:
			invoice.currency = company_currency
			invoice.conversion_rate = 1
		invoice.posting_date = getdate()
		invoice.bill_no = self.name
		invoice.bill_date = getdate()
		invoice.project = self.project
		invoice.remarks = _("مستخلص مقاول عن قياسات معتمدة لأعمال المشروع")
		service_uom = frappe.db.get_value("Item", service_item, "stock_uom")
		expense_account = get_default_expense_account(self.company)

		for line in self.lines:
			invoice.append(
				"items",
				{
					"item_code": service_item,
					"description": line.description or _("مستخلص مقاول عن قياسات معتمدة لأعمال المشروع"),
					"qty": line.current_certified_qty,
					"uom": service_uom,
					"rate": line.unit_rate,
					"amount": line.current_amount,
					"expense_account": expense_account,
					"project": self.project,
					"construction_work_item": line.construction_work_item,
					"construction_boq": line.construction_boq,
					"wbs_element": line.wbs_element,
					"cost_code": line.cost_code,
				},
			)

		invoice.insert(ignore_permissions=True)
		self.db_set("purchase_invoice", invoice.name)
		self.db_set("paid_amount", 0)
		self.db_set("outstanding_amount", self.net_payable)
		self.db_set("payment_difference_amount", self.net_payable)
		self.db_set("status", "Invoice Created")
		self.db_set("workflow_state", "Invoice Created")
		from construct_erpnext.contractor_management.ledger_utils import update_ledger_from_purchase_invoice

		update_ledger_from_purchase_invoice(invoice)
		return invoice.name

	@frappe.whitelist()
	def update_payment_status(self):
		if not self.purchase_invoice:
			return
		grand_total, outstanding_amount, docstatus = frappe.db.get_value(
			"Purchase Invoice",
			self.purchase_invoice,
			["grand_total", "outstanding_amount", "docstatus"],
		)
		paid_amount = flt(grand_total) - flt(outstanding_amount)
		self.paid_amount = paid_amount
		self.outstanding_amount = flt(outstanding_amount)
		self.payment_difference_amount = flt(self.net_payable) - paid_amount
		if docstatus == 1:
			if paid_amount >= flt(self.net_payable):
				self.status = "Paid"
				self.workflow_state = "Paid"
			elif paid_amount > 0:
				self.status = "Partially Paid"
				self.workflow_state = "Partially Paid"
			elif self.status == "Approved":
				self.status = "Invoice Created"
				self.workflow_state = "Invoice Created"


def get_contractor_service_item():
	for item_code in ("خدمة مقاول أعمال إنشائية", "Contractor Service"):
		if frappe.db.exists("Item", item_code):
			return item_code
	frappe.throw(_("Contractor service item is required to create Purchase Invoice."))


def get_default_expense_account(company):
	account = frappe.db.get_value(
		"Account",
		{"company": company, "root_type": "Expense", "is_group": 0},
		"name",
	)
	if not account:
		frappe.throw(_("Expense account is required to create Purchase Invoice."))
	return account
