import frappe
from frappe import _
from frappe.utils import date_diff, nowdate


def execute(filters=None):
	filters = frappe._dict(filters or {})
	return get_columns(), get_data(filters)


def get_columns():
	return [
		{"label": _("Unit"), "fieldname": "unit", "fieldtype": "Link", "options": "Unit", "width": 120},
		{"label": _("Reservation"), "fieldname": "name", "fieldtype": "Link", "options": "Unit Reservation", "width": 170},
		{"label": _("Party"), "fieldname": "party", "fieldtype": "Data", "width": 180},
		{"label": _("Valid From"), "fieldname": "valid_from", "fieldtype": "Date", "width": 120},
		{"label": _("Valid Until"), "fieldname": "valid_until", "fieldtype": "Date", "width": 120},
		{"label": _("Days Remaining"), "fieldname": "days_remaining", "fieldtype": "Int", "width": 120},
		{"label": _("Reservation Type"), "fieldname": "reservation_type", "fieldtype": "Data", "width": 130},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
	]


def get_data(filters):
	conditions = ["status = 'Reserved'", "docstatus = 1"]
	values = {}
	for field in ("real_estate_project", "building", "reservation_type"):
		if filters.get(field):
			conditions.append(f"{field} = %({field})s")
			values[field] = filters[field]

	rows = frappe.db.sql(
		f"""
		select name, unit, coalesce(customer, lead, party_name) as party,
			valid_from, valid_until, reservation_type, status
		from `tabUnit Reservation`
		where {" and ".join(conditions)}
		order by valid_until asc, creation desc
		""",
		values,
		as_dict=True,
	)
	for row in rows:
		row.days_remaining = date_diff(row.valid_until, nowdate()) if row.valid_until else None
	return rows
