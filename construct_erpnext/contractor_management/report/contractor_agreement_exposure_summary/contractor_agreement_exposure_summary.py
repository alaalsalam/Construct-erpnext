import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
	filters = filters or {}
	columns = [
		{"label": _("Contractor"), "fieldname": "contractor", "fieldtype": "Link", "options": "Supplier", "width": 180},
		{"label": _("Agreements Count"), "fieldname": "agreements_count", "fieldtype": "Int", "width": 130},
		{"label": _("Total Agreement Amount"), "fieldname": "total_agreement_amount", "fieldtype": "Currency", "width": 170},
		{"label": _("Certified Amount"), "fieldname": "certified_amount", "fieldtype": "Currency", "width": 150},
		{"label": _("Retention Held"), "fieldname": "retention_held", "fieldtype": "Currency", "width": 140},
		{"label": _("Invoiced Amount"), "fieldname": "invoiced_amount", "fieldtype": "Currency", "width": 150},
		{"label": _("Outstanding Amount"), "fieldname": "outstanding_amount", "fieldtype": "Currency", "width": 160},
		{"label": _("Risk Status"), "fieldname": "risk_status", "fieldtype": "Data", "width": 120},
	]
	doc_filters = {"docstatus": ["!=", 2]}
	for field in ("project", "contractor"):
		if filters.get(field):
			doc_filters[field] = filters[field]
	summary = {}
	for agreement in frappe.get_all(
		"Subcontract",
		filters=doc_filters,
		fields=["name", "contractor", "total_agreement_amount", "certified_amount", "invoiced_amount", "remaining_agreement_amount"],
	):
		row = summary.setdefault(
			agreement.contractor,
			{
				"contractor": agreement.contractor,
				"agreements_count": 0,
				"total_agreement_amount": 0,
				"certified_amount": 0,
				"retention_held": 0,
				"invoiced_amount": 0,
				"outstanding_amount": 0,
			},
		)
		row["agreements_count"] += 1
		row["total_agreement_amount"] += flt(agreement.total_agreement_amount)
		row["certified_amount"] += flt(agreement.certified_amount)
		row["invoiced_amount"] += flt(agreement.invoiced_amount)
		row["outstanding_amount"] += flt(agreement.remaining_agreement_amount)
		for retention in frappe.get_all(
			"Retention Register",
			filters={"contractor": agreement.contractor, "status": ["!=", "Cancelled"]},
			fields=["retention_amount", "released_amount"],
		):
			row["retention_held"] += flt(retention.retention_amount) - flt(retention.released_amount)

	data = list(summary.values())
	for row in data:
		if flt(row["outstanding_amount"]) > flt(row["total_agreement_amount"]) * 0.4:
			row["risk_status"] = "Watch"
		else:
			row["risk_status"] = "Normal"
	return columns, data
