import frappe
from frappe import _
from construct_erpnext.reporting.report_utils import normalize_common_filters


def execute(filters=None):
	filters = normalize_common_filters(filters)
	columns = [
		{"label": _("Unit"), "fieldname": "unit", "fieldtype": "Link", "options": "Unit", "width": 120},
		{"label": _("Building"), "fieldname": "building", "fieldtype": "Link", "options": "Building", "width": 120},
		{"label": _("Floor"), "fieldname": "floor", "fieldtype": "Link", "options": "Floor", "width": 120},
		{"label": _("Allocated Cost"), "fieldname": "allocated_cost", "fieldtype": "Currency", "width": 130},
		{"label": _("GL Cost"), "fieldname": "gl_cost", "fieldtype": "Currency", "width": 120},
		{"label": _("Cost Code"), "fieldname": "cost_code", "fieldtype": "Link", "options": "Cost Code", "width": 120},
		{"label": _("Work Item"), "fieldname": "construction_work_item", "fieldtype": "Link", "options": "Construction Work Item", "width": 170},
		{"label": _("Variance"), "fieldname": "variance", "fieldtype": "Currency", "width": 120},
		{"label": _("Profitability Status"), "fieldname": "profitability_status", "fieldtype": "Data", "width": 140},
	]
	return columns, get_data(filters)


def get_data(filters):
	unit_conditions = []
	values = {}
	if filters.get("project"):
		unit_conditions.append("u.project = %(project)s")
		values["project"] = filters.project
	if filters.get("real_estate_project"):
		unit_conditions.append("u.real_estate_project = %(real_estate_project)s")
		values["real_estate_project"] = filters.real_estate_project

	units = frappe.db.sql(
		f"""
		SELECT u.name AS unit, u.building, u.floor, u.allocated_cost, u.profitability_status
		FROM `tabUnit` u
		{"WHERE " + " AND ".join(unit_conditions) if unit_conditions else ""}
		ORDER BY u.building, u.floor, u.unit_code
		""",
		values,
		as_dict=True,
	)

	gl_by_unit = get_gl_by_unit(filters)
	data = []
	for unit in units:
		gl_rows = gl_by_unit.get(unit.unit) or [frappe._dict({"gl_cost": 0, "cost_code": "", "construction_work_item": ""})]
		for gl_row in gl_rows:
			data.append({
				"unit": unit.unit,
				"building": unit.building,
				"floor": unit.floor,
				"allocated_cost": unit.allocated_cost,
				"gl_cost": gl_row.gl_cost,
				"cost_code": gl_row.cost_code,
				"construction_work_item": gl_row.construction_work_item,
				"variance": (unit.allocated_cost or 0) - (gl_row.gl_cost or 0),
				"profitability_status": unit.profitability_status,
			})
	return data


def get_gl_by_unit(filters):
	meta = frappe.get_meta("GL Entry", cached=False)
	if not meta.get_field("unit"):
		return {}

	conditions = ["is_cancelled = 0", "IFNULL(unit, '') != ''"]
	values = {}
	if filters.get("project"):
		conditions.append("project = %(project)s")
		values["project"] = filters.project
	if filters.get("cost_code") and meta.get_field("cost_code"):
		conditions.append("cost_code = %(cost_code)s")
		values["cost_code"] = filters.cost_code

	cost_code_select = "cost_code" if meta.get_field("cost_code") else "'' AS cost_code"
	work_item_select = (
		"construction_work_item"
		if meta.get_field("construction_work_item")
		else "'' AS construction_work_item"
	)
	group_by = ["unit"]
	if meta.get_field("cost_code"):
		group_by.append("cost_code")
	if meta.get_field("construction_work_item"):
		group_by.append("construction_work_item")

	rows = frappe.db.sql(
		f"""
		SELECT unit, {cost_code_select}, {work_item_select}, SUM(debit - credit) AS gl_cost
		FROM `tabGL Entry`
		WHERE {" AND ".join(conditions)}
		GROUP BY {", ".join(group_by)}
		""",
		values,
		as_dict=True,
	)

	result = {}
	for row in rows:
		result.setdefault(row.unit, []).append(row)
	return result
