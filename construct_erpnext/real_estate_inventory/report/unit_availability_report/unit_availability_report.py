import frappe
from frappe import _


def execute(filters=None):
	filters = filters or {}
	columns = [
		{"label": _("Project"), "fieldname": "real_estate_project", "fieldtype": "Link", "options": "Real Estate Project", "width": 180},
		{"label": _("Building"), "fieldname": "building", "fieldtype": "Link", "options": "Building", "width": 140},
		{"label": _("Total Units"), "fieldname": "total_units", "fieldtype": "Int", "width": 100},
		{"label": _("Available"), "fieldname": "available_units", "fieldtype": "Int", "width": 100},
		{"label": _("Reserved"), "fieldname": "reserved_units", "fieldtype": "Int", "width": 100},
		{"label": _("Sold"), "fieldname": "sold_units", "fieldtype": "Int", "width": 90},
		{"label": _("Rented"), "fieldname": "rented_units", "fieldtype": "Int", "width": 90},
		{"label": _("Blocked"), "fieldname": "blocked_units", "fieldtype": "Int", "width": 90},
		{"label": _("Availability %"), "fieldname": "availability_percent", "fieldtype": "Percent", "width": 120},
	]
	conditions = ["1=1"]
	values = {}
	for field in ("real_estate_project", "building", "status", "usage_purpose"):
		if filters.get(field):
			conditions.append(f"{field} = %({field})s")
			values[field] = filters[field]
	data = frappe.db.sql(
		f"""
		SELECT real_estate_project, building,
			COUNT(*) AS total_units,
			SUM(CASE WHEN status = 'Available' THEN 1 ELSE 0 END) AS available_units,
			SUM(CASE WHEN status = 'Reserved' THEN 1 ELSE 0 END) AS reserved_units,
			SUM(CASE WHEN status = 'Sold' THEN 1 ELSE 0 END) AS sold_units,
			SUM(CASE WHEN status = 'Rented' THEN 1 ELSE 0 END) AS rented_units,
			SUM(CASE WHEN status = 'Blocked' THEN 1 ELSE 0 END) AS blocked_units,
			CASE WHEN COUNT(*) > 0 THEN SUM(CASE WHEN status = 'Available' THEN 1 ELSE 0 END) / COUNT(*) * 100 ELSE 0 END AS availability_percent
		FROM `tabUnit`
		WHERE {" AND ".join(conditions)}
		GROUP BY real_estate_project, building
		ORDER BY real_estate_project, building
		""",
		values,
		as_dict=True,
	)
	return columns, data
