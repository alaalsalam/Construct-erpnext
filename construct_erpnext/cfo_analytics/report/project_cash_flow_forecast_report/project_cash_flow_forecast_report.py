import frappe
from frappe import _


def execute(filters=None):
	filters = filters or {}
	columns = [
		{"label": _("Period"), "fieldname": "period_label", "fieldtype": "Data", "width": 190},
		{"label": _("Expected Inflow"), "fieldname": "total_inflow", "fieldtype": "Currency", "width": 130},
		{"label": _("Purchase Order Outflow"), "fieldname": "purchase_order_outflow", "fieldtype": "Currency", "width": 160},
		{"label": _("Purchase Invoice Outflow"), "fieldname": "purchase_invoice_outflow", "fieldtype": "Currency", "width": 170},
		{"label": _("IPC Outflow"), "fieldname": "ipc_outflow", "fieldtype": "Currency", "width": 120},
		{"label": _("Retention Release"), "fieldname": "retention_release_outflow", "fieldtype": "Currency", "width": 140},
		{"label": _("Total Outflow"), "fieldname": "total_outflow", "fieldtype": "Currency", "width": 130},
		{"label": _("Net Cash Flow"), "fieldname": "net_cash_flow", "fieldtype": "Currency", "width": 130},
		{"label": _("Running Balance"), "fieldname": "running_balance", "fieldtype": "Currency", "width": 140},
		{"label": _("Risk"), "fieldname": "risk", "fieldtype": "Data", "width": 90},
	]
	conditions = ["1=1"]
	values = {}
	if filters.get("forecast"):
		conditions.append("f.name = %(forecast)s")
		values["forecast"] = filters["forecast"]
	if filters.get("project"):
		conditions.append("f.project = %(project)s")
		values["project"] = filters["project"]
	if filters.get("period_type"):
		conditions.append("f.period_type = %(period_type)s")
		values["period_type"] = filters["period_type"]
	if filters.get("start_date"):
		conditions.append("p.period_start >= %(start_date)s")
		values["start_date"] = filters["start_date"]
	if filters.get("end_date"):
		conditions.append("p.period_end <= %(end_date)s")
		values["end_date"] = filters["end_date"]
	data = frappe.db.sql(
		f"""
		SELECT p.period_label, p.total_inflow, p.purchase_order_outflow, p.purchase_invoice_outflow,
			p.ipc_outflow, p.retention_release_outflow, p.total_outflow, p.net_cash_flow,
			p.running_balance, IF(p.cash_deficit = 1, 'Red', f.cash_risk_status) AS risk
		FROM `tabProject Cash Flow Forecast Period` p
		INNER JOIN `tabProject Cash Flow Forecast` f ON f.name = p.parent
		WHERE {" AND ".join(conditions)}
		ORDER BY f.creation DESC, p.period_start ASC
		""",
		values,
		as_dict=True,
	)
	return columns, data
