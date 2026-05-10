import frappe
from frappe import _


def execute(filters=None):
	return get_columns(), get_data(filters or {})


def get_columns():
	return [
		{"fieldname": "sales_contract", "fieldtype": "Link", "label": _("Sales Contract"), "options": "Sales Contract", "width": 140},
		{"fieldname": "unit", "fieldtype": "Link", "label": _("Unit"), "options": "Unit", "width": 90},
		{"fieldname": "customer", "fieldtype": "Link", "label": _("Customer"), "options": "Customer", "width": 160},
		{"fieldname": "installment_number", "fieldtype": "Data", "label": _("Installment No"), "width": 110},
		{"fieldname": "due_date", "fieldtype": "Date", "label": _("Due Date"), "width": 100},
		{"fieldname": "amount", "fieldtype": "Currency", "label": _("Amount"), "width": 120},
		{"fieldname": "outstanding_amount", "fieldtype": "Currency", "label": _("Outstanding Amount"), "width": 140},
		{"fieldname": "overdue_days", "fieldtype": "Int", "label": _("Overdue Days"), "width": 110},
		{"fieldname": "invoice_status", "fieldtype": "Data", "label": _("Status"), "width": 110},
	]


def get_data(filters):
	conditions, values = get_conditions(filters)
	return frappe.db.sql(
		f"""
		SELECT
			sc.name AS sales_contract,
			sc.unit,
			sc.customer,
			sis.installment_number,
			sis.due_date,
			sis.amount,
			COALESCE(sis.outstanding_amount, sis.amount) AS outstanding_amount,
			sis.overdue_days,
			COALESCE(sis.invoice_status, sis.installment_status) AS invoice_status
		FROM `tabSales Installment Schedule` sis
		INNER JOIN `tabSales Contract` sc ON sc.name = sis.parent
		WHERE sis.parenttype = 'Sales Contract'
		  AND sc.docstatus < 2
		  AND (sis.invoice_status = 'Overdue' OR sis.installment_status = 'Overdue' OR sis.overdue_days > 0)
		  {conditions}
		ORDER BY sis.overdue_days DESC, sis.due_date ASC
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
	if filters.get("customer"):
		conditions.append("sc.customer = %(customer)s")
		values["customer"] = filters["customer"]
	if filters.get("overdue_days_min"):
		conditions.append("sis.overdue_days >= %(overdue_days_min)s")
		values["overdue_days_min"] = filters["overdue_days_min"]
	return (" AND " + " AND ".join(conditions)) if conditions else "", values
