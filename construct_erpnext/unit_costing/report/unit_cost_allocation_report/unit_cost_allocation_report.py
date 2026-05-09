import frappe
from frappe import _


def execute(filters=None):
	filters = filters or {}
	columns = [
		{"label": _("Allocation"), "fieldname": "name", "fieldtype": "Link", "options": "Unit Cost Allocation", "width": 140},
		{"label": _("Project"), "fieldname": "real_estate_project", "fieldtype": "Link", "options": "Real Estate Project", "width": 180},
		{"label": _("Basis"), "fieldname": "allocation_basis", "fieldtype": "Data", "width": 120},
		{"label": _("Cost Source"), "fieldname": "cost_source", "fieldtype": "Data", "width": 130},
		{"label": _("Source Amount"), "fieldname": "source_amount", "fieldtype": "Currency", "width": 130},
		{"label": _("Total Allocated"), "fieldname": "total_allocated_amount", "fieldtype": "Currency", "width": 140},
		{"label": _("Unallocated"), "fieldname": "unallocated_amount", "fieldtype": "Currency", "width": 120},
		{"label": _("Status"), "fieldname": "allocation_status", "fieldtype": "Data", "width": 110},
		{"label": _("Date"), "fieldname": "allocation_date", "fieldtype": "Date", "width": 110},
	]
	conditions = ["1=1"]
	values = {}
	for field in ("real_estate_project", "allocation_status", "allocation_basis", "cost_source"):
		if filters.get(field):
			conditions.append(f"{field} = %({field})s")
			values[field] = filters[field]
	data = frappe.db.sql(
		f"""
		SELECT name, real_estate_project, allocation_basis, cost_source, source_amount,
			total_allocated_amount, unallocated_amount, allocation_status, allocation_date
		FROM `tabUnit Cost Allocation`
		WHERE {" AND ".join(conditions)}
		ORDER BY allocation_date DESC, creation DESC
		""",
		values,
		as_dict=True,
	)
	return columns, data
