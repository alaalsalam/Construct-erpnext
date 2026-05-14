import frappe
from frappe import _
from construct_erpnext.reporting.report_utils import report_dashboard_message, sum_field, summary_value


def execute(filters=None):
	data = get_data(frappe._dict(filters or {}))
	return get_columns(), data, report_dashboard_message(get_report_summary(data)), None, None, False


def get_columns():
	return [
		{"fieldname": "lease_contract", "fieldtype": "Link", "label": _("Lease Contract"), "options": "Lease Contract", "width": 150},
		{"fieldname": "unit", "fieldtype": "Link", "label": _("Unit"), "options": "Unit", "width": 120},
		{"fieldname": "customer", "fieldtype": "Link", "label": _("Customer"), "options": "Customer", "width": 170},
		{"fieldname": "total_scheduled_rent", "fieldtype": "Currency", "label": _("Total Scheduled Rent"), "width": 150},
		{"fieldname": "total_invoiced_rent", "fieldtype": "Currency", "label": _("Total Invoiced Rent"), "width": 150},
		{"fieldname": "total_collected_rent", "fieldtype": "Currency", "label": _("Total Collected Rent"), "width": 150},
		{"fieldname": "total_outstanding_rent", "fieldtype": "Currency", "label": _("Total Outstanding Rent"), "width": 160},
		{"fieldname": "rent_collection_status", "fieldtype": "Data", "label": _("Rent Collection Status"), "width": 160},
		{"fieldname": "latest_payment_entry", "fieldtype": "Link", "label": _("Latest Payment Entry"), "options": "Payment Entry", "width": 150},
	]


def get_data(filters):
	lease_filters = {"docstatus": ["<", 2]}
	for fieldname in ("company", "real_estate_project", "customer", "rent_collection_status"):
		if filters.get(fieldname):
			lease_filters[fieldname] = filters.get(fieldname)
	if filters.get("from_date") and filters.get("to_date"):
		lease_filters["contract_date"] = ["between", [filters.from_date, filters.to_date]]
	elif filters.get("from_date"):
		lease_filters["contract_date"] = [">=", filters.from_date]
	elif filters.get("to_date"):
		lease_filters["contract_date"] = ["<=", filters.to_date]

	rows = frappe.get_all(
		"Lease Contract",
		filters=lease_filters,
		fields=[
			"name",
			"unit",
			"customer",
			"total_scheduled_rent",
			"total_invoiced_rent",
			"total_collected_rent",
			"total_outstanding_rent",
			"rent_collection_status",
			"latest_payment_entry",
		],
		order_by="contract_date desc, name desc",
	)
	for row in rows:
		row["lease_contract"] = row.name
	return rows


def get_report_summary(data):
	return [
		summary_value("Total Scheduled Rent", sum_field(data, "total_scheduled_rent"), "Currency", "Blue"),
		summary_value("Total Invoiced Rent", sum_field(data, "total_invoiced_rent"), "Currency", "Orange"),
		summary_value("Total Collected Rent", sum_field(data, "total_collected_rent"), "Currency", "Green"),
		summary_value("Total Outstanding Rent", sum_field(data, "total_outstanding_rent"), "Currency", "Red"),
	]
