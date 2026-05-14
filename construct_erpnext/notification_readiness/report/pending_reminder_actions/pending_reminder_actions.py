import frappe


def execute(filters=None):
	filters = filters or {}
	conditions = {}
	if filters.get("scenario"):
		conditions["scenario"] = filters.get("scenario")
	if filters.get("status"):
		conditions["status"] = filters.get("status")
	data = frappe.get_all(
		"Automation Log",
		filters=conditions,
		fields=["name", "scenario", "source_doctype", "source_document", "party_type", "party", "due_date", "status", "action_notes"],
		order_by="due_date asc, modified desc",
	)
	return _columns(), data


def _columns():
	return [
		{"label": "Automation Log", "fieldname": "name", "fieldtype": "Link", "options": "Automation Log", "width": 170},
		{"label": "Scenario", "fieldname": "scenario", "fieldtype": "Data", "width": 170},
		{"label": "Source DocType", "fieldname": "source_doctype", "fieldtype": "Data", "width": 150},
		{"label": "Source Document", "fieldname": "source_document", "fieldtype": "Dynamic Link", "options": "source_doctype", "width": 170},
		{"label": "Party Type", "fieldname": "party_type", "fieldtype": "Data", "width": 120},
		{"label": "Party", "fieldname": "party", "fieldtype": "Dynamic Link", "options": "party_type", "width": 170},
		{"label": "Due Date", "fieldname": "due_date", "fieldtype": "Date", "width": 120},
		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100},
		{"label": "Action Notes", "fieldname": "action_notes", "fieldtype": "Small Text", "width": 220},
	]
