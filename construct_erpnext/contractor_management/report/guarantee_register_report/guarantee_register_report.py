import frappe
from frappe import _


def execute(filters=None):
	filters = filters or {}
	columns = [
		{"label": _("Contractor"), "fieldname": "contractor", "fieldtype": "Link", "options": "Supplier", "width": 170},
		{"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 160},
		{"label": _("Guarantee Type"), "fieldname": "guarantee_type", "fieldtype": "Data", "width": 170},
		{"label": _("Guarantee Number"), "fieldname": "guarantee_number", "fieldtype": "Data", "width": 150},
		{"label": _("Bank"), "fieldname": "issuing_bank", "fieldtype": "Data", "width": 160},
		{"label": _("Amount"), "fieldname": "guarantee_amount", "fieldtype": "Currency", "width": 130},
		{"label": _("Issue Date"), "fieldname": "issue_date", "fieldtype": "Date", "width": 110},
		{"label": _("Expiry Date"), "fieldname": "expiry_date", "fieldtype": "Date", "width": 110},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 120},
		{"label": _("Alert Before Days"), "fieldname": "alert_before_days", "fieldtype": "Int", "width": 130},
	]
	conditions = ["1=1"]
	values = {}
	for field in ("project", "contractor", "status"):
		if filters.get(field):
			conditions.append(f"{field} = %({field})s")
			values[field] = filters[field]
	if filters.get("expiry_from"):
		conditions.append("expiry_date >= %(expiry_from)s")
		values["expiry_from"] = filters["expiry_from"]
	if filters.get("expiry_to"):
		conditions.append("expiry_date <= %(expiry_to)s")
		values["expiry_to"] = filters["expiry_to"]

	data = frappe.db.sql(
		f"""
		SELECT contractor, project, guarantee_type, guarantee_number, issuing_bank,
			guarantee_amount, issue_date, expiry_date, status, alert_before_days
		FROM `tabGuarantee Register`
		WHERE {" AND ".join(conditions)}
		ORDER BY expiry_date ASC, creation DESC
		""",
		values,
		as_dict=True,
	)
	return columns, data
