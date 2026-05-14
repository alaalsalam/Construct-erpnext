import frappe
from frappe import _


def execute(filters=None):
	return get_columns(), get_data(frappe._dict(filters or {}))


def get_columns():
	return [
		{"fieldname": "sales_contract", "fieldtype": "Link", "label": _("Sales Contract"), "options": "Sales Contract", "width": 150},
		{"fieldname": "customer", "fieldtype": "Link", "label": _("Customer"), "options": "Customer", "width": 170},
		{"fieldname": "unit", "fieldtype": "Link", "label": _("Unit"), "options": "Unit", "width": 140},
		{"fieldname": "installment_no", "fieldtype": "Data", "label": _("Installment No"), "width": 120},
		{"fieldname": "due_date", "fieldtype": "Date", "label": _("Due Date"), "width": 110},
		{"fieldname": "installment_amount", "fieldtype": "Currency", "label": _("Installment Amount"), "width": 140},
		{"fieldname": "invoice", "fieldtype": "Link", "label": _("Invoice"), "options": "Sales Invoice", "width": 150},
		{"fieldname": "invoice_status", "fieldtype": "Data", "label": _("Invoice Status"), "width": 130},
		{"fieldname": "paid_amount", "fieldtype": "Currency", "label": _("Paid Amount"), "width": 130},
		{"fieldname": "outstanding", "fieldtype": "Currency", "label": _("Outstanding"), "width": 130},
		{"fieldname": "overdue_days", "fieldtype": "Int", "label": _("Overdue Days"), "width": 120},
		{"fieldname": "collection_status", "fieldtype": "Data", "label": _("Collection Status"), "width": 150},
	]


def get_data(filters):
	data = []
	for contract in _get_contracts(filters):
		for row in frappe.get_all(
			"Sales Installment Schedule",
			filters=_get_installment_filters(contract.name, filters),
			fields=[
				"sequence",
				"installment_number",
				"due_date",
				"amount",
				"sales_invoice",
				"invoice_status",
				"paid_amount",
				"outstanding_amount",
				"overdue_days",
			],
			order_by="sequence asc, idx asc",
		):
			data.append(
				{
					"sales_contract": contract.name,
					"customer": contract.customer,
					"unit": contract.unit,
					"installment_no": row.installment_number or row.sequence,
					"due_date": row.due_date,
					"installment_amount": row.amount,
					"invoice": row.sales_invoice,
					"invoice_status": row.invoice_status,
					"paid_amount": row.paid_amount,
					"outstanding": row.outstanding_amount,
					"overdue_days": row.overdue_days,
					"collection_status": contract.collection_status,
				}
			)
	return data


def _get_contracts(filters):
	contract_filters = {"docstatus": ["<", 2]}
	for fieldname in ("real_estate_project", "sales_contract", "customer"):
		if filters.get(fieldname):
			contract_filters["name" if fieldname == "sales_contract" else fieldname] = filters.get(fieldname)
	return frappe.get_all(
		"Sales Contract",
		filters=contract_filters,
		fields=["name", "customer", "unit", "collection_status"],
		order_by="contract_date desc, name desc",
	)


def _get_installment_filters(contract_name, filters):
	installment_filters = {"parenttype": "Sales Contract", "parent": contract_name}
	if filters.get("status"):
		installment_filters["invoice_status"] = filters.status
	if filters.get("from_due_date"):
		installment_filters["due_date"] = [">=", filters.from_due_date]
	if filters.get("to_due_date"):
		if "due_date" in installment_filters:
			installment_filters["due_date"] = ["between", [filters.from_due_date, filters.to_due_date]]
		else:
			installment_filters["due_date"] = ["<=", filters.to_due_date]
	return installment_filters
