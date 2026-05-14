import frappe
from frappe import _


def execute(filters=None):
	return get_columns(), get_data(frappe._dict(filters or {}))


def get_columns():
	return [
		{"fieldname": "unit", "fieldtype": "Link", "label": _("Unit"), "options": "Unit", "width": 120},
		{"fieldname": "lease_contract", "fieldtype": "Link", "label": _("Lease Contract"), "options": "Lease Contract", "width": 150},
		{"fieldname": "customer", "fieldtype": "Link", "label": _("Customer"), "options": "Customer", "width": 170},
		{"fieldname": "total_scheduled_rent", "fieldtype": "Currency", "label": _("Total Scheduled Rent"), "width": 150},
		{"fieldname": "total_invoiced_rent", "fieldtype": "Currency", "label": _("Total Invoiced Rent"), "width": 150},
		{"fieldname": "total_collected_rent", "fieldtype": "Currency", "label": _("Total Collected Rent"), "width": 150},
		{"fieldname": "total_outstanding_rent", "fieldtype": "Currency", "label": _("Total Outstanding Rent"), "width": 160},
		{"fieldname": "profitability_status", "fieldtype": "Data", "label": _("Profitability Status"), "width": 140},
		{"fieldname": "unit_dimension_status", "fieldtype": "Data", "label": _("Unit Dimension Status"), "width": 150},
	]


def get_data(filters):
	lease_filters = {"docstatus": ["<", 2]}
	for fieldname in ("real_estate_project", "unit", "customer"):
		if filters.get(fieldname):
			lease_filters[fieldname] = filters.get(fieldname)
	data = []
	for lease in frappe.get_all(
		"Lease Contract",
		filters=lease_filters,
		fields=["name", "unit", "customer", "total_scheduled_rent", "total_invoiced_rent", "total_collected_rent", "total_outstanding_rent"],
		order_by="contract_date desc, name desc",
	):
		data.append(
			{
				"unit": lease.unit,
				"lease_contract": lease.name,
				"customer": lease.customer,
				"total_scheduled_rent": lease.total_scheduled_rent,
				"total_invoiced_rent": lease.total_invoiced_rent,
				"total_collected_rent": lease.total_collected_rent,
				"total_outstanding_rent": lease.total_outstanding_rent,
				"profitability_status": frappe.db.get_value("Unit", lease.unit, "profitability_status") if lease.unit else None,
				"unit_dimension_status": _("Ready") if lease.unit else _("Needs Review"),
			}
		)
	return data
