import frappe
from frappe import _
from construct_erpnext.reporting.report_utils import sum_field, summary_value


def execute(filters=None):
	filters = filters or {}
	columns = [
		{"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 150},
		{"label": _("Date"), "fieldname": "calculation_date", "fieldtype": "Date", "width": 110},
		{"label": _("BAC"), "fieldname": "budget_at_completion", "fieldtype": "Currency", "width": 110},
		{"label": _("EV"), "fieldname": "earned_value", "fieldtype": "Currency", "width": 110},
		{"label": _("AC"), "fieldname": "actual_cost", "fieldtype": "Currency", "width": 110},
		{"label": _("PV"), "fieldname": "planned_value", "fieldtype": "Currency", "width": 110},
		{"label": _("CV"), "fieldname": "cost_variance", "fieldtype": "Currency", "width": 110},
		{"label": _("SV"), "fieldname": "schedule_variance", "fieldtype": "Currency", "width": 110},
		{"label": _("CPI"), "fieldname": "cost_performance_index", "fieldtype": "Float", "width": 80},
		{"label": _("SPI"), "fieldname": "schedule_performance_index", "fieldtype": "Float", "width": 80},
		{"label": _("EAC"), "fieldname": "estimate_at_completion", "fieldtype": "Currency", "width": 110},
		{"label": _("ETC"), "fieldname": "estimate_to_complete", "fieldtype": "Currency", "width": 110},
		{"label": _("VAC"), "fieldname": "variance_at_completion", "fieldtype": "Currency", "width": 110},
		{"label": _("TCPI"), "fieldname": "to_complete_performance_index", "fieldtype": "Float", "width": 90},
		{"label": _("Actual Progress %"), "fieldname": "actual_progress_percent", "fieldtype": "Percent", "width": 130},
		{"label": _("Planned Progress %"), "fieldname": "planned_progress_percent", "fieldtype": "Percent", "width": 140},
		{"label": _("Cost Status"), "fieldname": "cost_status", "fieldtype": "Data", "width": 100},
		{"label": _("Schedule Status"), "fieldname": "schedule_status", "fieldtype": "Data", "width": 120},
		{"label": _("Overall Status"), "fieldname": "overall_evm_status", "fieldtype": "Data", "width": 120},
	]
	conditions = ["1=1"]
	values = {}
	for field in ("project", "status"):
		if filters.get(field):
			conditions.append(f"{field} = %({field})s")
			values[field] = filters[field]
	if filters.get("calculation_date"):
		conditions.append("calculation_date = %(calculation_date)s")
		values["calculation_date"] = filters["calculation_date"]
	data = frappe.db.sql(
		f"""
		SELECT project, calculation_date, budget_at_completion, earned_value, actual_cost,
			planned_value, cost_variance, schedule_variance, cost_performance_index,
			schedule_performance_index, estimate_at_completion, estimate_to_complete,
			variance_at_completion, to_complete_performance_index, actual_progress_percent,
			planned_progress_percent, cost_status, schedule_status, overall_evm_status
		FROM `tabProject EVM Metrics`
		WHERE {" AND ".join(conditions)}
		ORDER BY calculation_date DESC, creation DESC
		""",
		values,
		as_dict=True,
	)
	return columns, data, None, None, None, False


def get_report_summary(data):
	latest = data[0] if data else {}
	return [
		summary_value("BAC", sum_field(data, "budget_at_completion"), "Currency", "Blue"),
		summary_value("EV", sum_field(data, "earned_value"), "Currency", "Green"),
		summary_value("AC", sum_field(data, "actual_cost"), "Currency", "Orange"),
		summary_value("CPI", latest.get("cost_performance_index") or 0, "Float", "Green" if (latest.get("cost_performance_index") or 0) >= 1 else "Red"),
		summary_value("SPI", latest.get("schedule_performance_index") or 0, "Float", "Green" if (latest.get("schedule_performance_index") or 0) >= 1 else "Orange"),
		summary_value("Overall EVM Status", latest.get("overall_evm_status") or "N/A", "Data", "Green" if latest.get("overall_evm_status") == "On Track" else "Red"),
	]
