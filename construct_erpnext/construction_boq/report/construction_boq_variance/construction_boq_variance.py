import frappe
from frappe import _


def execute(filters=None):
	filters = filters or {}
	return get_columns(), get_data(filters)


def get_columns():
	return [
		{"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 170},
		{"label": _("Construction BOQ"), "fieldname": "construction_boq", "fieldtype": "Link", "options": "Construction BOQ", "width": 180},
		{"label": _("Total Amount"), "fieldname": "total_amount", "fieldtype": "Currency", "width": 130},
		{"label": _("Actual Cost"), "fieldname": "total_actual_cost", "fieldtype": "Currency", "width": 130},
		{"label": _("Variance Amount"), "fieldname": "variance_amount", "fieldtype": "Currency", "width": 140},
		{"label": _("Variance %"), "fieldname": "variance_percent", "fieldtype": "Percent", "width": 120},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 120},
	]


def get_data(filters):
	conditions = ["docstatus < 2"]
	values = {}

	if filters.get("project"):
		conditions.append("project = %(project)s")
		values["project"] = filters.get("project")
	if filters.get("status"):
		conditions.append("status = %(status)s")
		values["status"] = filters.get("status")

	return frappe.db.sql(
		"""
		SELECT
			project,
			name AS construction_boq,
			total_amount,
			total_actual_cost,
			variance_amount,
			variance_percent,
			status
		FROM `tabConstruction BOQ`
		WHERE {conditions}
		ORDER BY project, modified DESC
		""".format(conditions=" AND ".join(conditions)),
		values,
		as_dict=True,
	)
