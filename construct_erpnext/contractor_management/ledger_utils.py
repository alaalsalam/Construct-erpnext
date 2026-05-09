import frappe
from frappe.utils import add_months, flt, getdate, today


def get_or_create_contractor_account(project, contractor, subcontract=None, company=None):
	filters = {
		"project": project,
		"contractor": contractor,
		"subcontract": subcontract or "",
		"status": "Active",
	}
	account = frappe.db.exists("Contractor Account", filters)
	if account:
		return account

	doc = frappe.get_doc(
		{
			"doctype": "Contractor Account",
			"company": company,
			"project": project,
			"contractor": contractor,
			"subcontract": subcontract,
			"status": "Active",
		}
	)
	doc.insert(ignore_permissions=True)
	return doc.name


def create_ledger_entry(
	contractor_account,
	transaction_type,
	reference_doctype,
	reference_name,
	posting_date=None,
	allow_reversal=False,
	**values,
):
	if not contractor_account or not reference_doctype or not reference_name or not transaction_type:
		return None

	existing = frappe.db.exists(
		"Contractor Ledger Entry",
		{
			"contractor_account": contractor_account,
			"transaction_type": transaction_type,
			"reference_doctype": reference_doctype,
			"reference_name": reference_name,
			"is_reversed": 1 if allow_reversal else 0,
		},
	)
	if existing:
		return existing

	account = frappe.get_doc("Contractor Account", contractor_account)
	doc = frappe.get_doc(
		{
			"doctype": "Contractor Ledger Entry",
			"company": values.get("company") or account.company,
			"project": values.get("project") or account.project,
			"contractor": values.get("contractor") or account.contractor,
			"contractor_account": contractor_account,
			"subcontract": values.get("subcontract") or account.subcontract,
			"posting_date": posting_date or values.get("posting_date") or today(),
			"transaction_type": transaction_type,
			"reference_doctype": reference_doctype,
			"reference_name": reference_name,
			"ipc": values.get("ipc"),
			"purchase_invoice": values.get("purchase_invoice"),
			"payment_entry": values.get("payment_entry"),
			"gross_amount": flt(values.get("gross_amount")),
			"retention_amount": flt(values.get("retention_amount")),
			"advance_amount": flt(values.get("advance_amount")),
			"recovered_amount": flt(values.get("recovered_amount")),
			"deduction_amount": flt(values.get("deduction_amount")),
			"invoice_amount": flt(values.get("invoice_amount")),
			"payment_amount": flt(values.get("payment_amount")),
			"outstanding_amount": flt(values.get("outstanding_amount")),
			"remarks": values.get("remarks"),
			"is_reversed": 1 if allow_reversal else 0,
			"reversed_entry": values.get("reversed_entry"),
		}
	)
	doc.insert(ignore_permissions=True)
	recalculate_contractor_account(contractor_account)
	return doc.name


def create_reversal_entry(entry_name, reference_doctype=None, reference_name=None):
	if not entry_name or frappe.db.get_value("Contractor Ledger Entry", entry_name, "is_reversed"):
		return None
	entry = frappe.get_doc("Contractor Ledger Entry", entry_name)
	reversal = create_ledger_entry(
		entry.contractor_account,
		entry.transaction_type,
		reference_doctype or entry.reference_doctype,
		reference_name or f"{entry.reference_name}-REV",
		allow_reversal=True,
		company=entry.company,
		project=entry.project,
		contractor=entry.contractor,
		subcontract=entry.subcontract,
		ipc=entry.ipc,
		purchase_invoice=entry.purchase_invoice,
		payment_entry=entry.payment_entry,
		gross_amount=-flt(entry.gross_amount),
		retention_amount=-flt(entry.retention_amount),
		advance_amount=-flt(entry.advance_amount),
		recovered_amount=-flt(entry.recovered_amount),
		deduction_amount=-flt(entry.deduction_amount),
		invoice_amount=-flt(entry.invoice_amount),
		payment_amount=-flt(entry.payment_amount),
		outstanding_amount=-flt(entry.outstanding_amount),
		remarks=f"Reversal of {entry.name}",
		reversed_entry=entry.name,
	)
	frappe.db.set_value("Contractor Ledger Entry", entry.name, "is_reversed", 1, update_modified=False)
	return reversal


