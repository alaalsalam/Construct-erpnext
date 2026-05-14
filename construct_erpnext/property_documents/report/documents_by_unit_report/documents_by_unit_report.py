import frappe


def execute(filters=None):
	filters = filters or {}
	conditions = {"unit": ["is", "set"]}
	if filters.get("unit"):
		conditions["unit"] = filters.get("unit")
	rows = frappe.get_all("Property Document", filters=conditions, fields=["unit", "document_type", "status"])
	summary = {}
	for row in rows:
		summary.setdefault(row.unit, {"unit": row.unit, "documents_count": 0, "active_count": 0, "expired_count": 0})
		summary[row.unit]["documents_count"] += 1
		if row.status == "Active":
			summary[row.unit]["active_count"] += 1
		if row.status == "Expired":
			summary[row.unit]["expired_count"] += 1
	return [
		{"label": "Unit", "fieldname": "unit", "fieldtype": "Link", "options": "Unit", "width": 150},
		{"label": "Documents Count", "fieldname": "documents_count", "fieldtype": "Int", "width": 140},
		{"label": "Active Count", "fieldname": "active_count", "fieldtype": "Int", "width": 130},
		{"label": "Expired Count", "fieldname": "expired_count", "fieldtype": "Int", "width": 130},
	], list(summary.values())
