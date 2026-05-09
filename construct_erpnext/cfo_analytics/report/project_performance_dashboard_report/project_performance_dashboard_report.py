import frappe
from frappe import _

from construct_erpnext.cfo_analytics.evm_metrics import get_evm_metrics
from construct_erpnext.cfo_analytics.project_financials import get_project_financial_snapshot


def execute(filters=None):
	filters = filters or {}
	columns = [
		{"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 150},
		{"label": _("BOQ Total"), "fieldname": "boq_total_amount", "fieldtype": "Currency", "width": 120},
		{"label": _("Certified Value"), "fieldname": "certified_gross_amount", "fieldtype": "Currency", "width": 130},
		{"label": _("Actual Cost"), "fieldname": "actual_cost", "fieldtype": "Currency", "width": 120},
		{"label": _("Planned Value"), "fieldname": "planned_value", "fieldtype": "Currency", "width": 120},
		{"label": _("Cost Variance"), "fieldname": "cost_variance", "fieldtype": "Currency", "width": 120},
		{"label": _("Schedule Variance"), "fieldname": "schedule_variance", "fieldtype": "Currency", "width": 140},
		{"label": _("CPI"), "fieldname": "cost_performance_index", "fieldtype": "Float", "width": 80},
		{"label": _("SPI"), "fieldname": "schedule_performance_index", "fieldtype": "Float", "width": 80},
		{"label": _("Cash Risk"), "fieldname": "cash_risk_status", "fieldtype": "Data", "width": 100},
		{"label": _("EVM Risk"), "fieldname": "overall_evm_status", "fieldtype": "Data", "width": 110},
		{"label": _("Overall Recommendation"), "fieldname": "recommendations", "fieldtype": "Data", "width": 300},
	]
	projects = [filters.project] if filters.get("project") else frappe.get_all("Project", pluck="name")
	data = []
	for project in projects:
		financial = get_project_financial_snapshot(project)
		evm = frappe.db.get_value(
			"Project EVM Metrics",
			{"project": project, "status": ["!=", "Archived"]},
			[
				"actual_cost",
				"planned_value",
				"cost_variance",
				"schedule_variance",
				"cost_performance_index",
				"schedule_performance_index",
				"overall_evm_status",
				"recommendations",
			],
			as_dict=True,
			order_by="calculation_date desc, creation desc",
		)
		if not evm:
			evm = get_evm_metrics(project, planned_progress_percent=financial.get("measurement_progress_percent"))
		data.append(
			{
				"project": project,
				"boq_total_amount": financial.get("boq_total_amount"),
				"certified_gross_amount": financial.get("certified_gross_amount"),
				"actual_cost": evm.get("actual_cost"),
				"planned_value": evm.get("planned_value"),
				"cost_variance": evm.get("cost_variance"),
				"schedule_variance": evm.get("schedule_variance"),
				"cost_performance_index": evm.get("cost_performance_index"),
				"schedule_performance_index": evm.get("schedule_performance_index"),
				"cash_risk_status": financial.get("cash_risk_status"),
				"overall_evm_status": evm.get("overall_evm_status"),
				"recommendations": evm.get("recommendations"),
			}
		)
	return columns, data
