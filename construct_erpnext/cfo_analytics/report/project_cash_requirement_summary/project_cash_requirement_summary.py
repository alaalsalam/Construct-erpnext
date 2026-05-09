import frappe
from frappe import _


def execute(filters=None):
	filters = filters or {}
	columns = [
		{"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 160},
		{"label": _("Forecast Period"), "fieldname": "period", "fieldtype": "Data", "width": 190},
		{"label": _("Total Inflow"), "fieldname": "total_expected_inflow", "fieldtype": "Currency", "width": 130},
		{"label": _("Total Outflow"), "fieldname": "total_expected_outflow", "fieldtype": "Currency", "width": 130},
		{"label": _("Net Cash Flow"), "fieldname": "net_cash_flow", "fieldtype": "Currency", "width": 130},
		{"label": _("Lowest Balance"), "fieldname": "lowest_projected_balance", "fieldtype": "Currency", "width": 140},
		{"label": _("Deficit"), "fieldname": "cash_deficit_amount", "fieldtype": "Currency", "width": 120},
		{"label": _("Cash Risk"), "fieldname": "cash_risk_status", "fieldtype": "Data", "width": 100},
		{"label": _("Recommendation"), "fieldname": "recommendations", "fieldtype": "Data", "width": 280},
	]
	conditions = ["1=1"]
	values = {}
	if filters.get("project"):
		conditions.append("project = %(project)s")
		values["project"] = filters["project"]
	if filters.get("from_date"):
		conditions.append("start_date >= %(from_date)s")
		values["from_date"] = filters["from_date"]
	if filters.get("to_date"):
		conditions.append("end_date <= %(to_date)s")
		values["to_date"] = filters["to_date"]
	data = frappe.db.sql(
		f"""
		SELECT project, CONCAT(start_date, ' - ', end_date) AS period, total_expected_inflow,
			total_expected_outflow, net_cash_flow, lowest_projected_balance, cash_deficit_amount,
			cash_risk_status, recommendations
		FROM `tabProject Cash Flow Forecast`
		WHERE {" AND ".join(conditions)}
		ORDER BY forecast_date DESC, creation DESC
		""",
		values,
		as_dict=True,
	)
	return columns, data
