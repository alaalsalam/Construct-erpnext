import frappe
from frappe import _


def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = [
		{"label": _("Date"), "fieldname": "posting_date", "fieldtype": "Date", "width": 110},
		{"label": _("Voucher Type"), "fieldname": "voucher_type", "fieldtype": "Data", "width": 130},
		{"label": _("Voucher No"), "fieldname": "voucher_no", "fieldtype": "Dynamic Link", "options": "voucher_type", "width": 170},
		{"label": _("Account"), "fieldname": "account", "fieldtype": "Link", "options": "Account", "width": 180},
		{"label": _("Debit"), "fieldname": "debit", "fieldtype": "Currency", "width": 120},
		{"label": _("Credit"), "fieldname": "credit", "fieldtype": "Currency", "width": 120},
		{"label": _("Net Amount"), "fieldname": "net_amount", "fieldtype": "Currency", "width": 120},
		{"label": _("Unit"), "fieldname": "unit", "fieldtype": "Link", "options": "Unit", "width": 120},
		{"label": _("Cost Code"), "fieldname": "cost_code", "fieldtype": "Link", "options": "Cost Code", "width": 120},
		{"label": _("Remarks"), "fieldname": "remarks", "fieldtype": "Small Text", "width": 220},
	]
	return columns, get_data(filters)


def get_data(filters):
	meta = frappe.get_meta("GL Entry", cached=False)
	if not meta.get_field("construction_work_item"):
		return []

	selects = [
		"posting_date",
		"voucher_type",
		"voucher_no",
		"account",
		"debit",
		"credit",
		"(debit - credit) AS net_amount",
		"unit" if meta.get_field("unit") else "'' AS unit",
		"cost_code" if meta.get_field("cost_code") else "'' AS cost_code",
		"remarks",
	]
	conditions = ["is_cancelled = 0"]
	values = {}
	for fieldname in ("construction_work_item", "project"):
		if filters.get(fieldname):
			conditions.append(f"{fieldname} = %({fieldname})s")
			values[fieldname] = filters[fieldname]
	if filters.get("from_date"):
		conditions.append("posting_date >= %(from_date)s")
		values["from_date"] = filters.from_date
	if filters.get("to_date"):
		conditions.append("posting_date <= %(to_date)s")
		values["to_date"] = filters.to_date

	return frappe.db.sql(
		f"""
		SELECT {", ".join(selects)}
		FROM `tabGL Entry`
		WHERE {" AND ".join(conditions)}
		ORDER BY posting_date, creation
		""",
		values,
		as_dict=True,
	)
