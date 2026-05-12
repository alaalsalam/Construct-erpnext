import frappe
from frappe import _
from construct_erpnext.reporting.report_utils import sum_field, summary_value, report_dashboard_message


def execute(filters=None):
	filters = filters or {}
	columns = [
		{"label": _("Contractor"), "fieldname": "contractor", "fieldtype": "Link", "options": "Supplier", "width": 170},
		{"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 170},
		{"label": _("Total Certified"), "fieldname": "total_certified_amount", "fieldtype": "Currency", "width": 140},
		{"label": _("Total Retention Held"), "fieldname": "total_retention_held", "fieldtype": "Currency", "width": 150},
		{"label": _("Total Advance Paid"), "fieldname": "total_advance_paid", "fieldtype": "Currency", "width": 140},
		{"label": _("Total Advance Recovered"), "fieldname": "total_advance_recovered", "fieldtype": "Currency", "width": 170},
		{"label": _("Total Deductions"), "fieldname": "total_deductions", "fieldtype": "Currency", "width": 140},
		{"label": _("Total Invoiced"), "fieldname": "total_invoiced_amount", "fieldtype": "Currency", "width": 140},
		{"label": _("Total Paid"), "fieldname": "total_paid_amount", "fieldtype": "Currency", "width": 130},
		{"label": _("Outstanding Balance"), "fieldname": "outstanding_balance", "fieldtype": "Currency", "width": 150},
		{"label": _("Active Guarantees"), "fieldname": "active_guarantees", "fieldtype": "Int", "width": 130},
		{"label": _("Expiring Guarantees"), "fieldname": "expiring_guarantees", "fieldtype": "Int", "width": 140},
	]
	conditions = ["ca.status != 'Closed'"]
	values = {}
	for field in ("project", "contractor"):
		if filters.get(field):
			conditions.append(f"ca.{field} = %({field})s")
			values[field] = filters[field]

	data = frappe.db.sql(
		f"""
		SELECT
			ca.contractor,
			ca.project,
			ca.total_certified_amount,
			ca.total_retention_held,
			ca.total_advance_paid,
			ca.total_advance_recovered,
			ca.total_deductions,
			ca.total_invoiced_amount,
			ca.total_paid_amount,
			ca.outstanding_balance,
			(
				SELECT COUNT(*)
				FROM `tabGuarantee Register` gr
				WHERE gr.contractor_account = ca.name AND gr.status = 'Active'
			) AS active_guarantees,
			(
				SELECT COUNT(*)
				FROM `tabGuarantee Register` gr
				WHERE gr.contractor_account = ca.name AND gr.status = 'Expiring Soon'
			) AS expiring_guarantees
		FROM `tabContractor Account` ca
		WHERE {" AND ".join(conditions)}
		ORDER BY ca.project, ca.contractor
		""",
		values,
		as_dict=True,
	)
	return columns, data, report_dashboard_message(get_report_summary(data)), None, None, False


def get_report_summary(data):
	return [
		summary_value("Total Certified", sum_field(data, "total_certified_amount"), "Currency", "Blue"),
		summary_value("Total Retention", sum_field(data, "total_retention_held"), "Currency", "Orange"),
		summary_value("Total Paid", sum_field(data, "total_paid_amount"), "Currency", "Green"),
		summary_value("Outstanding Balance", sum_field(data, "outstanding_balance"), "Currency", "Red"),
	]
