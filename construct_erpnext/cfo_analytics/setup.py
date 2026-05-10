import frappe
from frappe import _


FINANCIAL_DIMENSIONS = [
	{
		"label": "Construction Work Item",
		"fieldname": "construction_work_item",
		"document_type": "Construction Work Item",
	},
	{
		"label": "Cost Code",
		"fieldname": "cost_code",
		"document_type": "Cost Code",
	},
	{
		"label": "Unit",
		"fieldname": "unit",
		"document_type": "Unit",
	},
]

WORKSPACE_LINKS = {
	"Executive Control Center": [
		{"type": "Card Break", "label": "Financial Traceability"},
		{"type": "Link", "label": "GL Dimension Traceability", "link_type": "Report", "link_to": "GL Dimension Traceability", "is_query_report": 1},
		{"type": "Link", "label": "Unit Financial Ledger", "link_type": "Report", "link_to": "Unit Financial Ledger", "is_query_report": 1},
		{"type": "Link", "label": "Project Unit Cost Matrix", "link_type": "Report", "link_to": "Project Unit Cost Matrix", "is_query_report": 1},
	],
	"Reports & Analytics": [
		{"type": "Card Break", "label": "Financial Dimension Reports"},
		{"type": "Link", "label": "GL Dimension Traceability", "link_type": "Report", "link_to": "GL Dimension Traceability", "is_query_report": 1},
		{"type": "Link", "label": "Unit Financial Ledger", "link_type": "Report", "link_to": "Unit Financial Ledger", "is_query_report": 1},
		{"type": "Link", "label": "Work Item Financial Ledger", "link_type": "Report", "link_to": "Work Item Financial Ledger", "is_query_report": 1},
		{"type": "Link", "label": "Cost Code Financial Analysis", "link_type": "Report", "link_to": "Cost Code Financial Analysis", "is_query_report": 1},
		{"type": "Link", "label": "Project Unit Cost Matrix", "link_type": "Report", "link_to": "Project Unit Cost Matrix", "is_query_report": 1},
	],
	"Real Estate Inventory": [
		{"type": "Card Break", "label": "Unit Financial Traceability"},
		{"type": "Link", "label": "Unit Financial Ledger", "link_type": "Report", "link_to": "Unit Financial Ledger", "is_query_report": 1},
		{"type": "Link", "label": "Project Unit Cost Matrix", "link_type": "Report", "link_to": "Project Unit Cost Matrix", "is_query_report": 1},
	],
	"Construction Control": [
		{"type": "Card Break", "label": "Work Item Financial Traceability"},
		{"type": "Link", "label": "Work Item Financial Ledger", "link_type": "Report", "link_to": "Work Item Financial Ledger", "is_query_report": 1},
		{"type": "Link", "label": "Cost Code Financial Analysis", "link_type": "Report", "link_to": "Cost Code Financial Analysis", "is_query_report": 1},
	],
}


def after_migrate():
	ensure_financial_dimension_settings()
	ensure_financial_dimensions()
	ensure_financial_dimension_workspace_links()


def ensure_financial_dimension_settings():
	frappe.get_single("Financial Dimension Settings")


def ensure_financial_dimensions():
	from erpnext.accounts.doctype.accounting_dimension.accounting_dimension import (
		get_doctypes_with_dimensions,
		make_dimension_in_accounting_doctypes,
	)

	for dimension in FINANCIAL_DIMENSIONS:
		_validate_dimension_conflicts(dimension, get_doctypes_with_dimensions())
		doc = _get_or_create_dimension(dimension)
		make_dimension_in_accounting_doctypes(doc)

	frappe.clear_cache()


def _get_or_create_dimension(dimension):
	existing = frappe.db.get_value(
		"Accounting Dimension",
		{"document_type": dimension["document_type"]},
		["name", "fieldname", "label", "disabled"],
		as_dict=True,
	)

	if existing:
		if existing.fieldname != dimension["fieldname"]:
			frappe.throw(
				_("Accounting Dimension for {0} already exists with fieldname {1}. Expected {2}.").format(
					dimension["document_type"], existing.fieldname, dimension["fieldname"]
				)
			)

		doc = frappe.get_doc("Accounting Dimension", existing.name)
		changed = False
		if doc.label != dimension["label"]:
			doc.label = dimension["label"]
			changed = True
		if doc.disabled:
			doc.disabled = 0
			changed = True
		if changed:
			doc.save(ignore_permissions=True)
		return doc

	return frappe.get_doc({
		"doctype": "Accounting Dimension",
		"document_type": dimension["document_type"],
		"label": dimension["label"],
		"fieldname": dimension["fieldname"],
		"disabled": 0,
	}).insert(ignore_permissions=True)


def _validate_dimension_conflicts(dimension, doctypes):
	for doctype in doctypes:
		try:
			field = frappe.get_meta(doctype, cached=False).get_field(dimension["fieldname"])
		except Exception:
			continue

		if not field:
			continue

		if field.fieldtype != "Link" or field.options != dimension["document_type"]:
			frappe.throw(
				_("Cannot create Accounting Dimension {0}: field {1} already exists on {2} as {3} / {4}.").format(
					dimension["label"],
					dimension["fieldname"],
					doctype,
					field.fieldtype,
					field.options,
				)
			)


def ensure_financial_dimension_workspace_links():
	for workspace_name, links in WORKSPACE_LINKS.items():
		if not frappe.db.exists("Workspace", workspace_name):
			continue

		workspace = frappe.get_doc("Workspace", workspace_name)
		existing = {
			(link.type, link.label, link.get("link_type"), link.get("link_to"))
			for link in workspace.links
		}

		changed = False
		for link in links:
			key = (link.get("type"), link.get("label"), link.get("link_type"), link.get("link_to"))
			if key in existing:
				continue

			workspace.append("links", {
				"type": link.get("type"),
				"label": link.get("label"),
				"link_type": link.get("link_type"),
				"link_to": link.get("link_to"),
				"is_query_report": link.get("is_query_report", 0),
				"hidden": 0,
				"onboard": 0,
				"link_count": 0,
			})
			changed = True

		if changed:
			workspace.save(ignore_permissions=True)
