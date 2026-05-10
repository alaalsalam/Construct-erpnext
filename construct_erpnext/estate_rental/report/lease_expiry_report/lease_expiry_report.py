import frappe
from frappe import _
from frappe.utils import add_days, date_diff, nowdate


def execute(filters=None):
	return get_columns(), get_data(filters or {})


def get_columns():
	return [
		{"fieldname": "lease_contract", "fieldtype": "Link", "label": _("Lease Contract"), "options": "Lease Contract", "width": 150},
		{"fieldname": "unit", "fieldtype": "Link", "label": _("Unit"), "options": "Unit", "width": 100},
		{"fieldname": "tenant_display", "fieldtype": "Data", "label": _("Tenant / Customer"), "width": 170},
		{"fieldname": "lease_end_date", "fieldtype": "Date", "label": _("Lease End"), "width": 110},
		{"fieldname": "days_remaining", "fieldtype": "Int", "label": _("Days Remaining"), "width": 120},
		{"fieldname": "monthly_rent", "fieldtype": "Currency", "label": _("Monthly Rent"), "width": 130},
		{"fieldname": "lease_status", "fieldtype": "Data", "label": _("Status"), "width": 110},
	]


def get_data(filters):
	within_days = int(filters.get("within_days") or 60)
	values = {"today": nowdate(), "to_date": add_days(nowdate(), within_days)}
	conditions = ["lc.lease_end_date BETWEEN %(today)s AND %(to_date)s"]
	if filters.get("real_estate_project"):
		conditions.append("lc.real_estate_project = %(real_estate_project)s")
		values["real_estate_project"] = filters["real_estate_project"]

	rows = frappe.db.sql(
		f"""
		SELECT
			lc.name AS lease_contract,
			lc.unit,
			COALESCE(c.customer_name, lc.tenant_name) AS tenant_display,
			lc.lease_end_date,
			lc.monthly_rent,
			lc.lease_status
		FROM `tabLease Contract` lc
		LEFT JOIN `tabCustomer` c ON c.name = lc.customer
		WHERE lc.docstatus = 1
			AND lc.lease_status IN ('Approved', 'Active')
			AND {" AND ".join(conditions)}
		ORDER BY lc.lease_end_date ASC
		""",
		values,
		as_dict=1,
	)
	for row in rows:
		row.days_remaining = date_diff(row.lease_end_date, nowdate()) if row.lease_end_date else 0
	return rows
