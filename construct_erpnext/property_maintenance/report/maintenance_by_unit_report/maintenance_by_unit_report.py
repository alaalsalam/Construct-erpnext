import frappe


def execute(filters=None):
	filters = filters or {}
	conditions = {}
	if filters.get("unit"):
		conditions["unit"] = filters.get("unit")
	rows = frappe.get_all("Property Maintenance Request", filters=conditions, fields=["unit", "estimated_cost", "actual_cost", "status"])
	summary = {}
	for row in rows:
		summary.setdefault(row.unit, {"unit": row.unit, "requests_count": 0, "open_count": 0, "estimated_cost": 0, "actual_cost": 0})
		summary[row.unit]["requests_count"] += 1
		if row.status not in ("Completed", "Cancelled"):
			summary[row.unit]["open_count"] += 1
		summary[row.unit]["estimated_cost"] += row.estimated_cost or 0
		summary[row.unit]["actual_cost"] += row.actual_cost or 0
	return [
		{"label": "Unit", "fieldname": "unit", "fieldtype": "Link", "options": "Unit", "width": 140},
		{"label": "Requests Count", "fieldname": "requests_count", "fieldtype": "Int", "width": 130},
		{"label": "Open Count", "fieldname": "open_count", "fieldtype": "Int", "width": 120},
		{"label": "Estimated Cost", "fieldname": "estimated_cost", "fieldtype": "Currency", "width": 140},
		{"label": "Actual Cost", "fieldname": "actual_cost", "fieldtype": "Currency", "width": 140},
	], list(summary.values())
