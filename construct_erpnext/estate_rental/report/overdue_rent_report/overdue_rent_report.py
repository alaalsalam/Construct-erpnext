import frappe
from frappe import _
from frappe.utils import flt, getdate, nowdate


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
		{"fieldname": "outstanding_amount", "fieldtype": "Currency", "label": _("Outstanding Amount"), "width": 150},
		{"fieldname": "overdue_days", "fieldtype": "Int", "label": _("Overdue Days"), "width": 120},
		{"fieldname": "status", "fieldtype": "Data", "label": _("Status"), "width": 130},
	]


def get_data(filters):
	data = []
	min_days = flt(filters.get("overdue_days_min") or 0)
	for lease in _get_leases(filters):
		for row in frappe.get_all(
			"Rent Schedule",
			filters={"parenttype": "Lease Contract", "parent": lease.name, "rent_status": ["not in", ("Paid", "Waived", "Cancelled")]},
			fields=["sequence", "label", "due_date", "rent_amount", "outstanding_amount", "overdue_days", "rent_status"],
			order_by="due_date asc, idx asc",
		):
			outstanding = flt(row.outstanding_amount) if row.outstanding_amount is not None else flt(row.rent_amount)
			overdue_days = row.overdue_days or max((getdate(nowdate()) - getdate(row.due_date)).days, 0) if row.due_date else 0
			if outstanding <= 0 or overdue_days < min_days:
				continue
			data.append(
				{
					"lease_contract": lease.name,
					"unit": lease.unit,
					"customer": lease.customer,
					"rent_period": row.label or row.sequence,
					"due_date": row.due_date,
					"rent_amount": row.rent_amount,
					"outstanding_amount": outstanding,
					"overdue_days": overdue_days,
					"status": row.rent_status,
				}
			)
	return data


def _get_leases(filters):
	lease_filters = {"docstatus": ["<", 2]}
	for fieldname in ("real_estate_project", "customer"):
		if filters.get(fieldname):
			lease_filters[fieldname] = filters.get(fieldname)
	return frappe.get_all("Lease Contract", filters=lease_filters, fields=["name", "unit", "customer"], order_by="contract_date desc, name desc")
