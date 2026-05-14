import frappe


def execute(filters=None):
	filters = filters or {}
	conditions = {}
	for field in ("preferred_project", "requirement_type", "status", "priority"):
		if filters.get(field):
			conditions[field] = filters.get(field)
	data = frappe.get_all(
		"Customer Requirement",
		filters=conditions,
		fields=[
			"name as requirement",
			"requirement_title",
			"requirement_date",
			"requirement_type",
			"preferred_project",
			"unit_type",
			"budget_min",
			"budget_max",
			"status",
			"priority",
			"lead_source",
		],
		order_by="modified desc",
	)
	return _columns(), data


def _columns():
	return [
		{"label": "Requirement", "fieldname": "requirement", "fieldtype": "Link", "options": "Customer Requirement", "width": 150},
		{"label": "Requirement Title", "fieldname": "requirement_title", "fieldtype": "Data", "width": 260},
		{"label": "Requirement Date", "fieldname": "requirement_date", "fieldtype": "Date", "width": 120},
		{"label": "Requirement Type", "fieldname": "requirement_type", "fieldtype": "Data", "width": 120},
		{"label": "Preferred Project", "fieldname": "preferred_project", "fieldtype": "Link", "options": "Real Estate Project", "width": 150},
		{"label": "Unit Type", "fieldname": "unit_type", "fieldtype": "Link", "options": "Unit Type", "width": 130},
		{"label": "Budget Min", "fieldname": "budget_min", "fieldtype": "Currency", "width": 130},
		{"label": "Budget Max", "fieldname": "budget_max", "fieldtype": "Currency", "width": 130},
		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 110},
		{"label": "Priority", "fieldname": "priority", "fieldtype": "Data", "width": 100},
		{"label": "Lead Source", "fieldname": "lead_source", "fieldtype": "Data", "width": 140},
	]
