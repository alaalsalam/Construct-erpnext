# SPDX-License-Identifier: MIT
# Collections synchronization for real estate Sales Contracts

import frappe
from frappe import _
from frappe.utils import add_days, flt, getdate, nowdate
from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry

from construct_erpnext.estate_sales.sales_invoice_utils import (
	recalculate_sales_contract_collection_status,
	sync_installments_from_sales_invoice,
)


def update_contract_from_payment_entry(payment_entry, method=None):
	"""Refresh Sales Contract collection status from Payment Entry references."""
	if isinstance(payment_entry, str):
		payment_entry = frappe.get_doc("Payment Entry", payment_entry)

	contracts = set()
	for reference in payment_entry.references:
		if reference.reference_doctype != "Sales Invoice" or not reference.reference_name:
			continue
		installments = frappe.get_all(
			"Sales Installment Schedule",
			filters={
				"parenttype": "Sales Contract",
				"sales_invoice": reference.reference_name,
			},
			fields=["name", "parent"],
		)
		if not installments:
			continue
		invoice = frappe.get_doc("Sales Invoice", reference.reference_name)
		sync_installments_from_sales_invoice(invoice)
		for row in installments:
			frappe.db.set_value(
				"Sales Installment Schedule",
				row.name,
				"payment_entry",
				payment_entry.name if payment_entry.docstatus == 1 else None,
				update_modified=False,
			)
			contracts.add(row.parent)

	for contract in contracts:
		recalculate_sales_contract_collection_status(contract)


@frappe.whitelist()
def refresh_contract_collection_status(sales_contract):
	"""Refresh collection totals for a Sales Contract."""
	recalculate_sales_contract_collection_status(sales_contract)
	return sales_contract


@frappe.whitelist()
def create_payment_entry_for_sales_invoice(
	sales_invoice_name,
	paid_amount=None,
	mode_of_payment=None,
	submit=False,
):
	"""Create one standard ERPNext Payment Entry for a submitted Sales Contract invoice."""
	invoice = frappe.get_doc("Sales Invoice", sales_invoice_name)
	if invoice.docstatus != 1:
		frappe.throw(_("Sales Invoice {0} must be submitted before creating Payment Entry.").format(invoice.name))
	if flt(invoice.outstanding_amount) <= 0:
		frappe.throw(_("Sales Invoice {0} has no outstanding amount.").format(invoice.name))

	installments = frappe.get_all(
		"Sales Installment Schedule",
		filters={"parenttype": "Sales Contract", "sales_invoice": invoice.name},
		fields=["name", "parent"],
	)
	if not installments:
		frappe.throw(_("Sales Invoice {0} is not linked to a Sales Contract installment.").format(invoice.name))

	collection_account = _get_default_collection_account(invoice.company)
	mode_of_payment = mode_of_payment or _get_or_create_default_collection_mode(
		invoice.company,
		collection_account,
	)
	allocated_amount = flt(paid_amount) if paid_amount is not None else flt(invoice.outstanding_amount)
	allocated_amount = min(allocated_amount, flt(invoice.outstanding_amount))
	if allocated_amount <= 0:
		frappe.throw(_("Payment amount must be greater than zero."))

	payment_entry = get_payment_entry(
		"Sales Invoice",
		invoice.name,
		bank_account=collection_account,
		reference_date=nowdate(),
	)
	payment_entry.mode_of_payment = mode_of_payment
	if payment_entry.meta.has_field("unit") and invoice.get("unit"):
		payment_entry.unit = invoice.get("unit")

	for reference in payment_entry.references:
		if reference.reference_doctype == "Sales Invoice" and reference.reference_name == invoice.name:
			reference.allocated_amount = allocated_amount

	payment_entry.paid_amount = allocated_amount
	payment_entry.received_amount = allocated_amount
	payment_entry.set_missing_values()
	payment_entry.set_amounts()
	payment_entry.insert(ignore_permissions=False)

	if submit:
		payment_entry.submit()
		update_contract_from_payment_entry(payment_entry)

	return payment_entry.name


