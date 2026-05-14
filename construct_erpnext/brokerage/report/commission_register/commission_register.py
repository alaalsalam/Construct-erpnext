import frappe
from frappe import _


def execute(filters=None):
	return get_columns(), get_data(frappe._dict(filters or {}))


def get_columns():
	return [
		{"fieldname": "commission_entry", "fieldtype": "Link", "label": _("Commission Entry"), "options": "Commission Entry", "width": 150},
		{"fieldname": "broker", "fieldtype": "Link", "label": _("Broker"), "options": "Broker", "width": 170},
		{"fieldname": "transaction_type", "fieldtype": "Data", "label": _("Transaction Type"), "width": 120},
		{"fieldname": "sales_contract", "fieldtype": "Link", "label": _("Sales Contract"), "options": "Sales Contract", "width": 150},
		{"fieldname": "lease_contract", "fieldtype": "Link", "label": _("Lease Contract"), "options": "Lease Contract", "width": 150},
		{"fieldname": "sales_invoice", "fieldtype": "Link", "label": _("Sales Invoice"), "options": "Sales Invoice", "width": 150},
		{"fieldname": "unit", "fieldtype": "Link", "label": _("Unit"), "options": "Unit", "width": 130},
		{"fieldname": "customer", "fieldtype": "Link", "label": _("Customer"), "options": "Customer", "width": 170},
		{"fieldname": "commission_base_amount", "fieldtype": "Currency", "label": _("Commission Base Amount"), "width": 150},
		{"fieldname": "commission_percent", "fieldtype": "Percent", "label": _("Commission Percent"), "width": 130},
		{"fieldname": "commission_amount", "fieldtype": "Currency", "label": _("Commission Amount"), "width": 150},
		{"fieldname": "status", "fieldtype": "Data", "label": _("Status"), "width": 110},
	]


def get_data(filters):
	entry_filters = {}
	for fieldname in ("broker", "transaction_type", "status"):
		if filters.get(fieldname):
			entry_filters[fieldname] = filters.get(fieldname)
	if filters.get("from_date") and filters.get("to_date"):
		entry_filters["posting_date"] = ["between", [filters.from_date, filters.to_date]]
	elif filters.get("from_date"):
		entry_filters["posting_date"] = [">=", filters.from_date]
	elif filters.get("to_date"):
		entry_filters["posting_date"] = ["<=", filters.to_date]

	rows = frappe.get_all(
		"Commission Entry",
		filters=entry_filters,
		fields=[
			"name",
			"broker",
			"transaction_type",
			"sales_contract",
			"lease_contract",
			"sales_invoice",
			"unit",
			"customer",
			"commission_base_amount",
			"commission_percent",
			"commission_amount",
			"status",
		],
		order_by="posting_date desc, name desc",
	)
	for row in rows:
		row["commission_entry"] = row.name
	return rows
