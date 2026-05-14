import frappe


def execute(filters=None):
	filters = filters or {}
	conditions = {}
	if filters.get("preferred_project"):
		conditions["preferred_project"] = filters.get("preferred_project")
	if filters.get("requirement_type"):
		conditions["requirement_type"] = filters.get("requirement_type")
	rows = frappe.get_all("Customer Requirement", filters=conditions, fields=["status", "requirement_type", "budget_max"])
	summary = {}
	for row in rows:
		key = (row.status, row.requirement_type)
		summary.setdefault(key, {"status": row.status, "requirement_type": row.requirement_type, "requirements_count": 0, "pipeline_value": 0})
		summary[key]["requirements_count"] += 1
		summary[key]["pipeline_value"] += row.budget_max or 0
	return [
		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 140},
		{"label": "Requirement Type", "fieldname": "requirement_type", "fieldtype": "Data", "width": 140},
		{"label": "Requirements Count", "fieldname": "requirements_count", "fieldtype": "Int", "width": 150},
		{"label": "Pipeline Value", "fieldname": "pipeline_value", "fieldtype": "Currency", "width": 150},
	], list(summary.values())
