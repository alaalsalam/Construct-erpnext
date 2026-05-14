import frappe
from frappe import _
from frappe.utils import flt, getdate


def execute(filters=None):
	filters = frappe._dict(filters or {})
	return get_columns(), get_data(filters)


def get_columns():
	return [
		{"fieldname": "posting_date", "fieldtype": "Date", "label": _("Date"), "width": 100},
		{"fieldname": "lease_contract", "fieldtype": "Link", "label": _("Lease Contract"), "options": "Lease Contract", "width": 150},
		{"fieldname": "unit", "fieldtype": "Link", "label": _("Unit"), "options": "Unit", "width": 120},
		{"fieldname": "invoice", "fieldtype": "Link", "label": _("Invoice"), "options": "Sales Invoice", "width": 150},
		{"fieldname": "rent_period", "fieldtype": "Data", "label": _("Rent Period"), "width": 150},
		{"fieldname": "debit", "fieldtype": "Currency", "label": _("Debit"), "width": 130},
		{"fieldname": "credit", "fieldtype": "Currency", "label": _("Credit"), "width": 130},
		{"fieldname": "outstanding", "fieldtype": "Currency", "label": _("Outstanding"), "width": 130},
		{"fieldname": "status", "fieldtype": "Data", "label": _("Status"), "width": 130},
		{"fieldname": "remarks", "fieldtype": "Data", "label": _("Remarks"), "width": 240},
	]


def get_data(filters):
	rows = []
	for lease in _get_leases(filters):
		for schedule in _get_schedules(lease.name):
			if not schedule.sales_invoice:
				continue
			invoice = frappe.get_doc("Sales Invoice", schedule.sales_invoice)
			if invoice.docstatus == 2:
				continue
			if filters.get("from_date") and getdate(invoice.posting_date) < getdate(filters.from_date):
				continue
			if filters.get("to_date") and getdate(invoice.posting_date) > getdate(filters.to_date):
				continue

			rows.append(
				{
					"posting_date": invoice.posting_date,
					"lease_contract": lease.name,
					"unit": lease.unit,
					"invoice": invoice.name,
					"rent_period": schedule.label or schedule.sequence,
					"debit": flt(invoice.grand_total),
					"credit": 0,
					"outstanding": flt(invoice.outstanding_amount),
					"status": schedule.rent_status or invoice.status,
					"remarks": _("Rent invoice for real estate unit"),
				}
			)
			rows.extend(_get_payment_rows(invoice, lease, schedule))

	rows.sort(key=lambda row: (row.get("posting_date") or "", row.get("invoice") or "", row.get("credit") > 0))
	return rows


def _get_leases(filters):
	lease_filters = {"docstatus": ["<", 2]}
	for fieldname in ("customer", "lease_contract", "real_estate_project", "unit"):
		if filters.get(fieldname):
			lease_filters["name" if fieldname == "lease_contract" else fieldname] = filters.get(fieldname)
	return frappe.get_all(
		"Lease Contract",
		filters=lease_filters,
		fields=["name", "customer", "unit", "real_estate_project"],
		order_by="contract_date desc, name desc",
	)


def _get_schedules(lease_contract):
	return frappe.get_all(
		"Rent Schedule",
		filters={"parenttype": "Lease Contract", "parent": lease_contract},
		fields=["name", "sequence", "label", "sales_invoice", "rent_status"],
		order_by="sequence asc, idx asc",
	)


def _get_payment_rows(invoice, lease, schedule):
	rows = []
	for reference in frappe.get_all(
		"Payment Entry Reference",
		filters={"reference_doctype": "Sales Invoice", "reference_name": invoice.name},
		fields=["parent", "allocated_amount"],
	):
		if frappe.db.get_value("Payment Entry", reference.parent, "docstatus") != 1:
			continue
		posting_date = frappe.db.get_value("Payment Entry", reference.parent, "posting_date")
		rows.append(
			{
				"posting_date": posting_date,
				"lease_contract": lease.name,
				"unit": lease.unit,
				"invoice": invoice.name,
				"rent_period": schedule.label or schedule.sequence,
				"debit": 0,
				"credit": flt(reference.allocated_amount),
				"outstanding": flt(invoice.outstanding_amount),
				"status": _("Payment Received"),
				"remarks": reference.parent,
			}
		)
	return rows
