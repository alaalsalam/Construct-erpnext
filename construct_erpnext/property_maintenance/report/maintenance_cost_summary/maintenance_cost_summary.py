import frappe


def execute(filters=None):
	rows = frappe.get_all("Property Maintenance Request", fields=["issue_type", "estimated_cost", "actual_cost"])
	summary = {}
	for row in rows:
		summary.setdefault(row.issue_type, {"issue_type": row.issue_type, "requests_count": 0, "estimated_cost": 0, "actual_cost": 0})
		summary[row.issue_type]["requests_count"] += 1
		summary[row.issue_type]["estimated_cost"] += row.estimated_cost or 0
		summary[row.issue_type]["actual_cost"] += row.actual_cost or 0
	return [
		{"label": "Issue Type", "fieldname": "issue_type", "fieldtype": "Data", "width": 140},
		{"label": "Requests Count", "fieldname": "requests_count", "fieldtype": "Int", "width": 130},
		{"label": "Estimated Cost", "fieldname": "estimated_cost", "fieldtype": "Currency", "width": 140},
		{"label": "Actual Cost", "fieldname": "actual_cost", "fieldtype": "Currency", "width": 140},
	], list(summary.values())
