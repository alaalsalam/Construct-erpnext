import frappe


def execute(filters=None):
	filters = filters or {}
	conditions = {}
	if filters.get("preferred_project"):
		conditions["preferred_project"] = filters.get("preferred_project")
	rows = frappe.get_all("Customer Requirement", filters=conditions, fields=["lead_source", "status", "budget_max"])
	summary = {}
	for row in rows:
		source = row.lead_source or "Not Specified"
		summary.setdefault(source, {"lead_source": source, "requirements_count": 0, "won_count": 0, "backlog_count": 0, "pipeline_value": 0})
		summary[source]["requirements_count"] += 1
		summary[source]["pipeline_value"] += row.budget_max or 0
		if row.status == "Won":
			summary[source]["won_count"] += 1
		if row.status == "Backlog":
			summary[source]["backlog_count"] += 1
	return [
		{"label": "Lead Source", "fieldname": "lead_source", "fieldtype": "Data", "width": 180},
		{"label": "Requirements Count", "fieldname": "requirements_count", "fieldtype": "Int", "width": 150},
		{"label": "Won Count", "fieldname": "won_count", "fieldtype": "Int", "width": 120},
		{"label": "Backlog Count", "fieldname": "backlog_count", "fieldtype": "Int", "width": 130},
		{"label": "Pipeline Value", "fieldname": "pipeline_value", "fieldtype": "Currency", "width": 160},
	], list(summary.values())
