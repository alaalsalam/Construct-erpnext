import frappe
from frappe import _


def execute(filters=None):
	return get_columns(), get_data(frappe._dict(filters or {}))


def get_columns():
	return [
		{"fieldname": "unit", "fieldtype": "Link", "label": _("Unit"), "options": "Unit", "width": 150},
		{"fieldname": "sales_contract", "fieldtype": "Link", "label": _("Sales Contract"), "options": "Sales Contract", "width": 160},
		{"fieldname": "contract_amount", "fieldtype": "Currency", "label": _("Contract Amount"), "width": 140},
		{"fieldname": "invoiced_amount", "fieldtype": "Currency", "label": _("Invoiced Amount"), "width": 140},
		{"fieldname": "collected_amount", "fieldtype": "Currency", "label": _("Collected Amount"), "width": 140},
		{"fieldname": "outstanding_amount", "fieldtype": "Currency", "label": _("Outstanding Amount"), "width": 150},
		{"fieldname": "profitability_status", "fieldtype": "Data", "label": _("Profitability Status"), "width": 150},
		{"fieldname": "unit_dimension_status", "fieldtype": "Data", "label": _("Unit Dimension Status"), "width": 170},
	]


def get_data(filters):
	contract_filters = {"docstatus": ["<", 2]}
	for fieldname in ("real_estate_project", "unit", "customer"):
		if filters.get(fieldname):
			contract_filters[fieldname] = filters.get(fieldname)

	rows = []
	for contract in frappe.get_all(
		"Sales Contract",
		filters=contract_filters,
		fields=[
			"name",
			"unit",
			"net_price",
			"total_invoiced_amount",
			"total_collected_amount",
			"total_outstanding_amount",
		],
		order_by="contract_date desc, name desc",
	):
		rows.append(
			{
				"unit": contract.unit,
				"sales_contract": contract.name,
				"contract_amount": contract.net_price,
				"invoiced_amount": contract.total_invoiced_amount,
				"collected_amount": contract.total_collected_amount,
				"outstanding_amount": contract.total_outstanding_amount,
				"profitability_status": frappe.db.get_value("Unit", contract.unit, "profitability_status"),
				"unit_dimension_status": _get_unit_dimension_status(contract.name, contract.unit),
			}
		)
	return rows


def _get_unit_dimension_status(sales_contract, unit):
	invoice_items = frappe.get_all(
		"Sales Invoice Item",
		filters={"sales_contract": sales_contract},
		fields=["unit"],
		limit=100,
	)
	if not invoice_items:
		return _("No Invoice Item")
	if all(row.unit == unit for row in invoice_items):
		return _("Ready")
	return _("Needs Review")
