import frappe
from frappe import _

from construct_erpnext.cfo_analytics.project_financials import get_project_financial_snapshot


def execute(filters=None):
	filters = filters or {}
	columns = [
		{"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 160},
		{"label": _("BOQ Total"), "fieldname": "boq_total_amount", "fieldtype": "Currency", "width": 120},
		{"label": _("Committed"), "fieldname": "committed_amount", "fieldtype": "Currency", "width": 120},
		{"label": _("Invoiced"), "fieldname": "procurement_invoiced_amount", "fieldtype": "Currency", "width": 120},
		{"label": _("Measured"), "fieldname": "measured_amount", "fieldtype": "Currency", "width": 120},
		{"label": _("Certified"), "fieldname": "certified_gross_amount", "fieldtype": "Currency", "width": 120},
		{"label": _("Retention"), "fieldname": "retention_held_amount", "fieldtype": "Currency", "width": 120},
		{"label": _("Paid"), "fieldname": "contractor_paid_amount", "fieldtype": "Currency", "width": 120},
		{"label": _("Outstanding"), "fieldname": "contractor_outstanding_amount", "fieldtype": "Currency", "width": 130},
		{"label": _("Risk"), "fieldname": "cost_risk_status", "fieldtype": "Data", "width": 90},
		{"label": _("Recommendation"), "fieldname": "recommendations", "fieldtype": "Data", "width": 280},
	]
	projects = [filters.project] if filters.get("project") else frappe.get_all("Project", pluck="name")
	data = []
	for project in projects:
		row = get_project_financial_snapshot(project)
		if filters.get("risk_status") and row.get("cost_risk_status") != filters.get("risk_status"):
			continue
		data.append(row)
	return columns, data
