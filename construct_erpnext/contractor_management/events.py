from construct_erpnext.contractor_management.ledger_utils import (
	reverse_ledger_for_reference,
	sync_ipc_payments_for_payment_entry,
	update_ledger_from_payment_entry,
	update_ledger_from_purchase_invoice,
)


def sync_purchase_invoice(doc, method=None):
	update_ledger_from_purchase_invoice(doc)


def reverse_purchase_invoice(doc, method=None):
	reverse_ledger_for_reference("Purchase Invoice", doc.name)


def sync_payment_entry(doc, method=None):
	update_ledger_from_payment_entry(doc)


def reverse_payment_entry(doc, method=None):
	reverse_ledger_for_reference("Payment Entry", doc.name)
	sync_ipc_payments_for_payment_entry(doc)
