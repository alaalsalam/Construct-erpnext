import frappe


def execute(filters=None):
	filters = filters or {}
	conditions = {}
	for field in ("customer_requirement", "status"):
		if filters.get(field):
			conditions[field] = filters.get(field)
	data = frappe.get_all(
		"Match Result",
		filters=conditions,
		fields=["name as match_result", "customer_requirement", "match_date", "status", "total_matches", "best_score"],
		order_by="modified desc",
	)
	return [
		{"label": "Match Result", "fieldname": "match_result", "fieldtype": "Link", "options": "Match Result", "width": 150},
		{"label": "Customer Requirement", "fieldname": "customer_requirement", "fieldtype": "Link", "options": "Customer Requirement", "width": 170},
		{"label": "Match Date", "fieldname": "match_date", "fieldtype": "Date", "width": 120},
		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 130},
		{"label": "Total Matches", "fieldname": "total_matches", "fieldtype": "Int", "width": 120},
		{"label": "Best Score", "fieldname": "best_score", "fieldtype": "Float", "width": 120},
	], data
