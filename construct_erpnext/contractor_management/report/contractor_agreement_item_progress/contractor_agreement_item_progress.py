import frappe
from frappe import _


def execute(filters=None):
	filters = filters or {}
	columns = [
		{"label": _("Agreement"), "fieldname": "agreement", "fieldtype": "Link", "options": "Subcontract", "width": 160},
		{"label": _("Contractor"), "fieldname": "contractor", "fieldtype": "Link", "options": "Supplier", "width": 170},
		{"label": _("Work Item"), "fieldname": "construction_work_item", "fieldtype": "Link", "options": "Construction Work Item", "width": 160},
		{"label": _("Description"), "fieldname": "description", "fieldtype": "Data", "width": 260},
		{"label": _("Cost Code"), "fieldname": "cost_code", "fieldtype": "Link", "options": "Cost Code", "width": 130},
		{"label": _("WBS"), "fieldname": "wbs_element", "fieldtype": "Link", "options": "WBS Element", "width": 130},
		{"label": _("Agreed Qty"), "fieldname": "agreed_quantity", "fieldtype": "Float", "width": 110},
		{"label": _("Measured Qty"), "fieldname": "measured_qty", "fieldtype": "Float", "width": 120},
		{"label": _("Certified Qty"), "fieldname": "certified_qty", "fieldtype": "Float", "width": 120},
		{"label": _("Remaining Qty"), "fieldname": "remaining_qty", "fieldtype": "Float", "width": 120},
		{"label": _("Agreed Amount"), "fieldname": "agreed_amount", "fieldtype": "Currency", "width": 140},
		{"label": _("Certified Amount"), "fieldname": "total_certified_amount", "fieldtype": "Currency", "width": 140},
		{"label": _("Remaining Amount"), "fieldname": "remaining_amount", "fieldtype": "Currency", "width": 140},
		{"label": _("Status"), "fieldname": "item_status", "fieldtype": "Data", "width": 130},
	]
	agreements = get_agreements(filters)
	data = []
	for agreement in agreements:
		doc = frappe.get_doc("Subcontract", agreement.name)
		for row in doc.activities:
			if filters.get("cost_code") and row.cost_code != filters.get("cost_code"):
				continue
			if filters.get("wbs_element") and row.wbs_element != filters.get("wbs_element"):
				continue
			if filters.get("item_status") and row.item_status != filters.get("item_status"):
				continue
			data.append(
				{
					"agreement": doc.name,
					"contractor": doc.contractor,
					"construction_work_item": row.construction_work_item,
					"description": row.description or row.activity_name,
					"cost_code": row.cost_code,
					"wbs_element": row.wbs_element,
					"agreed_quantity": row.agreed_quantity,
					"measured_qty": row.measured_qty,
					"certified_qty": row.certified_qty,
					"remaining_qty": row.remaining_qty,
					"agreed_amount": row.agreed_amount,
					"total_certified_amount": row.total_certified_amount,
					"remaining_amount": row.remaining_amount,
					"item_status": row.item_status,
				}
			)
	return columns, data


def get_agreements(filters):
	doc_filters = {"docstatus": ["!=", 2]}
	for field in ("project", "contractor"):
		if filters.get(field):
			doc_filters[field] = filters[field]
	if filters.get("contractor_agreement"):
		doc_filters["name"] = filters["contractor_agreement"]
	return frappe.get_all("Subcontract", filters=doc_filters, fields=["name"], order_by="project asc, contractor asc")

