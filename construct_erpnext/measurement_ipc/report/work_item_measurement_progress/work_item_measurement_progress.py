import frappe
from frappe import _


def execute(filters=None):
	filters = filters or {}
	return get_columns(), get_data(filters)


def get_columns():
	return [
		{"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 140},
		{"label": _("BOQ"), "fieldname": "construction_boq", "fieldtype": "Link", "options": "Construction BOQ", "width": 160},
		{"label": _("Work Item"), "fieldname": "name", "fieldtype": "Link", "options": "Construction Work Item", "width": 160},
		{"label": _("WBS"), "fieldname": "wbs_element", "fieldtype": "Link", "options": "WBS Element", "width": 140},
		{"label": _("Cost Code"), "fieldname": "cost_code", "fieldtype": "Link", "options": "Cost Code", "width": 120},
		{"label": _("Description"), "fieldname": "description", "fieldtype": "Data", "width": 240},
		{"label": _("Planned Qty"), "fieldname": "planned_quantity", "fieldtype": "Float", "width": 110},
		{"label": _("Measured Qty"), "fieldname": "measured_qty", "fieldtype": "Float", "width": 110},
		{"label": _("Remaining Qty"), "fieldname": "remaining_qty", "fieldtype": "Float", "width": 110},
		{"label": _("Progress %"), "fieldname": "measurement_progress_percent", "fieldtype": "Percent", "width": 100},
		{"label": _("Measurement Status"), "fieldname": "measurement_status", "fieldtype": "Data", "width": 140},
		{"label": _("Last Measurement Date"), "fieldname": "last_measurement_date", "fieldtype": "Date", "width": 130},
	]


def get_data(filters):
	conditions = ["disabled = 0"]
	values = {}
	for fieldname in ("project", "construction_boq", "measurement_status", "cost_code", "wbs_element"):
		if filters.get(fieldname):
			conditions.append(f"{fieldname} = %({fieldname})s")
			values[fieldname] = filters.get(fieldname)
	if filters.get("construction_work_item"):
		conditions.append("name = %(construction_work_item)s")
		values["construction_work_item"] = filters.get("construction_work_item")

	return frappe.db.sql(
		"""
		SELECT project, construction_boq, name, wbs_element, cost_code, description,
			planned_quantity, measured_qty, remaining_qty, measurement_progress_percent,
			measurement_status, last_measurement_date
		FROM `tabConstruction Work Item`
		WHERE {conditions}
		ORDER BY project, construction_boq, name
		""".format(conditions=" AND ".join(conditions)),
		values,
		as_dict=True,
	)
