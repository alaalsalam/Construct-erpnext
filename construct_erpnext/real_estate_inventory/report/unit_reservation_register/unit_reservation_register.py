import frappe
from frappe import _


def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"label": _("Reservation"), "fieldname": "name", "fieldtype": "Link", "options": "Unit Reservation", "width": 170},
		{"label": _("Unit"), "fieldname": "unit", "fieldtype": "Link", "options": "Unit", "width": 120},
		{"label": _("Project"), "fieldname": "real_estate_project", "fieldtype": "Link", "options": "Real Estate Project", "width": 180},
		{"label": _("Building"), "fieldname": "building", "fieldtype": "Link", "options": "Building", "width": 130},
		{"label": _("Floor"), "fieldname": "floor", "fieldtype": "Link", "options": "Floor", "width": 130},
		{"label": _("Type"), "fieldname": "reservation_type", "fieldtype": "Data", "width": 80},
		{"label": _("Party"), "fieldname": "party", "fieldtype": "Data", "width": 180},
		{"label": _("Reservation Date"), "fieldname": "reservation_date", "fieldtype": "Date", "width": 120},
		{"label": _("Valid Until"), "fieldname": "valid_until", "fieldtype": "Date", "width": 120},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
		{"label": _("Reservation Amount"), "fieldname": "reservation_amount", "fieldtype": "Currency", "width": 140},
		{"label": _("Remarks"), "fieldname": "remarks", "fieldtype": "Data", "width": 220},
	]


def get_data(filters):
	conditions = []
	values = {}

	for field in ("real_estate_project", "unit", "customer", "lead", "reservation_type", "status"):
		if filters.get(field):
			conditions.append(f"{field} = %({field})s")
			values[field] = filters[field]

	if filters.get("from_date"):
		conditions.append("reservation_date >= %(from_date)s")
		values["from_date"] = filters.from_date
	if filters.get("to_date"):
		conditions.append("reservation_date <= %(to_date)s")
		values["to_date"] = filters.to_date

	where = " where " + " and ".join(conditions) if conditions else ""
	return frappe.db.sql(
		f"""
		select
			name, unit, real_estate_project, building, floor, reservation_type,
			coalesce(customer, lead, party_name) as party,
			reservation_date, valid_until, status, reservation_amount, remarks
		from `tabUnit Reservation`
		{where}
		order by reservation_date desc, creation desc
		""",
		values,
		as_dict=True,
	)
