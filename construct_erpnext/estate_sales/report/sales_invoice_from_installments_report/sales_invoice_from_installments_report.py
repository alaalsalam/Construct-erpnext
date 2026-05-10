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
		{"fieldname": "installment_amount", "fieldtype": "Currency", "label": _("Installment Amount"), "width": 130},
		{"fieldname": "sales_invoice", "fieldtype": "Link", "label": _("Sales Invoice"), "options": "Sales Invoice", "width": 140},
		{"fieldname": "invoice_status", "fieldtype": "Data", "label": _("Invoice Status"), "width": 120},
		{"fieldname": "invoice_amount", "fieldtype": "Currency", "label": _("Invoice Amount"), "width": 120},
		{"fieldname": "paid_amount", "fieldtype": "Currency", "label": _("Paid Amount"), "width": 120},
		{"fieldname": "outstanding_amount", "fieldtype": "Currency", "label": _("Outstanding Amount"), "width": 140},
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
			sis.amount AS installment_amount,
			sis.sales_invoice,
			COALESCE(sis.invoice_status, 'Not Invoiced') AS invoice_status,
			sis.invoice_amount,
			sis.paid_amount,
			sis.outstanding_amount
		FROM `tabSales Installment Schedule` sis
		INNER JOIN `tabSales Contract` sc ON sc.name = sis.parent
		WHERE sis.parenttype = 'Sales Contract'
		  AND sc.docstatus < 2
		  {conditions}
		ORDER BY sc.contract_date DESC, sc.name, sis.sequence
		""",
		values,
		as_dict=1,
	)


def get_conditions(filters):
	conditions = []
	values = {}
	if filters.get("company"):
		conditions.append("sc.company = %(company)s")
		values["company"] = filters["company"]
	if filters.get("real_estate_project"):
		conditions.append("sc.real_estate_project = %(real_estate_project)s")
		values["real_estate_project"] = filters["real_estate_project"]
	if filters.get("sales_contract"):
		conditions.append("sc.name = %(sales_contract)s")
		values["sales_contract"] = filters["sales_contract"]
	if filters.get("customer"):
		conditions.append("sc.customer = %(customer)s")
		values["customer"] = filters["customer"]
	if filters.get("invoice_status"):
		conditions.append("sis.invoice_status = %(invoice_status)s")
		values["invoice_status"] = filters["invoice_status"]
	if filters.get("from_date"):
		conditions.append("sis.due_date >= %(from_date)s")
		values["from_date"] = filters["from_date"]
	if filters.get("to_date"):
		conditions.append("sis.due_date <= %(to_date)s")
		values["to_date"] = filters["to_date"]
	return (" AND " + " AND ".join(conditions)) if conditions else "", values
