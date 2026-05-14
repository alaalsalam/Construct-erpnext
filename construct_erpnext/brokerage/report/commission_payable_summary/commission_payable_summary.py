import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
	return get_columns(), get_data(frappe._dict(filters or {}))


def get_columns():
	return [
		{"fieldname": "broker", "fieldtype": "Link", "label": _("Broker"), "options": "Broker", "width": 180},
		{"fieldname": "accrued_amount", "fieldtype": "Currency", "label": _("Accrued Amount"), "width": 150},
		{"fieldname": "approved_amount", "fieldtype": "Currency", "label": _("Approved Amount"), "width": 150},
		{"fieldname": "paid_amount", "fieldtype": "Currency", "label": _("Paid Amount"), "width": 140},
		{"fieldname": "payable_amount", "fieldtype": "Currency", "label": _("Payable Amount"), "width": 150},
		{"fieldname": "entries_count", "fieldtype": "Int", "label": _("Commission Entries"), "width": 140},
	]


def get_data(filters):
	entry_filters = {"status": ["!=", "Cancelled"]}
	if filters.get("broker"):
		entry_filters["broker"] = filters.broker
	if filters.get("status"):
		entry_filters["status"] = filters.status
	grouped = {}
	for entry in frappe.get_all(
		"Commission Entry",
		filters=entry_filters,
		fields=["broker", "commission_amount", "status"],
	):
		row = grouped.setdefault(
			entry.broker,
			{
				"broker": entry.broker,
				"accrued_amount": 0,
				"approved_amount": 0,
				"paid_amount": 0,
				"payable_amount": 0,
				"entries_count": 0,
			},
		)
		row["entries_count"] += 1
		amount = flt(entry.commission_amount)
		if entry.status == "Accrued":
			row["accrued_amount"] += amount
			row["payable_amount"] += amount
		elif entry.status == "Approved":
			row["approved_amount"] += amount
			row["payable_amount"] += amount
		elif entry.status == "Paid":
			row["paid_amount"] += amount
	return list(grouped.values())
