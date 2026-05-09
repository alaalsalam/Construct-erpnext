import frappe
from frappe import _
from frappe.utils import flt


PROCUREMENT_CHILD_TABLES = {
	"Material Request": "Material Request Item",
	"Purchase Order": "Purchase Order Item",
	"Purchase Receipt": "Purchase Receipt Item",
	"Purchase Invoice": "Purchase Invoice Item",
	"Stock Entry": "Stock Entry Detail",
}


def sync_procurement_fields_on_doc(doc):
	for row in getattr(doc, "items", None) or []:
		sync_procurement_fields_on_row(row, doc)


def sync_procurement_fields_on_row(row, parent_doc):
	work_item_name = getattr(row, "construction_work_item", None)
	if not work_item_name:
		return

	work_item = frappe.get_cached_doc("Construction Work Item", work_item_name)
	set_if_has(row, "construction_boq", work_item.construction_boq)
	set_if_has(row, "wbs_element", work_item.wbs_element)
	set_if_has(row, "cost_code", work_item.cost_code)
	set_if_has(row, "project", work_item.project)
	set_if_has(row, "construction_project", work_item.project)
	set_if_has(row, "cost_center", work_item.cost_center)

	if not getattr(row, "item_code", None) and work_item.item_code:
		set_if_has(row, "item_code", work_item.item_code)

	if hasattr(row, "site_warehouse") and not row.site_warehouse:
		row.site_warehouse = get_row_site_warehouse(row, parent_doc)

	if parent_doc.doctype in ("Material Request", "Purchase Order"):
		set_row_target_warehouse(row)


def get_row_site_warehouse(row, parent_doc):
	for fieldname in ("warehouse", "t_warehouse", "s_warehouse"):
		if getattr(row, fieldname, None):
			return row.get(fieldname)

	settings = frappe.get_cached_doc("Procurement Control Settings")
	if settings.default_site_warehouse:
		return settings.default_site_warehouse

	for fieldname in ("set_warehouse", "to_warehouse", "from_warehouse"):
		if getattr(parent_doc, fieldname, None):
			return parent_doc.get(fieldname)

	return None


def set_row_target_warehouse(row):
	if not getattr(row, "site_warehouse", None):
		return
	if hasattr(row, "warehouse") and not row.warehouse:
		row.warehouse = row.site_warehouse


def set_if_has(row, fieldname, value):
	if value and hasattr(row, fieldname):
		row.set(fieldname, value)


def recalculate_work_items_from_doc(doc):
	work_items = set()
	for row in getattr(doc, "items", None) or []:
		work_item_name = getattr(row, "construction_work_item", None)
		if work_item_name:
			work_items.add(work_item_name)

	for work_item_name in work_items:
		recalculate_work_item_procurement(work_item_name)


def recalculate_work_item_procurement(work_item_name):
	if not frappe.db.exists("Construction Work Item", work_item_name):
		return

	values = {
		"requested_qty": get_material_request_qty(work_item_name),
		"ordered_qty": get_purchase_order_qty(work_item_name),
		"received_qty": get_purchase_receipt_qty(work_item_name),
		"invoiced_qty": get_purchase_invoice_qty(work_item_name),
		"consumed_qty": get_stock_consumed_qty(work_item_name),
		"committed_amount": get_purchase_order_amount(work_item_name),
		"invoiced_amount": get_purchase_invoice_amount(work_item_name),
		"consumed_amount": get_stock_consumed_amount(work_item_name),
	}

	planned_qty, planned_amount = frappe.db.get_value(
		"Construction Work Item",
		work_item_name,
		["planned_quantity", "planned_amount"],
	)
	values["procurement_variance_qty"] = flt(planned_qty) - flt(values["ordered_qty"])
	values["procurement_variance_amount"] = flt(planned_amount) - flt(values["committed_amount"])
	values["procurement_status"] = get_procurement_status(values, planned_qty)

	frappe.db.set_value(
		"Construction Work Item",
		work_item_name,
		values,
		update_modified=False,
	)


