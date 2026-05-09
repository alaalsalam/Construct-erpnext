import frappe
from frappe import _


def execute(filters=None):
	filters = filters or {}
	columns = [
		{"label": _("Contractor"), "fieldname": "contractor", "fieldtype": "Link", "options": "Supplier", "width": 170},
		{"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 160},
		{"label": _("Advance Date"), "fieldname": "advance_date", "fieldtype": "Date", "width": 110},
		{"label": _("Advance Amount"), "fieldname": "advance_amount", "fieldtype": "Currency", "width": 130},
		{"label": _("Recovered Amount"), "fieldname": "recovered_amount", "fieldtype": "Currency", "width": 140},
		{"label": _("Outstanding Advance"), "fieldname": "outstanding_advance_amount", "fieldtype": "Currency", "width": 150},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 120},
		{"label": _("Payment Entry"), "fieldname": "payment_entry", "fieldtype": "Link", "options": "Payment Entry", "width": 160},
	]
	conditions = ["1=1"]
	values = {}
	for field in ("project", "contractor", "status"):
		if filters.get(field):
			conditions.append(f"{field} = %({field})s")
			values[field] = filters[field]

	data = frappe.db.sql(
		f"""
		SELECT contractor, project, advance_date, advance_amount, recovered_amount,
			outstanding_advance_amount, status, payment_entry
		FROM `tabAdvance Register`
		WHERE {" AND ".join(conditions)}
		ORDER BY advance_date DESC, creation DESC
		""",
		values,
		as_dict=True,
	)
	return columns, data
