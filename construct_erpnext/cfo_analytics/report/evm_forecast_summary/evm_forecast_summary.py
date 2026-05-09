import frappe
from frappe import _


def execute(filters=None):
	filters = filters or {}
	columns = [
		{"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 150},
		{"label": _("Latest Date"), "fieldname": "calculation_date", "fieldtype": "Date", "width": 110},
		{"label": _("BAC"), "fieldname": "budget_at_completion", "fieldtype": "Currency", "width": 110},
		{"label": _("EV"), "fieldname": "earned_value", "fieldtype": "Currency", "width": 110},
		{"label": _("AC"), "fieldname": "actual_cost", "fieldtype": "Currency", "width": 110},
		{"label": _("EAC"), "fieldname": "estimate_at_completion", "fieldtype": "Currency", "width": 110},
		{"label": _("ETC"), "fieldname": "estimate_to_complete", "fieldtype": "Currency", "width": 110},
		{"label": _("VAC"), "fieldname": "variance_at_completion", "fieldtype": "Currency", "width": 110},
		{"label": _("Forecast Overrun"), "fieldname": "forecast_overrun_amount", "fieldtype": "Currency", "width": 140},
		{"label": _("CPI"), "fieldname": "cost_performance_index", "fieldtype": "Float", "width": 80},
		{"label": _("SPI"), "fieldname": "schedule_performance_index", "fieldtype": "Float", "width": 80},
		{"label": _("Overall Status"), "fieldname": "overall_evm_status", "fieldtype": "Data", "width": 120},
		{"label": _("Recommendation"), "fieldname": "recommendations", "fieldtype": "Data", "width": 280},
	]
	conditions = ["1=1"]
	values = {}
	if filters.get("project"):
		conditions.append("project = %(project)s")
		values["project"] = filters["project"]
	if filters.get("from_date"):
		conditions.append("calculation_date >= %(from_date)s")
		values["from_date"] = filters["from_date"]
	if filters.get("to_date"):
		conditions.append("calculation_date <= %(to_date)s")
		values["to_date"] = filters["to_date"]
	if filters.get("overall_status"):
		conditions.append("overall_evm_status = %(overall_status)s")
		values["overall_status"] = filters["overall_status"]
	data = frappe.db.sql(
		f"""
		SELECT project, calculation_date, budget_at_completion, earned_value, actual_cost,
			estimate_at_completion, estimate_to_complete, variance_at_completion,
			forecast_overrun_amount, cost_performance_index, schedule_performance_index,
			overall_evm_status, recommendations
		FROM `tabProject EVM Metrics`
		WHERE {" AND ".join(conditions)}
		ORDER BY calculation_date DESC, creation DESC
		""",
		values,
		as_dict=True,
	)
	return columns, data
