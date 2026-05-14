import frappe
from frappe import _
from frappe.utils import flt, getdate


def execute(filters=None):
	filters = frappe._dict(filters or {})
	data = get_data(filters)
	return get_columns(), data


def get_columns():
	return [
		{"fieldname": "posting_date", "fieldtype": "Date", "label": _("Date"), "width": 100},
		{"fieldname": "sales_contract", "fieldtype": "Link", "label": _("Sales Contract"), "options": "Sales Contract", "width": 150},
		{"fieldname": "unit", "fieldtype": "Link", "label": _("Unit"), "options": "Unit", "width": 140},
		{"fieldname": "invoice", "fieldtype": "Link", "label": _("Invoice"), "options": "Sales Invoice", "width": 150},
		{"fieldname": "installment", "fieldtype": "Data", "label": _("Installment"), "width": 120},
		{"fieldname": "debit", "fieldtype": "Currency", "label": _("Debit"), "width": 130},
		{"fieldname": "credit", "fieldtype": "Currency", "label": _("Credit"), "width": 130},
		{"fieldname": "outstanding", "fieldtype": "Currency", "label": _("Outstanding"), "width": 130},
		{"fieldname": "status", "fieldtype": "Data", "label": _("Status"), "width": 130},
		{"fieldname": "remarks", "fieldtype": "Data", "label": _("Remarks"), "width": 260},
	]


def get_data(filters):
	rows = []
	for contract in _get_contracts(filters):
		for installment in _get_installments(contract.name, filters):
			invoice_name = installment.get("sales_invoice")
			if not invoice_name:
				continue
			invoice = frappe.get_doc("Sales Invoice", invoice_name)
			if invoice.docstatus == 2:
				continue
			if filters.get("from_date") and getdate(invoice.posting_date) < getdate(filters.from_date):
				continue
			if filters.get("to_date") and getdate(invoice.posting_date) > getdate(filters.to_date):
				continue

			rows.append(
				{
					"posting_date": invoice.posting_date,
					"sales_contract": contract.name,
					"unit": contract.unit,
					"invoice": invoice.name,
					"installment": installment.get("installment_number") or installment.get("sequence"),
					"debit": flt(invoice.grand_total),
					"credit": 0,
					"outstanding": flt(invoice.outstanding_amount),
					"status": installment.get("invoice_status") or invoice.status,
					"remarks": _("Sales invoice for real estate unit installment"),
				}
			)
			rows.extend(_get_payment_rows(invoice, contract, installment))

	rows.sort(key=lambda row: (row.get("posting_date") or "", row.get("invoice") or "", row.get("credit") > 0))
	return rows


def _get_contracts(filters):
	contract_filters = {"docstatus": ["<", 2]}
	for fieldname in ("customer", "sales_contract", "real_estate_project", "unit"):
		if filters.get(fieldname):
			contract_filters["name" if fieldname == "sales_contract" else fieldname] = filters.get(fieldname)
	return frappe.get_all(
		"Sales Contract",
		filters=contract_filters,
		fields=["name", "customer", "unit", "real_estate_project"],
		order_by="contract_date desc, name desc",
	)


def _get_installments(contract_name, filters):
	installment_filters = {"parenttype": "Sales Contract", "parent": contract_name}
	return frappe.get_all(
		"Sales Installment Schedule",
		filters=installment_filters,
		fields=[
			"name",
			"sequence",
			"installment_number",
			"sales_invoice",
			"invoice_status",
			"payment_entry",
		],
		order_by="sequence asc, idx asc",
	)


def _get_payment_rows(invoice, contract, installment):
	rows = []
	references = frappe.get_all(
		"Payment Entry Reference",
		filters={"reference_doctype": "Sales Invoice", "reference_name": invoice.name},
		fields=["parent", "allocated_amount"],
	)
	for reference in references:
		if frappe.db.get_value("Payment Entry", reference.parent, "docstatus") != 1:
			continue
		posting_date = frappe.db.get_value("Payment Entry", reference.parent, "posting_date")
		rows.append(
			{
				"posting_date": posting_date,
				"sales_contract": contract.name,
				"unit": contract.unit,
				"invoice": invoice.name,
				"installment": installment.get("installment_number") or installment.get("sequence"),
				"debit": 0,
				"credit": flt(reference.allocated_amount),
				"outstanding": flt(invoice.outstanding_amount),
				"status": _("Payment Received"),
				"remarks": reference.parent,
			}
		)
	return rows
