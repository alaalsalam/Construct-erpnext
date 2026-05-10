import frappe
from frappe import _


def execute(filters=None):
	return get_columns(), get_data(filters or {})


def get_columns():
	return [
		{"fieldname": "project", "fieldtype": "Link", "label": _("Project"), "options": "Real Estate Project", "width": 180},
		{"fieldname": "active_leases", "fieldtype": "Int", "label": _("Active Leases"), "width": 110},
		{"fieldname": "total_scheduled_rent", "fieldtype": "Currency", "label": _("Total Scheduled Rent"), "width": 160},
		{"fieldname": "monthly_rent_value", "fieldtype": "Currency", "label": _("Monthly Rent Value"), "width": 150},
		{"fieldname": "rented_units", "fieldtype": "Int", "label": _("Rented Units"), "width": 110},
		{"fieldname": "available_units", "fieldtype": "Int", "label": _("Available Units"), "width": 120},
	]


def get_data(filters):
	conditions = []
	values = {}
	if filters.get("real_estate_project"):
		conditions.append("lc.real_estate_project = %(real_estate_project)s")
		values["real_estate_project"] = filters["real_estate_project"]
	if filters.get("from_date"):
		conditions.append("lc.lease_start_date >= %(from_date)s")
		values["from_date"] = filters["from_date"]
	if filters.get("to_date"):
		conditions.append("lc.lease_start_date <= %(to_date)s")
		values["to_date"] = filters["to_date"]

	where_clause = (" AND " + " AND ".join(conditions)) if conditions else ""
	return frappe.db.sql(
		f"""
		SELECT
			lc.real_estate_project AS project,
			COUNT(CASE WHEN lc.lease_status IN ('Approved', 'Active') AND lc.docstatus = 1 THEN 1 END) AS active_leases,
			SUM(CASE WHEN lc.docstatus < 2 THEN lc.total_scheduled_rent ELSE 0 END) AS total_scheduled_rent,
			SUM(CASE WHEN lc.lease_status IN ('Approved', 'Active') AND lc.docstatus = 1 THEN lc.monthly_rent ELSE 0 END) AS monthly_rent_value,
			COALESCE(rep.rented_units, 0) AS rented_units,
			COALESCE(rep.available_units, 0) AS available_units
		FROM `tabLease Contract` lc
		LEFT JOIN `tabReal Estate Project` rep ON rep.name = lc.real_estate_project
		WHERE lc.real_estate_project IS NOT NULL
		{where_clause}
		GROUP BY lc.real_estate_project
		ORDER BY lc.real_estate_project
		""",
		values,
		as_dict=1,
	)
