import frappe
from frappe import _
from construct_erpnext.reporting.report_utils import normalize_common_filters


def execute(filters=None):
	filters = normalize_common_filters(filters)
	columns = [
		{"label": _("Contractor"), "fieldname": "contractor", "fieldtype": "Link", "options": "Supplier", "width": 170},
		{"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 160},
		{"label": _("IPC"), "fieldname": "name", "fieldtype": "Link", "options": "Interim Payment Certificate", "width": 160},
		{"label": _("Purchase Invoice"), "fieldname": "purchase_invoice", "fieldtype": "Link", "options": "Purchase Invoice", "width": 160},
		{"label": _("Expected Payment Date"), "fieldname": "expected_payment_date", "fieldtype": "Date", "width": 150},
		{"label": _("Net Payable"), "fieldname": "net_payable", "fieldtype": "Currency", "width": 130},
		{"label": _("Paid Amount"), "fieldname": "paid_amount", "fieldtype": "Currency", "width": 120},
		{"label": _("Outstanding Amount"), "fieldname": "outstanding_amount", "fieldtype": "Currency", "width": 150},
		{"label": _("Retention Due"), "fieldname": "retention_due", "fieldtype": "Currency", "width": 130},
		{"label": _("Risk Status"), "fieldname": "risk_status", "fieldtype": "Data", "width": 110},
	]
	conditions = ["ipc.docstatus < 2", "ipc.status IN ('Approved', 'Invoice Created', 'Partially Paid')"]
	values = {}
	if filters.get("project"):
		conditions.append("ipc.project = %(project)s")
		values["project"] = filters["project"]
	if filters.get("contractor"):
		conditions.append("ipc.contractor = %(contractor)s")
		values["contractor"] = filters["contractor"]
	if filters.get("from_date"):
		conditions.append("COALESCE(ipc.expected_next_payment_date, ipc.period_end) >= %(from_date)s")
		values["from_date"] = filters["from_date"]
	if filters.get("to_date"):
		conditions.append("COALESCE(ipc.expected_next_payment_date, ipc.period_end) <= %(to_date)s")
		values["to_date"] = filters["to_date"]
	data = frappe.db.sql(
		f"""
		SELECT ipc.contractor, ipc.project, ipc.name, ipc.purchase_invoice,
			COALESCE(ipc.expected_next_payment_date, ipc.period_end) AS expected_payment_date,
			ipc.net_payable, ipc.paid_amount,
			COALESCE(ipc.outstanding_amount, ipc.net_payable - ipc.paid_amount, ipc.net_payable, 0) AS outstanding_amount,
			COALESCE(ret.remaining_retention_amount, 0) AS retention_due,
			CASE
				WHEN COALESCE(ipc.outstanding_amount, ipc.net_payable - ipc.paid_amount, ipc.net_payable, 0) > 0 THEN 'Red'
				ELSE 'Green'
			END AS risk_status
		FROM `tabInterim Payment Certificate` ipc
		LEFT JOIN `tabRetention Register` ret ON ret.ipc = ipc.name AND ret.status != 'Cancelled'
		WHERE {" AND ".join(conditions)}
		ORDER BY expected_payment_date ASC, ipc.creation ASC
		""",
		values,
		as_dict=True,
	)
	return columns, data
