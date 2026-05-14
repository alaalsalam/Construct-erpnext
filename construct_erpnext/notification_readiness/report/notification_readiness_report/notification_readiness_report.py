import frappe


def execute(filters=None):
	filters = filters or {}
	conditions = {}
	if filters.get("scenario"):
		conditions["scenario"] = filters.get("scenario")
	if filters.get("status"):
		conditions["status"] = filters.get("status")
	data = frappe.get_all("Reminder Setting", filters=conditions, fields=["name", "scenario", "status", "lead_days", "channel", "target_doctype", "last_evaluated_on"], order_by="scenario")
	return _columns(), data


def _columns():
	return [
		{"label": "Reminder Setting", "fieldname": "name", "fieldtype": "Link", "options": "Reminder Setting", "width": 170},
		{"label": "Scenario", "fieldname": "scenario", "fieldtype": "Data", "width": 170},
		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 110},
		{"label": "Lead Days", "fieldname": "lead_days", "fieldtype": "Int", "width": 100},
		{"label": "Channel", "fieldname": "channel", "fieldtype": "Data", "width": 120},
		{"label": "Target DocType", "fieldname": "target_doctype", "fieldtype": "Data", "width": 160},
		{"label": "Last Evaluated On", "fieldname": "last_evaluated_on", "fieldtype": "Date", "width": 140},
	]
