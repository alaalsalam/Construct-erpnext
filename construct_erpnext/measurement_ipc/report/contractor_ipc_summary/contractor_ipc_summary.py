import frappe
from frappe import _


def execute(filters=None):
	filters = filters or {}
	columns = [
		{"label": _("Contractor"), "fieldname": "contractor", "fieldtype": "Link", "options": "Supplier", "width": 180},
		{"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 160},
		{"label": _("IPC Count"), "fieldname": "ipc_count", "fieldtype": "Int", "width": 100},
		{"label": _("Gross Amount"), "fieldname": "gross_amount", "fieldtype": "Currency", "width": 130},
		{"label": _("Retention Held"), "fieldname": "retention_held", "fieldtype": "Currency", "width": 130},
		{"label": _("Deductions"), "fieldname": "deductions", "fieldtype": "Currency", "width": 120},
		{"label": _("Net Payable"), "fieldname": "net_payable", "fieldtype": "Currency", "width": 130},
		{"label": _("Invoiced Amount"), "fieldname": "invoiced_amount", "fieldtype": "Currency", "width": 130},
		{"label": _("Paid Amount"), "fieldname": "paid_amount", "fieldtype": "Currency", "width": 130},
		{"label": _("Outstanding Amount"), "fieldname": "outstanding_amount", "fieldtype": "Currency", "width": 140},
	]
	conditions = ["docstatus != 2"]
	values = {}
	if filters.get("contractor"):
		conditions.append("contractor = %(contractor)s")
		values["contractor"] = filters["contractor"]
	if filters.get("project"):
		conditions.append("project = %(project)s")
		values["project"] = filters["project"]
	if filters.get("from_date"):
		conditions.append("period_start >= %(from_date)s")
		values["from_date"] = filters["from_date"]
	if filters.get("to_date"):
		conditions.append("period_end <= %(to_date)s")
		values["to_date"] = filters["to_date"]
	data = frappe.db.sql(
		f"""
		SELECT contractor, project, COUNT(name) AS ipc_count,
			SUM(gross_amount) AS gross_amount,
			SUM(retention_amount) AS retention_held,
			SUM(advance_recovery_amount + penalty_amount + withholding_tax_amount + other_deduction_amount) AS deductions,
			SUM(net_payable) AS net_payable,
			SUM(CASE WHEN purchase_invoice IS NOT NULL AND purchase_invoice != '' THEN net_payable ELSE 0 END) AS invoiced_amount,
			SUM(paid_amount) AS paid_amount,
			SUM(outstanding_amount) AS outstanding_amount
		FROM `tabInterim Payment Certificate`
		WHERE {" AND ".join(conditions)}
		GROUP BY contractor, project
		ORDER BY contractor, project
		""",
		values,
		as_dict=True,
	)
	return columns, data