def get_material_request_qty(work_item_name):
	return get_child_sum(
		"Material Request",
		"Material Request Item",
		"qty",
		work_item_name,
	)


def get_purchase_order_qty(work_item_name):
	return get_child_sum("Purchase Order", "Purchase Order Item", "qty", work_item_name)


def get_purchase_receipt_qty(work_item_name):
	return get_child_sum(
		"Purchase Receipt",
		"Purchase Receipt Item",
		"qty",
		work_item_name,
	)


def get_purchase_invoice_qty(work_item_name):
	return get_child_sum(
		"Purchase Invoice",
		"Purchase Invoice Item",
		"qty",
		work_item_name,
	)


def get_purchase_order_amount(work_item_name):
	return get_child_sum(
		"Purchase Order",
		"Purchase Order Item",
		"base_net_amount",
		work_item_name,
		fallback_field="base_amount",
	)


def get_purchase_invoice_amount(work_item_name):
	return get_child_sum(
		"Purchase Invoice",
		"Purchase Invoice Item",
		"base_net_amount",
		work_item_name,
		fallback_field="base_amount",
	)


def get_stock_consumed_qty(work_item_name):
	return get_stock_sum(work_item_name, "qty")


def get_stock_consumed_amount(work_item_name):
	return get_stock_sum(work_item_name, "amount")


def get_child_sum(parent_dt, child_dt, fieldname, work_item_name, fallback_field=None):
	# Only submitted parent documents are included. Cancelled and draft records are excluded.
	field_expression = f"item.{fieldname}"
	if fallback_field:
		field_expression = f"COALESCE(item.{fieldname}, item.{fallback_field})"

	result = frappe.db.sql(
		f"""
		SELECT SUM({field_expression})
		FROM `tab{child_dt}` item
		INNER JOIN `tab{parent_dt}` parent ON parent.name = item.parent
		WHERE parent.docstatus = 1
			AND item.construction_work_item = %s
		""",
		work_item_name,
	)
	return flt(result[0][0] if result else 0)


def get_stock_sum(work_item_name, fieldname):
	# Site consumption is counted from submitted Stock Entries where the row consumes from a source warehouse.
	result = frappe.db.sql(
		f"""
		SELECT SUM(item.{fieldname})
		FROM `tabStock Entry Detail` item
		INNER JOIN `tabStock Entry` parent ON parent.name = item.parent
		WHERE parent.docstatus = 1
			AND item.construction_work_item = %s
			AND IFNULL(item.s_warehouse, '') != ''
		""",
		work_item_name,
	)
	return flt(result[0][0] if result else 0)


def get_procurement_status(values, planned_qty):
	planned_qty = flt(planned_qty)
	requested = flt(values.get("requested_qty"))
	ordered = flt(values.get("ordered_qty"))
	received = flt(values.get("received_qty"))
	invoiced = flt(values.get("invoiced_qty"))

	if planned_qty and requested > planned_qty:
		return "Over Requested"
	if planned_qty and ordered > planned_qty:
		return "Over Ordered"
	if planned_qty and received > planned_qty:
		return "Over Received"
	if planned_qty and invoiced >= planned_qty:
		return "Fully Invoiced"
	if invoiced:
		return "Partially Invoiced"
	if planned_qty and received >= planned_qty:
		return "Fully Received"
	if received:
		return "Partially Received"
	if planned_qty and ordered >= planned_qty:
		return "Fully Ordered"
	if ordered:
		return "Partially Ordered"
	if planned_qty and requested >= planned_qty:
		return "Fully Requested"
	if requested:
		return "Partially Requested"
	return "Not Requested"


def get_work_item_remaining_qty(work_item, basis="requested"):
	if isinstance(work_item, str):
		work_item = frappe.get_cached_doc("Construction Work Item", work_item)

	if basis == "ordered":
		used_qty = flt(work_item.ordered_qty)
	else:
		used_qty = flt(work_item.requested_qty)

	return max(flt(work_item.planned_quantity) - used_qty, 0)


def get_work_item_material_request_qty(work_item):
	return get_work_item_remaining_qty(work_item, basis="requested")
