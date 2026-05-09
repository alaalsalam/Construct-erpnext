import frappe
from frappe import _


def execute(filters=None):
	filters = filters or {}
	columns = [
		{"label": _("Contractor"), "fieldname": "contractor", "fieldtype": "Link", "options": "Supplier", "width": 170},
		{"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 160},
		{"label": _("IPC"), "fieldname": "ipc", "fieldtype": "Link", "options": "Interim Payment Certificate", "width": 160},
		{"label": _("Retention Amount"), "fieldname": "retention_amount", "fieldtype": "Currency", "width": 140},
		{"label": _("Remaining Retention"), "fieldname": "remaining_retention_amount", "fieldtype": "Currency", "width": 160},
		{"label": _("Release Due Date"), "fieldname": "release_due_date", "fieldtype": "Date", "width": 140},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 120},
	]
	conditions = ["status IN ('Held', 'Eligible for Release', 'Partially Released')"]
	values = {}
	for field in ("project", "contractor"):
		if filters.get(field):
			conditions.append(f"{field} = %({field})s")
			values[field] = filters[field]
	if filters.get("from_date"):
		conditions.append("release_due_date >= %(from_date)s")
		values["from_date"] = filters["from_date"]
	if filters.get("to_date"):
		conditions.append("release_due_date <= %(to_date)s")
		values["to_date"] = filters["to_date"]
	data = frappe.db.sql(
		f"""
		SELECT contractor, project, ipc, retention_amount, remaining_retention_amount,
			release_due_date, status
		FROM `tabRetention Register`
		WHERE {" AND ".join(conditions)}
		ORDER BY release_due_date ASC, creation ASC
		""",
		values,
		as_dict=True,
	)
	return columns, data