def recalculate_contractor_account(contractor_account):
	if not contractor_account:
		return

	totals = frappe.db.sql(
		"""
		SELECT
			COALESCE(SUM(gross_amount), 0) AS total_certified_amount,
			COALESCE(SUM(retention_amount), 0) AS total_retention_held,
			COALESCE(SUM(advance_amount), 0) AS total_advance_paid,
			COALESCE(SUM(recovered_amount), 0) AS total_advance_recovered,
			COALESCE(SUM(deduction_amount), 0) AS total_deductions,
			COALESCE(SUM(invoice_amount), 0) AS total_invoiced_amount,
			COALESCE(SUM(payment_amount), 0) AS total_paid_amount,
			MAX(posting_date) AS last_transaction_date,
			MAX(ipc) AS last_ipc
		FROM `tabContractor Ledger Entry`
		WHERE contractor_account = %(contractor_account)s
		""",
		{"contractor_account": contractor_account},
		as_dict=True,
	)[0]

	retention_released = flt(
		frappe.db.sql(
			"""
			SELECT COALESCE(SUM(released_amount), 0)
			FROM `tabRetention Register`
			WHERE contractor_account = %s AND status != 'Cancelled'
			""",
			contractor_account,
		)[0][0]
	)
	outstanding_balance = (
		flt(totals.total_invoiced_amount)
		- flt(totals.total_paid_amount)
		- flt(totals.total_retention_held)
		+ retention_released
		- flt(totals.total_advance_recovered)
		- flt(totals.total_deductions)
	)
	current_advance_balance = flt(totals.total_advance_paid) - flt(totals.total_advance_recovered)

	frappe.db.set_value(
		"Contractor Account",
		contractor_account,
		{
			"current_advance_balance": current_advance_balance,
			"total_certified_amount": flt(totals.total_certified_amount),
			"total_retention_held": flt(totals.total_retention_held),
			"total_retention_released": retention_released,
			"total_advance_paid": flt(totals.total_advance_paid),
			"total_advance_recovered": flt(totals.total_advance_recovered),
			"total_deductions": flt(totals.total_deductions),
			"total_invoiced_amount": flt(totals.total_invoiced_amount),
			"total_paid_amount": flt(totals.total_paid_amount),
			"outstanding_balance": outstanding_balance,
			"last_transaction_date": totals.last_transaction_date,
			"last_ipc": totals.last_ipc,
		},
		update_modified=False,
	)
	recalculate_running_balance(contractor_account)


def recalculate_running_balance(contractor_account):
	running = 0
	entries = frappe.get_all(
		"Contractor Ledger Entry",
		filters={"contractor_account": contractor_account},
		fields=["name", "invoice_amount", "payment_amount", "outstanding_amount"],
		order_by="posting_date asc, creation asc",
	)
	for entry in entries:
		running += flt(entry.invoice_amount) - flt(entry.payment_amount)
		if flt(entry.outstanding_amount):
			running = flt(entry.outstanding_amount)
		frappe.db.set_value(
			"Contractor Ledger Entry",
			entry.name,
			"running_balance",
			running,
			update_modified=False,
		)


def create_retention_from_ipc(ipc):
	if not flt(ipc.retention_amount):
		return None
	if frappe.db.exists("Retention Register", {"ipc": ipc.name, "status": ["!=", "Cancelled"]}):
		return frappe.db.get_value("Retention Register", {"ipc": ipc.name, "status": ["!=", "Cancelled"]})

	account = ipc.contractor_account or get_or_create_contractor_account(
		ipc.project, ipc.contractor, ipc.subcontract, ipc.company
	)
	retained_on = ipc.period_end or today()
	doc = frappe.get_doc(
		{
			"doctype": "Retention Register",
			"company": ipc.company,
			"project": ipc.project,
			"contractor": ipc.contractor,
			"contractor_account": account,
			"ipc": ipc.name,
			"purchase_invoice": ipc.purchase_invoice,
			"retention_percent": ipc.retention_percent,
			"gross_amount": ipc.gross_amount,
			"retention_amount": ipc.retention_amount,
			"retained_on": retained_on,
			"release_due_date": add_months(retained_on, 12),
			"defect_liability_months": 12,
			"status": "Held",
		}
	)
	doc.insert(ignore_permissions=True)
	return doc.name