@frappe.whitelist()
def mark_overdue_installments():
	"""Mark overdue installment rows. This is idempotent and creates no accounting documents."""
	settings = None
	try:
		settings = frappe.get_single("Sales Invoice Collection Settings")
	except Exception:
		pass

	grace_days = settings.overdue_grace_days if settings else 0
	today = getdate(nowdate())
	contracts = set()
	rows = frappe.get_all(
		"Sales Installment Schedule",
		filters={
			"parenttype": "Sales Contract",
			"installment_status": ["not in", ("Paid", "Waived", "Cancelled")],
		},
		fields=[
			"name",
			"parent",
			"due_date",
			"outstanding_amount",
			"amount",
			"invoice_status",
		],
	)

	for row in rows:
		if not row.due_date:
			continue
		overdue_days = (today - add_days(getdate(row.due_date), grace_days or 0)).days
		if overdue_days <= 0:
			continue
		outstanding = flt(row.outstanding_amount) if row.outstanding_amount is not None else flt(row.amount)
		if outstanding <= 0:
			continue
		values = {
			"installment_status": "Overdue",
			"invoice_status": "Overdue",
			"overdue_days": overdue_days,
		}
		for fieldname, value in values.items():
			if frappe.get_meta("Sales Installment Schedule").has_field(fieldname):
				frappe.db.set_value(
					"Sales Installment Schedule",
					row.name,
					fieldname,
					value,
					update_modified=False,
				)
		contracts.add(row.parent)

	for contract in contracts:
		recalculate_sales_contract_collection_status(contract)

	return {"updated_contracts": len(contracts)}


def get_contract_collection_summary(sales_contract):
	"""Return collection summary for a Sales Contract."""
	contract = frappe.get_doc("Sales Contract", sales_contract)
	return {
		"sales_contract": contract.name,
		"unit": contract.unit,
		"customer": contract.customer,
		"net_price": flt(contract.net_price),
		"total_invoiced_amount": flt(contract.total_invoiced_amount),
		"total_collected_amount": flt(contract.total_collected_amount),
		"total_outstanding_amount": flt(contract.total_outstanding_amount),
		"collection_status": contract.collection_status,
	}


def get_unit_revenue_summary(unit):
	"""Return revenue summary for a Unit based on Sales Contract collection fields."""
	rows = frappe.get_all(
		"Sales Contract",
		filters={"unit": unit, "docstatus": ["!=", 2]},
		fields=[
			"name",
			"customer",
			"net_price",
			"total_invoiced_amount",
			"total_collected_amount",
			"total_outstanding_amount",
			"collection_status",
		],
	)
	return {
		"unit": unit,
		"contract_count": len(rows),
		"net_price": sum(flt(row.net_price) for row in rows),
		"invoiced": sum(flt(row.total_invoiced_amount) for row in rows),
		"collected": sum(flt(row.total_collected_amount) for row in rows),
		"outstanding": sum(flt(row.total_outstanding_amount) for row in rows),
		"contracts": rows,
	}


def _get_default_collection_account(company):
	account = frappe.db.get_value(
		"Account",
		{"company": company, "account_type": "Cash", "is_group": 0},
		"name",
	)
	if account:
		return account

	account = frappe.db.get_value(
		"Account",
		{"company": company, "account_type": "Bank", "is_group": 0},
		"name",
	)
	if account:
		return account

	frappe.throw(_("No Cash or Bank account is available for company {0}.").format(company))


def _get_or_create_default_collection_mode(company, account):
	mode_name = "نقداً"
	if frappe.db.exists("Mode of Payment", mode_name):
		mode = frappe.get_doc("Mode of Payment", mode_name)
	else:
		mode = frappe.new_doc("Mode of Payment")
		mode.mode_of_payment = mode_name
		mode.type = "Cash"

	if not any(row.company == company and row.default_account == account for row in mode.accounts):
		mode.append("accounts", {"company": company, "default_account": account})

	if mode.is_new():
		mode.insert(ignore_permissions=True)
	else:
		mode.save(ignore_permissions=True)

	return mode.name
