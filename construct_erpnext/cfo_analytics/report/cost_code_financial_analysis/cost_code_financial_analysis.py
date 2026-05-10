import frappe
from frappe import _


def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = [
		{"label": _("Cost Code"), "fieldname": "cost_code", "fieldtype": "Link", "options": "Cost Code", "width": 130},
		{"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 140},
		{"label": _("Unit"), "fieldname": "unit", "fieldtype": "Link", "options": "Unit", "width": 120},
		{"label": _("Work Item"), "fieldname": "construction_work_item", "fieldtype": "Link", "options": "Construction Work Item", "width": 170},
		{"label": _("Debit"), "fieldname": "debit", "fieldtype": "Currency", "width": 120},
		{"label": _("Credit"), "fieldname": "credit", "fieldtype": "Currency", "width": 120},
		{"label": _("Net Cost"), "fieldname": "net_cost", "fieldtype": "Currency", "width": 120},
		{"label": _("Voucher Count"), "fieldname": "voucher_count", "fieldtype": "Int", "width": 110},
	]
	return columns, get_data(filters)


def get_data(filters):
	meta = frappe.get_meta("GL Entry", cached=False)
	if not meta.get_field("cost_code"):
		return []

	selects = [
		"cost_code",
		"project",
		"unit" if meta.get_field("unit") else "'' AS unit",
		"construction_work_item" if meta.get_field("construction_work_item") else "'' AS construction_work_item",
		"SUM(debit) AS debit",
		"SUM(credit) AS credit",
		"SUM(debit - credit) AS net_cost",
		"COUNT(DISTINCT voucher_no) AS voucher_count",
	]
	group_by = ["cost_code", "project"]
	if meta.get_field("unit"):
		group_by.append("unit")
	if meta.get_field("construction_work_item"):
		group_by.append("construction_work_item")

	conditions = ["is_cancelled = 0"]
	values = {}
	for fieldname in ("project", "cost_code", "unit"):
		if filters.get(fieldname) and (fieldname != "unit" or meta.get_field("unit")):
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
		GROUP BY {", ".join(group_by)}
		ORDER BY cost_code, project
		""",
		values,
		as_dict=True,
	)
