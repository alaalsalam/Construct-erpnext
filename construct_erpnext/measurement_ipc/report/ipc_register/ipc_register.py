import frappe
from frappe import _
from construct_erpnext.reporting.report_utils import sum_field, summary_value


def execute(filters=None):
	filters = filters or {}
	columns = [
		{"label": _("IPC"), "fieldname": "name", "fieldtype": "Link", "options": "Interim Payment Certificate", "width": 160},
		{"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 160},
		{"label": _("Contractor"), "fieldname": "contractor", "fieldtype": "Link", "options": "Supplier", "width": 180},
		{"label": _("Period Start"), "fieldname": "period_start", "fieldtype": "Date", "width": 110},
		{"label": _("Period End"), "fieldname": "period_end", "fieldtype": "Date", "width": 110},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 120},
		{"label": _("Gross Amount"), "fieldname": "gross_amount", "fieldtype": "Currency", "width": 130},
		{"label": _("Retention Amount"), "fieldname": "retention_amount", "fieldtype": "Currency", "width": 130},
		{"label": _("Advance Recovery"), "fieldname": "advance_recovery_amount", "fieldtype": "Currency", "width": 130},
		{"label": _("Penalties"), "fieldname": "penalty_amount", "fieldtype": "Currency", "width": 120},
		{"label": _("Net Payable"), "fieldname": "net_payable", "fieldtype": "Currency", "width": 130},
		{"label": _("Purchase Invoice"), "fieldname": "purchase_invoice", "fieldtype": "Link", "options": "Purchase Invoice", "width": 160},
		{"label": _("Paid Amount"), "fieldname": "paid_amount", "fieldtype": "Currency", "width": 130},
		{"label": _("Outstanding Amount"), "fieldname": "outstanding_amount", "fieldtype": "Currency", "width": 140},
	]
	conditions = ["1=1"]
	values = {}
	for field in ("project", "contractor", "status"):
		if filters.get(field):
			conditions.append(f"{field} = %({field})s")
			values[field] = filters[field]
	if filters.get("from_date"):
		conditions.append("period_start >= %(from_date)s")
		values["from_date"] = filters["from_date"]
	if filters.get("to_date"):
		conditions.append("period_end <= %(to_date)s")
		values["to_date"] = filters["to_date"]
	data = frappe.db.sql(
		f"""
		SELECT name, project, contractor, period_start, period_end, status, gross_amount,
			retention_amount, advance_recovery_amount, penalty_amount, net_payable,
			purchase_invoice, paid_amount, outstanding_amount
		FROM `tabInterim Payment Certificate`
		WHERE {" AND ".join(conditions)}
		ORDER BY period_end DESC, modified DESC
		""",
		values,
		as_dict=True,
	)
	return columns, data, None, None, get_report_summary(data), False


def get_report_summary(data):
	return [
		summary_value("Gross Amount", sum_field(data, "gross_amount"), "Currency", "Blue"),
		summary_value("Retention Held", sum_field(data, "retention_amount"), "Currency", "Orange"),
		summary_value("Net Payable", sum_field(data, "net_payable"), "Currency", "Green"),
		summary_value("IPC Count", len(data or []), "Int", "Blue"),
	]
