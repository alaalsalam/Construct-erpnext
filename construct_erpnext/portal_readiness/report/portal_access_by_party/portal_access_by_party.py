import frappe


def execute(filters=None):
	rows = frappe.get_all("Portal Access Profile", fields=["party_type", "access_type"])
	summary = {}
	for row in rows:
		key = (row.party_type, row.access_type)
		summary.setdefault(key, {"party_type": row.party_type, "access_type": row.access_type, "profiles_count": 0})
		summary[key]["profiles_count"] += 1
	return [
		{"label": "Party Type", "fieldname": "party_type", "fieldtype": "Data", "width": 140},
		{"label": "Access Type", "fieldname": "access_type", "fieldtype": "Data", "width": 140},
		{"label": "Profiles Count", "fieldname": "profiles_count", "fieldtype": "Int", "width": 140},
	], list(summary.values())
