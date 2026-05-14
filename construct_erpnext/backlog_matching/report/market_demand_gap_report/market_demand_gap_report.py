import frappe


def execute(filters=None):
	rows = frappe.get_all("Backlog Request", fields=["reason", "status", "priority_score"])
	summary = {}
	for row in rows:
		summary.setdefault(row.reason, {"reason": row.reason, "active_count": 0, "matched_count": 0, "average_priority": 0})
		if row.status == "Active":
			summary[row.reason]["active_count"] += 1
		if row.status == "Matched":
			summary[row.reason]["matched_count"] += 1
		summary[row.reason]["average_priority"] += row.priority_score or 0
	for row in summary.values():
		count = row["active_count"] + row["matched_count"]
		if count:
			row["average_priority"] = round(row["average_priority"] / count, 2)
	return [
		{"label": "Reason", "fieldname": "reason", "fieldtype": "Data", "width": 140},
		{"label": "Active Count", "fieldname": "active_count", "fieldtype": "Int", "width": 130},
		{"label": "Matched Count", "fieldname": "matched_count", "fieldtype": "Int", "width": 130},
		{"label": "Average Priority", "fieldname": "average_priority", "fieldtype": "Float", "width": 140},
	], list(summary.values())
