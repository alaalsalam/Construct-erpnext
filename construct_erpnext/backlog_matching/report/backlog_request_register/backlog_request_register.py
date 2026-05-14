import frappe


def execute(filters=None):
	filters = filters or {}
	conditions = {}
	for field in ("status", "reason"):
		if filters.get(field):
			conditions[field] = filters.get(field)
	data = frappe.get_all(
		"Backlog Request",
		filters=conditions,
		fields=["name as backlog_request", "customer_requirement", "status", "reason", "priority_score", "waiting_since", "last_match_attempt", "matched_unit", "requirement_summary"],
		order_by="priority_score desc, modified desc",
	)
	return _columns(), data


def _columns():
	return [
		{"label": "Backlog Request", "fieldname": "backlog_request", "fieldtype": "Link", "options": "Backlog Request", "width": 150},
		{"label": "Customer Requirement", "fieldname": "customer_requirement", "fieldtype": "Link", "options": "Customer Requirement", "width": 170},
		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 110},
		{"label": "Reason", "fieldname": "reason", "fieldtype": "Data", "width": 120},
		{"label": "Priority Score", "fieldname": "priority_score", "fieldtype": "Float", "width": 120},
		{"label": "Waiting Since", "fieldname": "waiting_since", "fieldtype": "Date", "width": 120},
		{"label": "Last Match Attempt", "fieldname": "last_match_attempt", "fieldtype": "Datetime", "width": 160},
		{"label": "Matched Unit", "fieldname": "matched_unit", "fieldtype": "Link", "options": "Unit", "width": 130},
		{"label": "Requirement Summary", "fieldname": "requirement_summary", "fieldtype": "Data", "width": 280},
	]
