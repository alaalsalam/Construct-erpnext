import frappe


def execute(filters=None):
	filters = filters or {}
	conditions = {}
	for field in ("channel", "result"):
		if filters.get(field):
			conditions[field] = filters.get(field)
	if filters.get("from_date") or filters.get("to_date"):
		conditions["follow_up_date"] = ["between", [filters.get("from_date") or "1900-01-01", filters.get("to_date") or "2999-12-31"]]
	data = frappe.get_all(
		"Real Estate Follow Up",
		filters=conditions,
		fields=["name as follow_up", "requirement", "follow_up_date", "channel", "result", "lead", "customer", "assigned_to", "next_action"],
		order_by="follow_up_date desc",
	)
	return [
		{"label": "Follow Up", "fieldname": "follow_up", "fieldtype": "Link", "options": "Real Estate Follow Up", "width": 150},
		{"label": "Customer Requirement", "fieldname": "requirement", "fieldtype": "Link", "options": "Customer Requirement", "width": 170},
		{"label": "Follow Up Date", "fieldname": "follow_up_date", "fieldtype": "Date", "width": 130},
		{"label": "Channel", "fieldname": "channel", "fieldtype": "Data", "width": 110},
		{"label": "Result", "fieldname": "result", "fieldtype": "Data", "width": 150},
		{"label": "Lead", "fieldname": "lead", "fieldtype": "Link", "options": "Lead", "width": 140},
		{"label": "Customer", "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 160},
		{"label": "Assigned To", "fieldname": "assigned_to", "fieldtype": "Link", "options": "User", "width": 140},
		{"label": "Next Action", "fieldname": "next_action", "fieldtype": "Data", "width": 240},
	], data
