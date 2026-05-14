import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
	return get_columns(), get_data(frappe._dict(filters or {}))


def get_columns():
	return [
		{"fieldname": "broker", "fieldtype": "Link", "label": _("Broker"), "options": "Broker", "width": 180},
		{"fieldname": "entries_count", "fieldtype": "Int", "label": _("Commission Entries"), "width": 140},
		{"fieldname": "sales_count", "fieldtype": "Int", "label": _("Sales Count"), "width": 120},
		{"fieldname": "rent_count", "fieldtype": "Int", "label": _("Rent Count"), "width": 120},
		{"fieldname": "commission_base_amount", "fieldtype": "Currency", "label": _("Commission Base Amount"), "width": 160},
		{"fieldname": "commission_amount", "fieldtype": "Currency", "label": _("Commission Amount"), "width": 150},
		{"fieldname": "approved_amount", "fieldtype": "Currency", "label": _("Approved Amount"), "width": 150},
		{"fieldname": "paid_amount", "fieldtype": "Currency", "label": _("Paid Amount"), "width": 140},
	]


def get_data(filters):
	entry_filters = {"status": ["!=", "Cancelled"]}
	for fieldname in ("broker", "transaction_type"):
		if filters.get(fieldname):
			entry_filters[fieldname] = filters.get(fieldname)
	grouped = {}
	for entry in frappe.get_all(
		"Commission Entry",
		filters=entry_filters,
		fields=["broker", "transaction_type", "commission_base_amount", "commission_amount", "status"],
	):
		row = grouped.setdefault(
			entry.broker,
			{
				"broker": entry.broker,
				"entries_count": 0,
				"sales_count": 0,
				"rent_count": 0,
				"commission_base_amount": 0,
				"commission_amount": 0,
				"approved_amount": 0,
				"paid_amount": 0,
			},
		)
		row["entries_count"] += 1
		row["sales_count" if entry.transaction_type == "Sale" else "rent_count"] += 1
		row["commission_base_amount"] += flt(entry.commission_base_amount)
		row["commission_amount"] += flt(entry.commission_amount)
		if entry.status in ("Approved", "Paid"):
			row["approved_amount"] += flt(entry.commission_amount)
		if entry.status == "Paid":
			row["paid_amount"] += flt(entry.commission_amount)
	return list(grouped.values())
