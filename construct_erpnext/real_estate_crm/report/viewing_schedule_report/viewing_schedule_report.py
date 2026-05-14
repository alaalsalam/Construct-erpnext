import frappe


def execute(filters=None):
	filters = filters or {}
	conditions = {}
	if filters.get("status"):
		conditions["status"] = filters.get("status")
	if filters.get("from_date") or filters.get("to_date"):
		conditions["appointment_date"] = ["between", [filters.get("from_date") or "1900-01-01", filters.get("to_date") or "2999-12-31"]]
	data = frappe.get_all(
		"Viewing Appointment",
		filters=conditions,
		fields=["name as appointment", "requirement", "unit", "appointment_date", "status", "lead", "customer", "assigned_to", "feedback"],
		order_by="appointment_date desc",
	)
	return [
		{"label": "Appointment", "fieldname": "appointment", "fieldtype": "Link", "options": "Viewing Appointment", "width": 150},
		{"label": "Customer Requirement", "fieldname": "requirement", "fieldtype": "Link", "options": "Customer Requirement", "width": 170},
		{"label": "Unit", "fieldname": "unit", "fieldtype": "Link", "options": "Unit", "width": 130},
		{"label": "Appointment Date", "fieldname": "appointment_date", "fieldtype": "Datetime", "width": 160},
		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 110},
		{"label": "Lead", "fieldname": "lead", "fieldtype": "Link", "options": "Lead", "width": 140},
		{"label": "Customer", "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 160},
		{"label": "Assigned To", "fieldname": "assigned_to", "fieldtype": "Link", "options": "User", "width": 140},
		{"label": "Feedback", "fieldname": "feedback", "fieldtype": "Data", "width": 220},
	], data
