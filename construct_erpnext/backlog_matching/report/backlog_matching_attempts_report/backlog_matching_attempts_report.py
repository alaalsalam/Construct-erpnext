import frappe


def execute(filters=None):
	filters = filters or {}
	conditions = {}
	for field in ("backlog_request", "result"):
		if filters.get(field):
			conditions[field] = filters.get(field)
	data = frappe.get_all(
		"Backlog Match Attempt",
		filters=conditions,
		fields=["name as attempt", "backlog_request", "attempt_date", "result", "matched_unit", "units_checked", "best_score"],
		order_by="attempt_date desc",
	)
	return [
		{"label": "Attempt", "fieldname": "attempt", "fieldtype": "Link", "options": "Backlog Match Attempt", "width": 150},
		{"label": "Backlog Request", "fieldname": "backlog_request", "fieldtype": "Link", "options": "Backlog Request", "width": 150},
		{"label": "Attempt Date", "fieldname": "attempt_date", "fieldtype": "Datetime", "width": 160},
		{"label": "Result", "fieldname": "result", "fieldtype": "Data", "width": 120},
		{"label": "Matched Unit", "fieldname": "matched_unit", "fieldtype": "Link", "options": "Unit", "width": 130},
		{"label": "Units Checked", "fieldname": "units_checked", "fieldtype": "Int", "width": 120},
		{"label": "Best Score", "fieldname": "best_score", "fieldtype": "Float", "width": 120},
	], data
