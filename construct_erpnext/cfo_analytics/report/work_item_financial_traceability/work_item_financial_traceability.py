import frappe
from frappe import _


def execute(filters=None):
	filters = filters or {}
	columns = [
		{"label": _("Work Item"), "fieldname": "name", "fieldtype": "Link", "options": "Construction Work Item", "width": 160},
		{"label": _("Description"), "fieldname": "description", "fieldtype": "Data", "width": 220},
		{"label": _("Planned Amount"), "fieldname": "planned_amount", "fieldtype": "Currency", "width": 130},
		{"label": _("Requested Qty"), "fieldname": "requested_qty", "fieldtype": "Float", "width": 110},
		{"label": _("Ordered Qty"), "fieldname": "ordered_qty", "fieldtype": "Float", "width": 110},
		{"label": _("Received Qty"), "fieldname": "received_qty", "fieldtype": "Float", "width": 110},
		{"label": _("Invoiced Qty"), "fieldname": "invoiced_qty", "fieldtype": "Float", "width": 110},
		{"label": _("Consumed Qty"), "fieldname": "consumed_qty", "fieldtype": "Float", "width": 110},
		{"label": _("Measured Qty"), "fieldname": "measured_qty", "fieldtype": "Float", "width": 110},
		{"label": _("Certified Qty"), "fieldname": "certified_qty", "fieldtype": "Float", "width": 110},
		{"label": _("Committed Amount"), "fieldname": "committed_amount", "fieldtype": "Currency", "width": 140},
		{"label": _("Invoiced Amount"), "fieldname": "invoiced_amount", "fieldtype": "Currency", "width": 140},
		{"label": _("Consumed Amount"), "fieldname": "consumed_amount", "fieldtype": "Currency", "width": 140},
		{"label": _("Measured Amount"), "fieldname": "measurement_amount", "fieldtype": "Currency", "width": 140},
		{"label": _("Certified Amount"), "fieldname": "certified_amount", "fieldtype": "Currency", "width": 140},
		{"label": _("Variance"), "fieldname": "variance", "fieldtype": "Currency", "width": 120},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 110},
	]
	conditions = ["IFNULL(disabled, 0) = 0"]
	values = {}
	for field in ("project", "construction_boq", "cost_code", "wbs_element"):
		if filters.get(field):
			conditions.append(f"{field} = %({field})s")
			values[field] = filters[field]
	if filters.get("construction_work_item"):
		conditions.append("name = %(construction_work_item)s")
		values["construction_work_item"] = filters["construction_work_item"]
	data = frappe.db.sql(
		f"""
		SELECT name, description, planned_amount, requested_qty, ordered_qty, received_qty,
			invoiced_qty, consumed_qty, measured_qty, certified_qty, committed_amount,
			invoiced_amount, consumed_amount, measurement_amount, certified_amount,
			(planned_amount - committed_amount) AS variance, status
		FROM `tabConstruction Work Item`
		WHERE {" AND ".join(conditions)}
		ORDER BY project, construction_boq, wbs_code, creation
		""",
		values,
		as_dict=True,
	)
	return columns, data
