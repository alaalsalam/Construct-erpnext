import frappe
from frappe import _


def execute(filters=None):
	return get_columns(), get_data(filters or {})


def get_columns():
	return [
		{"fieldname": "unit", "fieldtype": "Link", "label": _("Unit"), "options": "Unit", "width": 90},
		{"fieldname": "customer", "fieldtype": "Link", "label": _("Customer"), "options": "Customer", "width": 160},
		{"fieldname": "sales_contract", "fieldtype": "Link", "label": _("Sales Contract"), "options": "Sales Contract", "width": 140},
		{"fieldname": "sales_invoice", "fieldtype": "Link", "label": _("Sales Invoice"), "options": "Sales Invoice", "width": 140},
		{"fieldname": "invoice_amount", "fieldtype": "Currency", "label": _("Invoice Amount"), "width": 120},
		{"fieldname": "paid_amount", "fieldtype": "Currency", "label": _("Paid Amount"), "width": 120},
		{"fieldname": "outstanding_amount", "fieldtype": "Currency", "label": _("Outstanding"), "width": 120},
		{"fieldname": "unit_dimension", "fieldtype": "Link", "label": _("Unit Dimension"), "options": "Unit", "width": 120},
		{"fieldname": "profitability_status", "fieldtype": "Data", "label": _("Profitability Status"), "width": 140},
	]


def get_data(filters):
	conditions, values = get_conditions(filters)
	return frappe.db.sql(
		f"""
		SELECT
			sc.unit,
			sc.customer,
			sc.name AS sales_contract,
			sis.sales_invoice,
			sis.invoice_amount,
			sis.paid_amount,
			sis.outstanding_amount,
			sii.unit AS unit_dimension,
			u.profitability_status
		FROM `tabSales Contract` sc
		LEFT JOIN `tabSales Installment Schedule` sis
			ON sis.parent = sc.name AND sis.parenttype = 'Sales Contract'
		LEFT JOIN `tabSales Invoice Item` sii
			ON sii.parent = sis.sales_invoice AND sii.sales_contract = sc.name
		LEFT JOIN `tabUnit` u ON u.name = sc.unit
		WHERE sc.docstatus < 2
		  {conditions}
		ORDER BY sc.contract_date DESC, sc.name, sis.sequence
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
	if filters.get("unit"):
		conditions.append("sc.unit = %(unit)s")
		values["unit"] = filters["unit"]
	if filters.get("customer"):
		conditions.append("sc.customer = %(customer)s")
		values["customer"] = filters["customer"]
	if filters.get("from_date"):
		conditions.append("sc.contract_date >= %(from_date)s")
		values["from_date"] = filters["from_date"]
	if filters.get("to_date"):
		conditions.append("sc.contract_date <= %(to_date)s")
		values["to_date"] = filters["to_date"]
	return (" AND " + " AND ".join(conditions)) if conditions else "", values
