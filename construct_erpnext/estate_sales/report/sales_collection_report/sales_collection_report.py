import frappe
from frappe import _


def execute(filters=None):
	return get_columns(), get_data(filters or {})


def get_columns():
	return [
		{"fieldname": "sales_contract", "fieldtype": "Link", "label": _("Sales Contract"), "options": "Sales Contract", "width": 140},
		{"fieldname": "unit", "fieldtype": "Link", "label": _("Unit"), "options": "Unit", "width": 90},
		{"fieldname": "customer", "fieldtype": "Link", "label": _("Customer"), "options": "Customer", "width": 160},
		{"fieldname": "net_price", "fieldtype": "Currency", "label": _("Net Price"), "width": 120},
		{"fieldname": "total_invoiced_amount", "fieldtype": "Currency", "label": _("Total Invoiced"), "width": 130},
		{"fieldname": "total_collected_amount", "fieldtype": "Currency", "label": _("Total Collected"), "width": 130},
		{"fieldname": "total_outstanding_amount", "fieldtype": "Currency", "label": _("Outstanding"), "width": 120},
		{"fieldname": "collection_status", "fieldtype": "Data", "label": _("Collection Status"), "width": 130},
		{"fieldname": "latest_payment_entry", "fieldtype": "Link", "label": _("Latest Payment Entry"), "options": "Payment Entry", "width": 150},
	]


def get_data(filters):
	conditions, values = get_conditions(filters)
	return frappe.db.sql(
		f"""
		SELECT
			sc.name AS sales_contract,
			sc.unit,
			sc.customer,
			sc.net_price,
			sc.total_invoiced_amount,
			sc.total_collected_amount,
			sc.total_outstanding_amount,
			sc.collection_status,
			sc.latest_payment_entry
		FROM `tabSales Contract` sc
		WHERE sc.docstatus < 2
		  {conditions}
		ORDER BY sc.contract_date DESC, sc.name DESC
		""",
		values,
		as_dict=1,
	)


def get_conditions(filters):
	conditions = []
	values = {}
	for fieldname in ("company", "real_estate_project", "customer", "collection_status"):
		if filters.get(fieldname):
			conditions.append(f"sc.{fieldname} = %({fieldname})s")
			values[fieldname] = filters[fieldname]
	if filters.get("from_date"):
		conditions.append("sc.contract_date >= %(from_date)s")
		values["from_date"] = filters["from_date"]
	if filters.get("to_date"):
		conditions.append("sc.contract_date <= %(to_date)s")
		values["to_date"] = filters["to_date"]
	return (" AND " + " AND ".join(conditions)) if conditions else "", values
