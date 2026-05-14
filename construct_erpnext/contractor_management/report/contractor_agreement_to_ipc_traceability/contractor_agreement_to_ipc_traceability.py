import frappe
from frappe import _


def execute(filters=None):
	filters = filters or {}
	columns = [
		{"label": _("Agreement"), "fieldname": "agreement", "fieldtype": "Link", "options": "Subcontract", "width": 160},
		{"label": _("IPC"), "fieldname": "ipc", "fieldtype": "Link", "options": "Interim Payment Certificate", "width": 150},
		{"label": _("Work Item"), "fieldname": "construction_work_item", "fieldtype": "Link", "options": "Construction Work Item", "width": 160},
		{"label": _("Measurement Entry"), "fieldname": "measurement_entry", "fieldtype": "Link", "options": "Measurement Entry", "width": 150},
		{"label": _("Previous Certified Qty"), "fieldname": "previous_certified_qty", "fieldtype": "Float", "width": 150},
		{"label": _("Current Certified Qty"), "fieldname": "current_certified_qty", "fieldtype": "Float", "width": 150},
		{"label": _("Total Certified Qty"), "fieldname": "total_certified_qty", "fieldtype": "Float", "width": 140},
		{"label": _("Remaining Qty"), "fieldname": "remaining_qty", "fieldtype": "Float", "width": 120},
		{"label": _("Retention"), "fieldname": "retention_amount", "fieldtype": "Currency", "width": 120},
		{"label": _("Net Payable"), "fieldname": "net_line_amount", "fieldtype": "Currency", "width": 130},
	]
	ipc_filters = {"docstatus": ["!=", 2]}
	for field in ("project", "contractor"):
		if filters.get(field):
			ipc_filters[field] = filters[field]
	if filters.get("contractor_agreement"):
		ipc_filters["subcontract"] = filters["contractor_agreement"]
	if filters.get("ipc"):
		ipc_filters["name"] = filters["ipc"]
	data = []
	for ipc_ref in frappe.get_all("Interim Payment Certificate", filters=ipc_filters, fields=["name", "subcontract"], order_by="period_end desc"):
		ipc = frappe.get_doc("Interim Payment Certificate", ipc_ref.name)
		for row in ipc.lines:
			agreement = row.subcontract or ipc.subcontract
			if filters.get("contractor_agreement") and agreement != filters["contractor_agreement"]:
				continue
			data.append(
				{
					"agreement": agreement,
					"ipc": ipc.name,
					"construction_work_item": row.construction_work_item,
					"measurement_entry": row.measurement_entry,
					"previous_certified_qty": row.previous_certified_qty,
					"current_certified_qty": row.current_certified_qty,
					"total_certified_qty": row.total_certified_qty,
					"remaining_qty": row.remaining_qty,
					"retention_amount": row.retention_amount,
					"net_line_amount": row.net_line_amount,
				}
			)
	return columns, data
