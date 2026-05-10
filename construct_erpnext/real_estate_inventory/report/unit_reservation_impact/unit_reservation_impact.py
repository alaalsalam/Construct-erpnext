import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
	filters = frappe._dict(filters or {})
	return get_columns(), get_data(filters)


def get_columns():
	return [
		{"label": _("Project"), "fieldname": "real_estate_project", "fieldtype": "Link", "options": "Real Estate Project", "width": 190},
		{"label": _("Building"), "fieldname": "building", "fieldtype": "Link", "options": "Building", "width": 150},
		{"label": _("Total Units"), "fieldname": "total_units", "fieldtype": "Int", "width": 110},
		{"label": _("Available Units"), "fieldname": "available_units", "fieldtype": "Int", "width": 120},
		{"label": _("Reserved Units"), "fieldname": "reserved_units", "fieldtype": "Int", "width": 120},
		{"label": _("Sold Units"), "fieldname": "sold_units", "fieldtype": "Int", "width": 100},
		{"label": _("Rented Units"), "fieldname": "rented_units", "fieldtype": "Int", "width": 110},
		{"label": _("Reservation Rate %"), "fieldname": "reservation_rate", "fieldtype": "Percent", "width": 130},
	]


def get_data(filters):
	conditions = []
	values = {}
	for field in ("real_estate_project", "building"):
		if filters.get(field):
			conditions.append(f"{field} = %({field})s")
			values[field] = filters[field]

	where = " where " + " and ".join(conditions) if conditions else ""
	rows = frappe.db.sql(
		f"""
		select
			real_estate_project,
			coalesce(building, '') as building,
			count(*) as total_units,
			sum(case when status = 'Available' then 1 else 0 end) as available_units,
			sum(case when status = 'Reserved' then 1 else 0 end) as reserved_units,
			sum(case when status = 'Sold' then 1 else 0 end) as sold_units,
			sum(case when status = 'Rented' then 1 else 0 end) as rented_units
		from `tabUnit`
		{where}
		group by real_estate_project, building
		order by real_estate_project, building
		""",
		values,
		as_dict=True,
	)
	for row in rows:
		row.reservation_rate = flt(row.reserved_units) / flt(row.total_units) * 100 if row.total_units else 0
	return rows