def recover_advance_from_ipc(ipc):
	if not flt(ipc.advance_recovery_amount):
		return
	account = ipc.contractor_account
	remaining = flt(ipc.advance_recovery_amount)
	advances = frappe.get_all(
		"Advance Register",
		filters={"contractor_account": account, "status": "Active"},
		fields=["name", "advance_amount", "recovered_amount"],
		order_by="advance_date asc, creation asc",
	)
	for advance in advances:
		if remaining <= 0:
			break
		unrecovered = flt(advance.advance_amount) - flt(advance.recovered_amount)
		recovered = min(unrecovered, remaining)
		frappe.db.set_value(
			"Advance Register",
			advance.name,
			"recovered_amount",
			flt(advance.recovered_amount) + recovered,
			update_modified=False,
		)
		doc = frappe.get_doc("Advance Register", advance.name)
		doc.save(ignore_permissions=True)
		remaining -= recovered


def update_ledger_from_ipc(ipc):
	account = ipc.contractor_account or get_or_create_contractor_account(
		ipc.project, ipc.contractor, ipc.subcontract, ipc.company
	)
	if not ipc.contractor_account:
		frappe.db.set_value("Interim Payment Certificate", ipc.name, "contractor_account", account, update_modified=False)
		ipc.contractor_account = account

	posting_date = ipc.period_end or today()
	create_ledger_entry(
		account,
		"IPC Certified",
		"Interim Payment Certificate",
		ipc.name,
		posting_date=posting_date,
		ipc=ipc.name,
		gross_amount=ipc.gross_amount,
		outstanding_amount=ipc.net_payable,
		remarks=ipc.remarks,
	)
	if flt(ipc.retention_amount):
		create_ledger_entry(
			account,
			"Retention Held",
			"Interim Payment Certificate",
			ipc.name,
			posting_date=posting_date,
			ipc=ipc.name,
			retention_amount=ipc.retention_amount,
			remarks="Retention held from IPC",
		)
		create_retention_from_ipc(ipc)
	if flt(ipc.advance_recovery_amount):
		create_ledger_entry(
			account,
			"Advance Recovery",
			"Interim Payment Certificate",
			ipc.name,
			posting_date=posting_date,
			ipc=ipc.name,
			recovered_amount=ipc.advance_recovery_amount,
			remarks="Advance recovered through IPC",
		)
		recover_advance_from_ipc(ipc)
	deductions = flt(ipc.penalty_amount) + flt(ipc.withholding_tax_amount) + flt(ipc.other_deduction_amount)
	if deductions:
		create_ledger_entry(
			account,
			"Deduction",
			"Interim Payment Certificate",
			ipc.name,
			posting_date=posting_date,
			ipc=ipc.name,
			deduction_amount=deductions,
			remarks="IPC deductions",
		)
	recalculate_contractor_account(account)
	return account


def update_ledger_from_purchase_invoice(pi):
	ipc_name = frappe.db.get_value("Interim Payment Certificate", {"purchase_invoice": pi.name}, "name")
	if not ipc_name:
		return
	ipc = frappe.get_doc("Interim Payment Certificate", ipc_name)
	account = ipc.contractor_account or update_ledger_from_ipc(ipc)
	create_ledger_entry(
		account,
		"Purchase Invoice Created",
		"Purchase Invoice",
		pi.name,
		posting_date=getattr(pi, "posting_date", None) or today(),
		ipc=ipc.name,
		purchase_invoice=pi.name,
		invoice_amount=flt(getattr(pi, "grand_total", 0)) or flt(ipc.net_payable),
		outstanding_amount=flt(ipc.outstanding_amount) or flt(ipc.net_payable),
		remarks="Purchase Invoice linked to IPC",
	)
	link_retention_to_purchase_invoice(ipc.name, pi.name)
	recalculate_contractor_account(account)


