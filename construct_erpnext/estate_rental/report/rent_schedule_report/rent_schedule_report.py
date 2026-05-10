import frappe
from frappe import _


def execute(filters=None):
	return get_columns(), get_data(filters or {})


def get_columns():
	return [
		{"fieldname": "lease_contract", "fieldtype": "Link", "label": _("Lease Contract"), "options": "Lease Contract", "width": 150},
		{"fieldname": "unit", "fieldtype": "Link", "label": _("Unit"), "options": "Unit", "width": 100},
		{"fieldname": "tenant_display", "fieldtype": "Data", "label": _("Tenant / Customer"), "width": 170},
		{"fieldname": "rent_period_start", "fieldtype": "Date", "label": _("Period Start"), "width": 110},
		{"fieldname": "rent_period_end", "fieldtype": "Date", "label": _("Period End"), "width": 110},
		{"fieldname": "due_date", "fieldtype": "Date", "label": _("Due Date"), "width": 110},
		{"fieldname": "rent_amount", "fieldtype": "Currency", "label": _("Rent Amount"), "width": 130},
		{"fieldname": "rent_status", "fieldtype": "Data", "label": _("Status"), "width": 110},
		{"fieldname": "sales_invoice", "fieldtype": "Link", "label": _("Invoice"), "options": "Sales Invoice", "width": 150},
		{"fieldname": "payment_entry", "fieldtype": "Link", "label": _("Payment"), "options": "Payment Entry", "width": 150},
	]


def get_data(filters):
	conditions, values = get_conditions(filters)
	return frappe.db.sql(
		f"""
		SELECT
			rs.parent AS lease_contract,
			lc.unit,
			COALESCE(c.customer_name, lc.tenant_name) AS tenant_display,
			rs.rent_period_start,
			rs.rent_period_end,
			rs.due_date,
			rs.rent_amount,
			rs.rent_status,
			rs.sales_invoice,
			rs.payment_entry
		FROM `tabRent Schedule` rs
		INNER JOIN `tabLease Contract` lc ON lc.name = rs.parent
		LEFT JOIN `tabCustomer` c ON c.name = lc.customer
		WHERE rs.parenttype = 'Lease Contract'
			AND lc.docstatus < 2
		{conditions}
		ORDER BY rs.due_date ASC, rs.sequence ASC
		""",
		values,
		as_dict=1,
	)


def get_conditions(filters):
	conditions = []
	values = {}
	if filters.get("company"):
		conditions.append("lc.company = %(company)s")
		values["company"] = filters["company"]
	if filters.get("real_estate_project"):
		conditions.append("lc.real_estate_project = %(real_estate_project)s")
		values["real_estate_project"] = filters["real_estate_project"]
	if filters.get("lease_contract"):
		conditions.append("rs.parent = %(lease_contract)s")
		values["lease_contract"] = filters["lease_contract"]
	if filters.get("customer"):
		conditions.append("lc.customer = %(customer)s")
		values["customer"] = filters["customer"]
	if filters.get("rent_status"):
		conditions.append("rs.rent_status = %(rent_status)s")
		values["rent_status"] = filters["rent_status"]
	if filters.get("from_due_date"):
		conditions.append("rs.due_date >= %(from_due_date)s")
		values["from_due_date"] = filters["from_due_date"]
	if filters.get("to_due_date"):
		conditions.append("rs.due_date <= %(to_due_date)s")
		values["to_due_date"] = filters["to_due_date"]
	return (" AND " + " AND ".join(conditions)) if conditions else "", values
