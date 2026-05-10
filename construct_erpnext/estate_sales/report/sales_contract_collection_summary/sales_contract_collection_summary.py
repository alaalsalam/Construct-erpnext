import frappe
from frappe import _


def execute(filters=None):
	return get_columns(), get_data(filters or {})


def get_columns():
	return [
		{"fieldname": "project", "fieldtype": "Data", "label": _("Project"), "width": 180},
		{"fieldname": "contract_count", "fieldtype": "Int", "label": _("Contract Count"), "width": 120},
		{"fieldname": "contracted_sales_value", "fieldtype": "Currency", "label": _("Contracted Sales Value"), "width": 170},
		{"fieldname": "invoiced_amount", "fieldtype": "Currency", "label": _("Invoiced Amount"), "width": 140},
		{"fieldname": "collected_amount", "fieldtype": "Currency", "label": _("Collected Amount"), "width": 140},
		{"fieldname": "outstanding_amount", "fieldtype": "Currency", "label": _("Outstanding Amount"), "width": 150},
		{"fieldname": "overdue_amount", "fieldtype": "Currency", "label": _("Overdue Amount"), "width": 140},
	]


def get_data(filters):
	conditions, values = get_conditions(filters)
	return frappe.db.sql(
		f"""
		SELECT
			COALESCE(rp.project_name_ar, sc.real_estate_project, sc.project) AS project,
			COUNT(DISTINCT sc.name) AS contract_count,
			SUM(sc.net_price) AS contracted_sales_value,
			SUM(sc.total_invoiced_amount) AS invoiced_amount,
			SUM(sc.total_collected_amount) AS collected_amount,
			SUM(sc.total_outstanding_amount) AS outstanding_amount,
			SUM(CASE WHEN sc.collection_status = 'Overdue' THEN sc.total_outstanding_amount ELSE 0 END) AS overdue_amount
		FROM `tabSales Contract` sc
		LEFT JOIN `tabReal Estate Project` rp ON rp.name = sc.real_estate_project
		WHERE sc.docstatus < 2
		  {conditions}
		GROUP BY COALESCE(rp.project_name_ar, sc.real_estate_project, sc.project)
		ORDER BY project
		""",
		values,
		as_dict=1,
	)


def get_conditions(filters):
	conditions = []
	values = {}
	if filters.get("real_estate_project"):
		conditions.append("sc.real_estate_project = %(real_estate_project)s")
		values["real_estate_project"] = filters["real_estate_project"]
	if filters.get("from_date"):
		conditions.append("sc.contract_date >= %(from_date)s")
		values["from_date"] = filters["from_date"]
	if filters.get("to_date"):
		conditions.append("sc.contract_date <= %(to_date)s")
		values["to_date"] = filters["to_date"]
	return (" AND " + " AND ".join(conditions)) if conditions else "", values
