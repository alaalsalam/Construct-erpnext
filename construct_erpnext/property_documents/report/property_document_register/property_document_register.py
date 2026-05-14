import frappe


def execute(filters=None):
	filters = filters or {}
	conditions = {}
	for field in ("real_estate_project", "document_type"):
		if filters.get(field):
			conditions[field] = filters.get(field)
	data = frappe.get_all("Property Document", filters=conditions, fields=["name as property_document", "document_type", "document_title", "real_estate_project", "unit", "document_date", "expiry_date", "status"], order_by="modified desc")
	return _columns(), data


def _columns():
	return [
		{"label": "Property Document", "fieldname": "property_document", "fieldtype": "Link", "options": "Property Document", "width": 150},
		{"label": "Document Type", "fieldname": "document_type", "fieldtype": "Data", "width": 120},
		{"label": "Document Title", "fieldname": "document_title", "fieldtype": "Data", "width": 220},
		{"label": "Real Estate Project", "fieldname": "real_estate_project", "fieldtype": "Link", "options": "Real Estate Project", "width": 160},
		{"label": "Unit", "fieldname": "unit", "fieldtype": "Link", "options": "Unit", "width": 130},
		{"label": "Document Date", "fieldname": "document_date", "fieldtype": "Date", "width": 120},
		{"label": "Expiry Date", "fieldname": "expiry_date", "fieldtype": "Date", "width": 120},
		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 110},
	]
