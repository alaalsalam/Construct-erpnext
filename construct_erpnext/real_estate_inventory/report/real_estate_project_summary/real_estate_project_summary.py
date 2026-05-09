import frappe
from frappe import _


def execute(filters=None):
	filters = filters or {}
	columns = [
		{"label": _("Real Estate Project"), "fieldname": "real_estate_project", "fieldtype": "Link", "options": "Real Estate Project", "width": 180},
		{"label": _("ERPNext Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 160},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 120},
		{"label": _("Total Units"), "fieldname": "total_units", "fieldtype": "Int", "width": 100},
		{"label": _("Available"), "fieldname": "available_units", "fieldtype": "Int", "width": 90},
		{"label": _("Reserved"), "fieldname": "reserved_units", "fieldtype": "Int", "width": 90},
		{"label": _("Sold"), "fieldname": "sold_units", "fieldtype": "Int", "width": 80},
		{"label": _("Rented"), "fieldname": "rented_units", "fieldtype": "Int", "width": 80},
		{"label": _("Blocked"), "fieldname": "blocked_units", "fieldtype": "Int", "width": 80},
		{"label": _("Total Expected Sales Value"), "fieldname": "total_expected_sales_value", "fieldtype": "Currency", "width": 170},
		{"label": _("Total Allocated Cost"), "fieldname": "total_allocated_cost", "fieldtype": "Currency", "width": 150},
		{"label": _("Expected Margin"), "fieldname": "expected_margin", "fieldtype": "Currency", "width": 130},
	]
	conditions = ["1=1"]
	values = {}
	if filters.get("real_estate_project"):
		conditions.append("rep.name = %(real_estate_project)s")
		values["real_estate_project"] = filters["real_estate_project"]
	if filters.get("status"):
		conditions.append("rep.status = %(status)s")
		values["status"] = filters["status"]
	data = frappe.db.sql(
		f"""
		SELECT rep.name AS real_estate_project, rep.project, rep.status,
			rep.total_units, rep.available_units, rep.reserved_units,
			rep.sold_units, rep.rented_units, rep.blocked_units,
			COALESCE(SUM(u.expected_sale_price), 0) AS total_expected_sales_value,
			COALESCE(SUM(u.allocated_cost), 0) AS total_allocated_cost,
			COALESCE(SUM(u.expected_margin), 0) AS expected_margin
		FROM `tabReal Estate Project` rep
		LEFT JOIN `tabUnit` u ON u.real_estate_project = rep.name
		WHERE {" AND ".join(conditions)}
		GROUP BY rep.name
		ORDER BY rep.modified DESC
		""",
		values,
		as_dict=True,
	)
	return columns, data
