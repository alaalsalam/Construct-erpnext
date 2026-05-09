import frappe
from frappe import _
from frappe.utils import flt

from construct_erpnext.procurement_control.work_item_sync import (
	recalculate_work_items_from_doc,
	sync_procurement_fields_on_doc,
)


def validate_procurement_doc(doc, method=None):
	if not is_sync_enabled():
		return

	sync_procurement_fields_on_doc(doc)
	validate_required_work_items(doc)


def validate_purchase_order(doc, method=None):
	validate_procurement_doc(doc, method=method)
	if is_budget_warning_enabled() or is_budget_blocking_enabled():
		validate_purchase_order_budget(doc)


def recalculate_procurement_doc(doc, method=None):
	if not is_sync_enabled():
		return

	recalculate_work_items_from_doc(doc)


def validate_required_work_items(doc):
	settings = get_settings()
	if not settings.require_work_item_on_project_purchase:
		return

	for row in get_rows(doc):
		if getattr(row, "project", None) and not getattr(row, "construction_work_item", None):
			frappe.throw(
				_("Row {0}: Construction Work Item is required for project procurement.").format(
					row.idx
				)
			)


def validate_purchase_order_budget(doc):
	for row in get_rows(doc):
		work_item_name = getattr(row, "construction_work_item", None)
		if not work_item_name:
			continue

		work_item = frappe.get_doc("Construction Work Item", work_item_name)
		planned_amount = flt(work_item.planned_amount)
		row_amount = get_row_amount(row)
		current_committed = flt(work_item.committed_amount)
		projected_amount = current_committed + row_amount
		tolerance_amount = planned_amount * flt(get_settings().overrun_tolerance_percent) / 100
		allowed_amount = planned_amount + tolerance_amount

		if planned_amount and projected_amount > allowed_amount:
			message = _(
				"Row {0}: Purchase Order amount may exceed planned Work Item amount for {1}."
			).format(row.idx, work_item_name)
			if is_budget_blocking_enabled():
				frappe.throw(message)
			if is_budget_warning_enabled():
				frappe.msgprint(message, indicator="orange", alert=True)


def get_rows(doc):
	return getattr(doc, "items", None) or []


def get_row_amount(row):
	for fieldname in ("base_net_amount", "base_amount", "net_amount", "amount"):
		if hasattr(row, fieldname):
			return flt(row.get(fieldname))
	return flt(row.get("qty")) * flt(row.get("rate"))


def get_settings():
	return frappe.get_cached_doc("Procurement Control Settings")


def is_sync_enabled():
	return bool(get_settings().enable_work_item_sync)


def is_budget_warning_enabled():
	return bool(get_settings().enable_budget_warning)


def is_budget_blocking_enabled():
	return bool(get_settings().enable_budget_blocking)
