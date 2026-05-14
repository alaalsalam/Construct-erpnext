import frappe
from frappe import _
from frappe.utils import flt, getdate, nowdate


def execute(filters=None):
	return get_columns(), get_data(frappe._dict(filters or {}))


def get_columns():
	return [
		{"fieldname": "real_estate_project", "fieldtype": "Link", "label": _("Project"), "options": "Real Estate Project", "width": 180},
		{"fieldname": "lease_count", "fieldtype": "Int", "label": _("Lease Count"), "width": 120},
		{"fieldname": "scheduled_rent", "fieldtype": "Currency", "label": _("Scheduled Rent"), "width": 150},
		{"fieldname": "invoiced_rent", "fieldtype": "Currency", "label": _("Invoiced Rent"), "width": 150},
		{"fieldname": "collected_rent", "fieldtype": "Currency", "label": _("Collected Rent"), "width": 150},
		{"fieldname": "outstanding_rent", "fieldtype": "Currency", "label": _("Outstanding Rent"), "width": 150},
		{"fieldname": "overdue_amount", "fieldtype": "Currency", "label": _("Overdue Amount"), "width": 150},
	]


def get_data(filters):
	lease_filters = {"docstatus": ["<", 2]}
	if filters.get("real_estate_project"):
		lease_filters["real_estate_project"] = filters.real_estate_project
	rows_by_project = {}
	for lease in frappe.get_all(
		"Lease Contract",
		filters=lease_filters,
		fields=["name", "real_estate_project", "total_scheduled_rent", "total_invoiced_rent", "total_collected_rent", "total_outstanding_rent"],
	):
		project = lease.real_estate_project or _("Unassigned")
		row = rows_by_project.setdefault(
			project,
			{
				"real_estate_project": project,
				"lease_count": 0,
				"scheduled_rent": 0,
				"invoiced_rent": 0,
				"collected_rent": 0,
				"outstanding_rent": 0,
				"overdue_amount": 0,
			},
		)
		row["lease_count"] += 1
		row["scheduled_rent"] += flt(lease.total_scheduled_rent)
		row["invoiced_rent"] += flt(lease.total_invoiced_rent)
		row["collected_rent"] += flt(lease.total_collected_rent)
		row["outstanding_rent"] += flt(lease.total_outstanding_rent)
		row["overdue_amount"] += _overdue_for_lease(lease.name)
	return list(rows_by_project.values())


def _overdue_for_lease(lease_contract):
	return sum(
		flt(row.outstanding_amount)
		for row in frappe.get_all(
			"Rent Schedule",
			filters={
				"parenttype": "Lease Contract",
				"parent": lease_contract,
				"rent_status": ["not in", ("Paid", "Waived", "Cancelled")],
			},
			fields=["outstanding_amount", "due_date"],
		)
		if row.due_date and getdate(row.due_date) < getdate(nowdate())
	)
