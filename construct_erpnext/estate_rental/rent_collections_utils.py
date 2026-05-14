# SPDX-License-Identifier: MIT
# Rent collection synchronization through standard ERPNext Payment Entry

import frappe
from frappe import _
from frappe.utils import flt, nowdate
from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry

from construct_erpnext.estate_rental.rent_invoice_utils import (
	recalculate_lease_collection_status,
	sync_rent_schedule_from_sales_invoice,
)


def update_lease_from_payment_entry(payment_entry, method=None):
	if isinstance(payment_entry, str):
		payment_entry = frappe.get_doc("Payment Entry", payment_entry)

	leases = set()
	for reference in payment_entry.references:
		if reference.reference_doctype != "Sales Invoice" or not reference.reference_name:
			continue
		rows = frappe.get_all(
			"Rent Schedule",
			filters={"parenttype": "Lease Contract", "sales_invoice": reference.reference_name},
			fields=["name", "parent"],
		)
		if not rows:
			continue
		invoice = frappe.get_doc("Sales Invoice", reference.reference_name)
		sync_rent_schedule_from_sales_invoice(invoice)
		for row in rows:
			frappe.db.set_value(
				"Rent Schedule",
				row.name,
				"payment_entry",
				payment_entry.name if payment_entry.docstatus == 1 else None,
				update_modified=False,
			)
			leases.add(row.parent)

	for lease in leases:
		if frappe.get_meta("Lease Contract").has_field("latest_payment_entry") and payment_entry.docstatus == 1:
			frappe.db.set_value(
				"Lease Contract",
				lease,
				"latest_payment_entry",
				payment_entry.name,
				update_modified=False,
			)
		recalculate_lease_collection_status(lease)


@frappe.whitelist()
def refresh_lease_collection_status(lease_contract):
	recalculate_lease_collection_status(lease_contract)
	return lease_contract


@frappe.whitelist()
def create_payment_entry_for_rent_invoice(
	sales_invoice_name,
	paid_amount=None,
	mode_of_payment=None,
	submit=False,
):
	invoice = frappe.get_doc("Sales Invoice", sales_invoice_name)
	if invoice.docstatus != 1:
		frappe.throw(_("Sales Invoice {0} must be submitted before creating Payment Entry.").format(invoice.name))
	if flt(invoice.outstanding_amount) <= 0:
		frappe.throw(_("Sales Invoice {0} has no outstanding amount.").format(invoice.name))

	rows = frappe.get_all(
		"Rent Schedule",
		filters={"parenttype": "Lease Contract", "sales_invoice": invoice.name},
		fields=["name", "parent"],
	)
	if not rows:
		frappe.throw(_("Sales Invoice {0} is not linked to a Rent Schedule row.").format(invoice.name))

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
		update_lease_from_payment_entry(payment_entry)

	return payment_entry.name


def get_tenant_collection_summary(lease_contract):
	lease = frappe.get_doc("Lease Contract", lease_contract)
	return {
		"lease_contract": lease.name,
		"unit": lease.unit,
		"customer": lease.customer,
		"total_scheduled_rent": flt(lease.total_scheduled_rent),
		"total_invoiced_rent": flt(lease.total_invoiced_rent),
		"total_collected_rent": flt(lease.total_collected_rent),
		"total_outstanding_rent": flt(lease.total_outstanding_rent),
		"rent_collection_status": lease.rent_collection_status,
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
