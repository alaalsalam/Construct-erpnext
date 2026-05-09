import frappe
from frappe import _


def execute(filters=None):
	filters = filters or {}
	columns = [
		{"label": _("Contractor"), "fieldname": "contractor", "fieldtype": "Link", "options": "Supplier", "width": 170},
		{"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 160},
		{"label": _("IPC"), "fieldname": "ipc", "fieldtype": "Link", "options": "Interim Payment Certificate", "width": 160},
		{"label": _("Purchase Invoice"), "fieldname": "purchase_invoice", "fieldtype": "Link", "options": "Purchase Invoice", "width": 160},
		{"label": _("Gross Amount"), "fieldname": "gross_amount", "fieldtype": "Currency", "width": 130},
		{"label": _("Retention %"), "fieldname": "retention_percent", "fieldtype": "Percent", "width": 100},
		{"label": _("Retention Amount"), "fieldname": "retention_amount", "fieldtype": "Currency", "width": 130},
		{"label": _("Retained On"), "fieldname": "retained_on", "fieldtype": "Date", "width": 110},
		{"label": _("Release Due Date"), "fieldname": "release_due_date", "fieldtype": "Date", "width": 130},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 120},
		{"label": _("Released Amount"), "fieldname": "released_amount", "fieldtype": "Currency", "width": 130},
		{"label": _("Remaining Amount"), "fieldname": "remaining_retention_amount", "fieldtype": "Currency", "width": 140},
	]
	conditions = ["1=1"]
	values = {}
	for field in ("project", "contractor", "status"):
		if filters.get(field):
			conditions.append(f"{field} = %({field})s")
			values[field] = filters[field]
	if filters.get("from_date"):
		conditions.append("retained_on >= %(from_date)s")
		values["from_date"] = filters["from_date"]
	if filters.get("to_date"):
		conditions.append("retained_on <= %(to_date)s")
		values["to_date"] = filters["to_date"]
	data = frappe.db.sql(f"SELECT * FROM `tabRetention Register` WHERE {' AND '.join(conditions)} ORDER BY retained_on DESC", values, as_dict=True)
	return columns, data
