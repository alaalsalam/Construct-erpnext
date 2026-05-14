import frappe


def execute(filters=None):
	filters = filters or {}
	conditions = {}
	if filters.get("access_type"):
		conditions["access_type"] = filters.get("access_type")
	data = frappe.get_all("Portal Access Profile", filters=conditions, fields=["name as profile", "access_type", "party_type", "party", "status", "unit", "sales_contract", "lease_contract", "contractor_agreement"], order_by="modified desc")
	return _columns(), data


def _columns():
	return [
		{"label": "Profile", "fieldname": "profile", "fieldtype": "Link", "options": "Portal Access Profile", "width": 150},
		{"label": "Access Type", "fieldname": "access_type", "fieldtype": "Data", "width": 110},
		{"label": "Party Type", "fieldname": "party_type", "fieldtype": "Data", "width": 120},
		{"label": "Party", "fieldname": "party", "fieldtype": "Dynamic Link", "options": "party_type", "width": 170},
		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 130},
		{"label": "Unit", "fieldname": "unit", "fieldtype": "Link", "options": "Unit", "width": 130},
		{"label": "Sales Contract", "fieldname": "sales_contract", "fieldtype": "Link", "options": "Sales Contract", "width": 150},
		{"label": "Lease Contract", "fieldname": "lease_contract", "fieldtype": "Link", "options": "Lease Contract", "width": 150},
		{"label": "Contractor Agreement", "fieldname": "contractor_agreement", "fieldtype": "Link", "options": "Subcontract", "width": 160},
	]