def update_ledger_from_payment_entry(pe):
	for ref in getattr(pe, "references", []) or []:
		if ref.reference_doctype != "Purchase Invoice":
			continue
		ipc_name = frappe.db.get_value(
			"Interim Payment Certificate", {"purchase_invoice": ref.reference_name}, "name"
		)
		if not ipc_name:
			continue
		ipc = frappe.get_doc("Interim Payment Certificate", ipc_name)
		account = ipc.contractor_account or update_ledger_from_ipc(ipc)
		paid_amount = flt(ref.allocated_amount)
		create_ledger_entry(
			account,
			"Payment Made",
			"Payment Entry",
			pe.name,
			posting_date=getattr(pe, "posting_date", None) or today(),
			ipc=ipc.name,
			purchase_invoice=ref.reference_name,
			payment_entry=pe.name,
			payment_amount=paid_amount,
			remarks="Payment Entry allocated to IPC Purchase Invoice",
		)
		update_ipc_payment_from_purchase_invoice(ipc)
		if flt(ipc.paid_amount) and flt(ipc.paid_amount) < flt(ipc.net_payable) and ipc.payment_difference_reason:
			create_ledger_entry(
				account,
				"Payment Difference",
				"Payment Entry",
				pe.name,
				posting_date=getattr(pe, "posting_date", None) or today(),
				ipc=ipc.name,
				purchase_invoice=ref.reference_name,
				payment_entry=pe.name,
				outstanding_amount=ipc.payment_difference_amount,
				remarks=ipc.payment_difference_reason,
			)
		recalculate_contractor_account(account)


def update_ipc_payment_from_purchase_invoice(ipc):
	if not ipc.purchase_invoice:
		return
	grand_total, outstanding_amount, docstatus = frappe.db.get_value(
		"Purchase Invoice", ipc.purchase_invoice, ["grand_total", "outstanding_amount", "docstatus"]
	)
	paid_amount = flt(grand_total) - flt(outstanding_amount)
	status = ipc.status
	if docstatus == 1:
		if paid_amount >= flt(ipc.net_payable):
			status = "Paid"
		elif paid_amount > 0:
			status = "Partially Paid"
		elif status == "Approved":
			status = "Invoice Created"
	frappe.db.set_value(
		"Interim Payment Certificate",
		ipc.name,
		{
			"paid_amount": paid_amount,
			"outstanding_amount": flt(outstanding_amount) if docstatus == 1 else flt(ipc.net_payable),
			"payment_difference_amount": flt(ipc.net_payable) - paid_amount,
			"status": status,
			"workflow_state": status,
		},
		update_modified=False,
	)
	ipc.reload()


def reverse_ledger_for_reference(reference_doctype, reference_name):
	entries = frappe.get_all(
		"Contractor Ledger Entry",
		filters={
			"reference_doctype": reference_doctype,
			"reference_name": reference_name,
			"is_reversed": 0,
		},
		pluck="name",
	)
	accounts = set()
	for entry in entries:
		accounts.add(frappe.db.get_value("Contractor Ledger Entry", entry, "contractor_account"))
		create_reversal_entry(entry, reference_doctype, f"{reference_name}-CANCEL")
	for account in accounts:
		recalculate_contractor_account(account)


def link_retention_to_purchase_invoice(ipc_name, purchase_invoice):
	retention = frappe.db.exists("Retention Register", {"ipc": ipc_name, "status": ["!=", "Cancelled"]})
	if retention:
		frappe.db.set_value(
			"Retention Register",
			retention,
			"purchase_invoice",
			purchase_invoice,
			update_modified=False,
		)


@frappe.whitelist()
def sync_ipc(ipc_name):
	"""Rebuild operational contractor controls for an existing IPC without changing GL."""
	ipc = frappe.get_doc("Interim Payment Certificate", ipc_name)
	account = update_ledger_from_ipc(ipc)
	if ipc.purchase_invoice:
		pi = frappe.get_doc("Purchase Invoice", ipc.purchase_invoice)
		update_ledger_from_purchase_invoice(pi)
	return account
