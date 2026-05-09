import frappe
from frappe import _


def execute(filters=None):
	filters = filters or {}
	return get_columns(), get_data(filters)


def get_columns():
	return [
		{"label": _("Measurement Entry"), "fieldname": "name", "fieldtype": "Link", "options": "Measurement Entry", "width": 160},
		{"label": _("Measurement Book"), "fieldname": "measurement_book", "fieldtype": "Link", "options": "Measurement Book", "width": 170},
		{"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 140},
		{"label": _("Work Item"), "fieldname": "construction_work_item", "fieldtype": "Link", "options": "Construction Work Item", "width": 160},
		{"label": _("Description"), "fieldname": "description", "fieldtype": "Data", "width": 240},
		{"label": _("Current Measured Qty"), "fieldname": "current_measured_qty", "fieldtype": "Float", "width": 140},
		{"label": _("Accepted Qty"), "fieldname": "accepted_qty", "fieldtype": "Float", "width": 110},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 110},
		{"label": _("Measured By"), "fieldname": "measured_by", "fieldtype": "Link", "options": "User", "width": 130},
		{"label": _("Measurement Date"), "fieldname": "measurement_date", "fieldtype": "Date", "width": 120},
		{"label": _("Engineer Comment"), "fieldname": "engineer_comment", "fieldtype": "Data", "width": 220},
	]


def get_data(filters):
	conditions = []
	values = {}
	for fieldname in ("project", "contractor", "status", "measured_by"):
		if filters.get(fieldname):
			conditions.append(f"{fieldname} = %({fieldname})s")
			values[fieldname] = filters.get(fieldname)

	where = "WHERE " + " AND ".join(conditions) if conditions else ""
	return frappe.db.sql(
		f"""
		SELECT name, measurement_book, project, construction_work_item, description,
			current_measured_qty, accepted_qty, status, measured_by, measurement_date,
			engineer_comment
		FROM `tabMeasurement Entry`
		{where}
		ORDER BY measurement_date DESC, modified DESC
		""",
		values,
		as_dict=True,
	)
