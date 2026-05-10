import frappe
from frappe import _
from frappe.utils import add_days, date_diff, nowdate


def execute(filters=None):
	filters = frappe._dict(filters or {})
	return get_columns(), get_data(filters)


def get_columns():
	return [
		{"label": _("Reservation"), "fieldname": "name", "fieldtype": "Link", "options": "Unit Reservation", "width": 170},
		{"label": _("Unit"), "fieldname": "unit", "fieldtype": "Link", "options": "Unit", "width": 120},
		{"label": _("Party"), "fieldname": "party", "fieldtype": "Data", "width": 180},
		{"label": _("Valid Until"), "fieldname": "valid_until", "fieldtype": "Date", "width": 120},
		{"label": _("Days Remaining"), "fieldname": "days_remaining", "fieldtype": "Int", "width": 120},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
	]


def get_data(filters):
	within_days = int(filters.get("within_days") or 7)
	conditions = [
		"status = 'Reserved'",
		"docstatus = 1",
		"valid_until <= %(through_date)s",
	]
	values = {"through_date": add_days(nowdate(), within_days)}
	if filters.get("real_estate_project"):
		conditions.append("real_estate_project = %(real_estate_project)s")
		values["real_estate_project"] = filters.real_estate_project

	rows = frappe.db.sql(
		f"""
		select name, unit, coalesce(customer, lead, party_name) as party,
			valid_until, status
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
