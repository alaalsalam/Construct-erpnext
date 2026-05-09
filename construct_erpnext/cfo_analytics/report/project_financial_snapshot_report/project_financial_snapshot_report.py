import frappe
from frappe import _


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	conditions = ["1=1"]
	values = {}
	if filters.get("project"):
		conditions.append("project = %(project)s")
		values["project"] = filters["project"]
	if filters.get("snapshot_date"):
		conditions.append("snapshot_date = %(snapshot_date)s")
		values["snapshot_date"] = filters["snapshot_date"]
	data = frappe.db.sql(
		f"""
		SELECT project, boq_total_amount, committed_amount, procurement_invoiced_amount,
			consumed_amount, measured_amount, certified_gross_amount, certified_net_amount,
			retention_held_amount, contractor_outstanding_amount,
			budget_vs_committed_variance, budget_vs_invoiced_variance,
			certification_progress_percent, cost_risk_status, overall_status
		FROM `tabProject Financial Snapshot`
		WHERE {" AND ".join(conditions)}
		ORDER BY snapshot_date DESC, creation DESC
		""",
		values,
		as_dict=True,
	)
	return columns, data


def get_columns():
	return [
		{"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 160},
		{"label": _("BOQ Total"), "fieldname": "boq_total_amount", "fieldtype": "Currency", "width": 120},
		{"label": _("Committed Amount"), "fieldname": "committed_amount", "fieldtype": "Currency", "width": 140},
		{"label": _("Invoiced Amount"), "fieldname": "procurement_invoiced_amount", "fieldtype": "Currency", "width": 140},
		{"label": _("Consumed Amount"), "fieldname": "consumed_amount", "fieldtype": "Currency", "width": 140},
		{"label": _("Measured Amount"), "fieldname": "measured_amount", "fieldtype": "Currency", "width": 140},
		{"label": _("Certified Gross"), "fieldname": "certified_gross_amount", "fieldtype": "Currency", "width": 130},
		{"label": _("Certified Net"), "fieldname": "certified_net_amount", "fieldtype": "Currency", "width": 130},
		{"label": _("Retention Held"), "fieldname": "retention_held_amount", "fieldtype": "Currency", "width": 130},
		{"label": _("Contractor Outstanding"), "fieldname": "contractor_outstanding_amount", "fieldtype": "Currency", "width": 160},
		{"label": _("Budget vs Committed Variance"), "fieldname": "budget_vs_committed_variance", "fieldtype": "Currency", "width": 190},
		{"label": _("Budget vs Invoiced Variance"), "fieldname": "budget_vs_invoiced_variance", "fieldtype": "Currency", "width": 180},
		{"label": _("Certification Progress %"), "fieldname": "certification_progress_percent", "fieldtype": "Percent", "width": 160},
		{"label": _("Cost Risk"), "fieldname": "cost_risk_status", "fieldtype": "Data", "width": 100},
		{"label": _("Overall Status"), "fieldname": "overall_status", "fieldtype": "Data", "width": 120},
	]
