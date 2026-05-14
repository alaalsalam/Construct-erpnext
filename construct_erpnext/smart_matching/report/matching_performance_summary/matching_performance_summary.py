import frappe


def execute(filters=None):
	rows = frappe.get_all("Match Result", fields=["status", "total_matches", "best_score"])
	summary = {}
	for row in rows:
		summary.setdefault(row.status, {"status": row.status, "results_count": 0, "total_matches": 0, "average_best_score": 0})
		summary[row.status]["results_count"] += 1
		summary[row.status]["total_matches"] += row.total_matches or 0
		summary[row.status]["average_best_score"] += row.best_score or 0
	for row in summary.values():
		if row["results_count"]:
			row["average_best_score"] = round(row["average_best_score"] / row["results_count"], 2)
	return [
		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 150},
		{"label": "Results Count", "fieldname": "results_count", "fieldtype": "Int", "width": 130},
		{"label": "Total Matches", "fieldname": "total_matches", "fieldtype": "Int", "width": 130},
		{"label": "Average Best Score", "fieldname": "average_best_score", "fieldtype": "Float", "width": 150},
	], list(summary.values())
