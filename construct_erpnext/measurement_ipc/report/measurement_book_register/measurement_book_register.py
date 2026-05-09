import frappe
from frappe import _


def execute(filters=None):
	filters = filters or {}
	return get_columns(), get_data(filters)


def get_columns():
	return [
		{"label": _("Measurement Book"), "fieldname": "name", "fieldtype": "Link", "options": "Measurement Book", "width": 170},
		{"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 150},
		{"label": _("Contractor"), "fieldname": "contractor", "fieldtype": "Link", "options": "Supplier", "width": 150},
		{"label": _("Period Start"), "fieldname": "measurement_period_start", "fieldtype": "Date", "width": 110},
		{"label": _("Period End"), "fieldname": "measurement_period_end", "fieldtype": "Date", "width": 110},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 120},
		{"label": _("Total Entries"), "fieldname": "total_entries", "fieldtype": "Int", "width": 100},
		{"label": _("Total Accepted Qty"), "fieldname": "total_accepted_qty", "fieldtype": "Float", "width": 130},
		{"label": _("Total Measured Amount"), "fieldname": "total_measured_amount", "fieldtype": "Currency", "width": 150},
		{"label": _("Verified By"), "fieldname": "verified_by", "fieldtype": "Link", "options": "User", "width": 130},
		{"label": _("Verified On"), "fieldname": "verified_on", "fieldtype": "Datetime", "width": 150},
	]


def get_data(filters):
	conditions = []
	values = {}
	for fieldname in ("project", "contractor", "status"):
		if filters.get(fieldname):
			conditions.append(f"{fieldname} = %({fieldname})s")
			values[fieldname] = filters.get(fieldname)
	if filters.get("from_date"):
		conditions.append("measurement_period_start >= %(from_date)s")
		values["from_date"] = filters.get("from_date")
	if filters.get("to_date"):
		conditions.append("measurement_period_end <= %(to_date)s")
		values["to_date"] = filters.get("to_date")

	where = "WHERE " + " AND ".join(conditions) if conditions else ""
	return frappe.db.sql(
		f"""
		SELECT name, project, contractor, measurement_period_start, measurement_period_end,
			status, total_entries, total_accepted_qty, total_measured_amount,
			verified_by, verified_on
		FROM `tabMeasurement Book`
		{where}
		ORDER BY measurement_period_start DESC, name DESC
		""",
		values,
		as_dict=True,
	)
