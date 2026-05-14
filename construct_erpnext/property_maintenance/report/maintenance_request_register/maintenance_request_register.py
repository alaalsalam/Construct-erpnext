import frappe


def execute(filters=None):
	filters = filters or {}
	conditions = {}
	for field in ("real_estate_project", "status"):
		if filters.get(field):
			conditions[field] = filters.get(field)
	data = frappe.get_all("Property Maintenance Request", filters=conditions, fields=["name as request", "unit", "real_estate_project", "request_date", "issue_type", "priority", "status", "estimated_cost", "actual_cost"], order_by="modified desc")
	return _columns(), data


def _columns():
	return [
		{"label": "Request", "fieldname": "request", "fieldtype": "Link", "options": "Property Maintenance Request", "width": 150},
		{"label": "Unit", "fieldname": "unit", "fieldtype": "Link", "options": "Unit", "width": 130},
		{"label": "Real Estate Project", "fieldname": "real_estate_project", "fieldtype": "Link", "options": "Real Estate Project", "width": 160},
		{"label": "Request Date", "fieldname": "request_date", "fieldtype": "Date", "width": 120},
		{"label": "Issue Type", "fieldname": "issue_type", "fieldtype": "Data", "width": 120},
		{"label": "Priority", "fieldname": "priority", "fieldtype": "Data", "width": 100},
		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
		{"label": "Estimated Cost", "fieldname": "estimated_cost", "fieldtype": "Currency", "width": 130},
		{"label": "Actual Cost", "fieldname": "actual_cost", "fieldtype": "Currency", "width": 130},
	]
