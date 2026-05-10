import frappe
from frappe import _


def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = get_columns()
	data = get_gl_data(filters)
	return columns, data


def get_columns():
	return [
		{"label": _("Posting Date"), "fieldname": "posting_date", "fieldtype": "Date", "width": 110},
		{"label": _("Account"), "fieldname": "account", "fieldtype": "Link", "options": "Account", "width": 180},
		{"label": _("Voucher Type"), "fieldname": "voucher_type", "fieldtype": "Data", "width": 130},
		{"label": _("Voucher No"), "fieldname": "voucher_no", "fieldtype": "Dynamic Link", "options": "voucher_type", "width": 170},
		{"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 140},
		{"label": _("Unit"), "fieldname": "unit", "fieldtype": "Link", "options": "Unit", "width": 120},
		{"label": _("Construction Work Item"), "fieldname": "construction_work_item", "fieldtype": "Link", "options": "Construction Work Item", "width": 170},
		{"label": _("Cost Code"), "fieldname": "cost_code", "fieldtype": "Link", "options": "Cost Code", "width": 120},
		{"label": _("Debit"), "fieldname": "debit", "fieldtype": "Currency", "width": 120},
		{"label": _("Credit"), "fieldname": "credit", "fieldtype": "Currency", "width": 120},
		{"label": _("Balance"), "fieldname": "balance", "fieldtype": "Currency", "width": 120},
		{"label": _("Remarks"), "fieldname": "remarks", "fieldtype": "Small Text", "width": 220},
	]


def get_gl_data(filters):
	meta = frappe.get_meta("GL Entry", cached=False)
	optional_fields = ["unit", "construction_work_item", "cost_code"]
	selects = [
		"posting_date",
		"account",
		"voucher_type",
		"voucher_no",
		"project",
	]
	for fieldname in optional_fields:
		selects.append(fieldname if meta.get_field(fieldname) else f"'' AS {fieldname}")
	selects.extend(["debit", "credit", "(debit - credit) AS balance", "remarks"])

	conditions = ["is_cancelled = 0"]
	values = {}
	for fieldname in ("company", "project", "unit", "construction_work_item", "cost_code"):
		if filters.get(fieldname) and (fieldname in ("company", "project") or meta.get_field(fieldname)):
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
