import frappe
from frappe import _


def execute(filters=None):
	filters = filters or {}
	columns = [
		{"label": _("Agreement"), "fieldname": "agreement", "fieldtype": "Link", "options": "Subcontract", "width": 170},
		{"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 160},
		{"label": _("Contractor"), "fieldname": "contractor", "fieldtype": "Link", "options": "Supplier", "width": 180},
		{"label": _("Agreement Date"), "fieldname": "agreement_date", "fieldtype": "Date", "width": 120},
		{"label": _("Type"), "fieldname": "agreement_type", "fieldtype": "Data", "width": 120},
		{"label": _("Total Agreement Amount"), "fieldname": "total_agreement_amount", "fieldtype": "Currency", "width": 160},
		{"label": _("Measured Amount"), "fieldname": "measured_amount", "fieldtype": "Currency", "width": 140},
		{"label": _("Certified Amount"), "fieldname": "certified_amount", "fieldtype": "Currency", "width": 140},
		{"label": _("Remaining Amount"), "fieldname": "remaining_agreement_amount", "fieldtype": "Currency", "width": 150},
		{"label": _("Retention %"), "fieldname": "retention_percent", "fieldtype": "Percent", "width": 110},
		{"label": _("Status"), "fieldname": "contract_status", "fieldtype": "Data", "width": 120},
	]
	doc_filters = {"docstatus": ["!=", 2]}
	for field in ("project", "contractor", "agreement_type"):
		if filters.get(field):
			doc_filters[field] = filters[field]
	if filters.get("status"):
		doc_filters["contract_status"] = filters["status"]

	data = []
	for row in frappe.get_all(
		"Subcontract",
		filters=doc_filters,
		fields=[
			"name",
			"project",
			"contractor",
			"agreement_date",
			"agreement_type",
			"total_agreement_amount",
			"measured_amount",
			"certified_amount",
			"remaining_agreement_amount",
			"retention_percent",
			"contract_status",
		],
		order_by="project asc, contractor asc, agreement_date desc",
	):
		row["agreement"] = row.name
		data.append(row)
	return columns, data
