import frappe
from frappe import _


def execute(filters=None):
	filters = filters or {}
	columns = [
		{"label": _("Date"), "fieldname": "posting_date", "fieldtype": "Date", "width": 110},
		{"label": _("Contractor"), "fieldname": "contractor", "fieldtype": "Link", "options": "Supplier", "width": 170},
		{"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 160},
		{"label": _("Transaction Type"), "fieldname": "transaction_type", "fieldtype": "Data", "width": 150},
		{"label": _("Reference"), "fieldname": "reference_name", "fieldtype": "Dynamic Link", "options": "reference_doctype", "width": 170},
		{"label": _("Gross Amount"), "fieldname": "gross_amount", "fieldtype": "Currency", "width": 120},
		{"label": _("Retention"), "fieldname": "retention_amount", "fieldtype": "Currency", "width": 120},
		{"label": _("Advance"), "fieldname": "advance_amount", "fieldtype": "Currency", "width": 120},
		{"label": _("Recovered"), "fieldname": "recovered_amount", "fieldtype": "Currency", "width": 120},
		{"label": _("Deduction"), "fieldname": "deduction_amount", "fieldtype": "Currency", "width": 120},
		{"label": _("Invoice Amount"), "fieldname": "invoice_amount", "fieldtype": "Currency", "width": 130},
		{"label": _("Payment Amount"), "fieldname": "payment_amount", "fieldtype": "Currency", "width": 130},
		{"label": _("Outstanding"), "fieldname": "outstanding_amount", "fieldtype": "Currency", "width": 130},
		{"label": _("Running Balance"), "fieldname": "running_balance", "fieldtype": "Currency", "width": 140},
		{"label": _("Remarks"), "fieldname": "remarks", "fieldtype": "Data", "width": 220},
	]
	conditions = ["1=1"]
	values = {}
	for field in ("project", "contractor", "contractor_account"):
		if filters.get(field):
			conditions.append(f"{field} = %({field})s")
			values[field] = filters[field]
	if filters.get("from_date"):
		conditions.append("posting_date >= %(from_date)s")
		values["from_date"] = filters["from_date"]
	if filters.get("to_date"):
		conditions.append("posting_date <= %(to_date)s")
		values["to_date"] = filters["to_date"]
	data = frappe.db.sql(
		f"""
		SELECT posting_date, contractor, project, transaction_type, reference_doctype,
			reference_name, gross_amount, retention_amount, advance_amount, recovered_amount,
			deduction_amount, invoice_amount, payment_amount, outstanding_amount,
			running_balance, remarks
		FROM `tabContractor Ledger Entry`
		WHERE {" AND ".join(conditions)}
		ORDER BY posting_date ASC, creation ASC
		""",
		values,
		as_dict=True,
	)
	return columns, data
