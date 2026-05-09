import frappe
from frappe import _


def execute(filters=None):
	filters = filters or {}
	columns = [
		{"label": _("Owner"), "fieldname": "property_owner", "fieldtype": "Link", "options": "Property Owner", "width": 170},
		{"label": _("Unit"), "fieldname": "unit", "fieldtype": "Link", "options": "Unit", "width": 120},
		{"label": _("Project"), "fieldname": "real_estate_project", "fieldtype": "Link", "options": "Real Estate Project", "width": 180},
		{"label": _("Ownership %"), "fieldname": "ownership_percentage", "fieldtype": "Percent", "width": 110},
		{"label": _("Role"), "fieldname": "ownership_role", "fieldtype": "Data", "width": 120},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
		{"label": _("Start Date"), "fieldname": "start_date", "fieldtype": "Date", "width": 110},
		{"label": _("End Date"), "fieldname": "end_date", "fieldtype": "Date", "width": 110},
	]
	conditions = ["1=1"]
	values = {}
	for field in ("real_estate_project", "property_owner", "unit", "status"):
		if filters.get(field):
			conditions.append(f"{field} = %({field})s")
			values[field] = filters[field]
	data = frappe.db.sql(
		f"""
		SELECT property_owner, unit, real_estate_project, ownership_percentage,
			ownership_role, status, start_date, end_date
		FROM `tabProperty Ownership`
		WHERE {" AND ".join(conditions)}
		ORDER BY real_estate_project, unit, property_owner
		""",
		values,
		as_dict=True,
	)
	return columns, data
