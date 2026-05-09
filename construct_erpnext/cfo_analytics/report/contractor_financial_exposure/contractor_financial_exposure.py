import frappe
from frappe import _


def execute(filters=None):
	filters = filters or {}
	columns = [
		{"label": _("Contractor"), "fieldname": "contractor", "fieldtype": "Link", "options": "Supplier", "width": 170},
		{"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 160},
		{"label": _("Certified Amount"), "fieldname": "total_certified_amount", "fieldtype": "Currency", "width": 140},
		{"label": _("Retention Held"), "fieldname": "total_retention_held", "fieldtype": "Currency", "width": 130},
		{"label": _("Invoiced Amount"), "fieldname": "total_invoiced_amount", "fieldtype": "Currency", "width": 140},
		{"label": _("Paid Amount"), "fieldname": "total_paid_amount", "fieldtype": "Currency", "width": 120},
		{"label": _("Outstanding Balance"), "fieldname": "outstanding_balance", "fieldtype": "Currency", "width": 150},
		{"label": _("Active Guarantees"), "fieldname": "active_guarantees", "fieldtype": "Int", "width": 130},
		{"label": _("Expiring Guarantees"), "fieldname": "expiring_guarantees", "fieldtype": "Int", "width": 140},
		{"label": _("Risk Status"), "fieldname": "risk_status", "fieldtype": "Data", "width": 110},
	]
	conditions = ["ca.status != 'Closed'"]
	values = {}
	for field in ("project", "contractor"):
		if filters.get(field):
			conditions.append(f"ca.{field} = %({field})s")
			values[field] = filters[field]
	data = frappe.db.sql(
		f"""
		SELECT ca.contractor, ca.project, ca.total_certified_amount, ca.total_retention_held,
			ca.total_invoiced_amount, ca.total_paid_amount, ca.outstanding_balance,
			(SELECT COUNT(*) FROM `tabGuarantee Register` gr WHERE gr.contractor_account = ca.name AND gr.status = 'Active') AS active_guarantees,
			(SELECT COUNT(*) FROM `tabGuarantee Register` gr WHERE gr.contractor_account = ca.name AND gr.status = 'Expiring Soon') AS expiring_guarantees,
			CASE
				WHEN ca.total_certified_amount > 0 AND ca.outstanding_balance > ca.total_certified_amount * 0.75 THEN 'Red'
				WHEN ca.total_certified_amount > 0 AND ca.outstanding_balance > ca.total_certified_amount * 0.4 THEN 'Yellow'
				ELSE 'Green'
			END AS risk_status
		FROM `tabContractor Account` ca
		WHERE {" AND ".join(conditions)}
		ORDER BY ca.project, ca.contractor
		""",
		values,
		as_dict=True,
	)
	return columns, data
