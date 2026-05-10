import frappe
from frappe import _


def execute(filters=None):
	return get_columns(), get_data(filters or {})


def get_columns():
	return [
		{"fieldname": "lease_contract", "fieldtype": "Link", "label": _("Lease Contract"), "options": "Lease Contract", "width": 150},
		{"fieldname": "unit", "fieldtype": "Link", "label": _("Unit"), "options": "Unit", "width": 100},
		{"fieldname": "tenant_display", "fieldtype": "Data", "label": _("Tenant / Customer"), "width": 170},
		{"fieldname": "lease_start_date", "fieldtype": "Date", "label": _("Lease Start"), "width": 110},
		{"fieldname": "lease_end_date", "fieldtype": "Date", "label": _("Lease End"), "width": 110},
		{"fieldname": "monthly_rent", "fieldtype": "Currency", "label": _("Monthly Rent"), "width": 130},
		{"fieldname": "total_scheduled_rent", "fieldtype": "Currency", "label": _("Total Scheduled Rent"), "width": 150},
		{"fieldname": "lease_status", "fieldtype": "Data", "label": _("Status"), "width": 110},
		{"fieldname": "workflow_state", "fieldtype": "Data", "label": _("Workflow State"), "width": 130},
	]


def get_data(filters):
	conditions, values = get_conditions(filters)
	return frappe.db.sql(
		f"""
		SELECT
			lc.name AS lease_contract,
			lc.unit,
			COALESCE(c.customer_name, lc.tenant_name) AS tenant_display,
			lc.lease_start_date,
			lc.lease_end_date,
			lc.monthly_rent,
			lc.total_scheduled_rent,
			lc.lease_status,
			lc.workflow_state
		FROM `tabLease Contract` lc
		LEFT JOIN `tabCustomer` c ON c.name = lc.customer
		WHERE lc.docstatus < 2
		{conditions}
		ORDER BY lc.lease_start_date DESC, lc.name DESC
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
	if filters.get("customer"):
		conditions.append("lc.customer = %(customer)s")
		values["customer"] = filters["customer"]
	if filters.get("lease_status"):
		conditions.append("lc.lease_status = %(lease_status)s")
		values["lease_status"] = filters["lease_status"]
	if filters.get("from_date"):
		conditions.append("lc.contract_date >= %(from_date)s")
		values["from_date"] = filters["from_date"]
	if filters.get("to_date"):
		conditions.append("lc.contract_date <= %(to_date)s")
		values["to_date"] = filters["to_date"]
	return (" AND " + " AND ".join(conditions)) if conditions else "", values
