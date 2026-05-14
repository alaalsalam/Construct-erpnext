import frappe
from frappe import _


def execute(filters=None):
	return get_columns(), get_data(frappe._dict(filters or {}))


def get_columns():
	return [
		{"fieldname": "lease_contract", "fieldtype": "Link", "label": _("Lease Contract"), "options": "Lease Contract", "width": 150},
		{"fieldname": "unit", "fieldtype": "Link", "label": _("Unit"), "options": "Unit", "width": 120},
		{"fieldname": "customer", "fieldtype": "Link", "label": _("Customer"), "options": "Customer", "width": 170},
		{"fieldname": "rent_period", "fieldtype": "Data", "label": _("Rent Period"), "width": 130},
		{"fieldname": "due_date", "fieldtype": "Date", "label": _("Due Date"), "width": 110},
		{"fieldname": "rent_amount", "fieldtype": "Currency", "label": _("Rent Amount"), "width": 130},
		{"fieldname": "sales_invoice", "fieldtype": "Link", "label": _("Invoice"), "options": "Sales Invoice", "width": 150},
		{"fieldname": "rent_status", "fieldtype": "Data", "label": _("Status"), "width": 130},
		{"fieldname": "invoice_amount", "fieldtype": "Currency", "label": _("Invoice Amount"), "width": 130},
		{"fieldname": "paid_amount", "fieldtype": "Currency", "label": _("Paid Amount"), "width": 130},
		{"fieldname": "outstanding_amount", "fieldtype": "Currency", "label": _("Outstanding Amount"), "width": 140},
	]


def get_data(filters):
	data = []
	for lease in _get_leases(filters):
		for row in frappe.get_all(
			"Rent Schedule",
			filters=_schedule_filters(lease.name, filters),
			fields=["sequence", "label", "due_date", "rent_amount", "sales_invoice", "rent_status", "invoice_amount", "paid_amount", "outstanding_amount"],
			order_by="sequence asc, idx asc",
		):
			data.append(
				{
					"lease_contract": lease.name,
					"unit": lease.unit,
					"customer": lease.customer,
					"rent_period": row.label or row.sequence,
					"due_date": row.due_date,
					"rent_amount": row.rent_amount,
					"sales_invoice": row.sales_invoice,
					"rent_status": row.rent_status,
					"invoice_amount": row.invoice_amount,
					"paid_amount": row.paid_amount,
					"outstanding_amount": row.outstanding_amount,
				}
			)
	return data


def _get_leases(filters):
	lease_filters = {"docstatus": ["<", 2]}
	for fieldname in ("company", "real_estate_project", "customer", "lease_contract"):
		if filters.get(fieldname):
			lease_filters["name" if fieldname == "lease_contract" else fieldname] = filters.get(fieldname)
	return frappe.get_all("Lease Contract", filters=lease_filters, fields=["name", "unit", "customer"], order_by="contract_date desc, name desc")


def _schedule_filters(lease_contract, filters):
	schedule_filters = {"parenttype": "Lease Contract", "parent": lease_contract}
	if filters.get("rent_status"):
		schedule_filters["rent_status"] = filters.rent_status
	if filters.get("from_due_date") and filters.get("to_due_date"):
		schedule_filters["due_date"] = ["between", [filters.from_due_date, filters.to_due_date]]
	elif filters.get("from_due_date"):
		schedule_filters["due_date"] = [">=", filters.from_due_date]
	elif filters.get("to_due_date"):
		schedule_filters["due_date"] = ["<=", filters.to_due_date]
	return schedule_filters
