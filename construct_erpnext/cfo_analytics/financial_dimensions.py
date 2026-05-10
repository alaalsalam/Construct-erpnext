import frappe
from frappe import _


ITEM_TABLE_FIELDS = ("items", "accounts")
DIMENSION_FIELDS = ("construction_work_item", "cost_code", "unit")
PROJECT_PURCHASE_DOCTYPES = {
	"Material Request",
	"Purchase Order",
	"Purchase Receipt",
	"Purchase Invoice",
	"Stock Entry",
}


def get_dimensions_from_work_item(work_item):
	if isinstance(work_item, str):
		work_item = frappe.get_cached_doc("Construction Work Item", work_item)

	return {
		"construction_work_item": work_item.name,
		"cost_code": work_item.get("cost_code"),
		"project": work_item.get("project"),
		"cost_center": work_item.get("cost_center"),
		"construction_boq": work_item.get("construction_boq"),
		"wbs_element": work_item.get("wbs_element"),
	}


def get_dimensions_from_unit(unit):
	if isinstance(unit, str):
		unit = frappe.get_cached_doc("Unit", unit)

	return {
		"unit": unit.name,
		"real_estate_project": unit.get("real_estate_project"),
		"building": unit.get("building"),
		"floor": unit.get("floor"),
		"project": unit.get("project"),
	}


def sync_dimensions_on_doc(doc, method=None):
	if not is_sync_enabled():
		return

	for row in get_dimension_rows(doc):
		sync_dimensions_on_row(row, doc)

	validate_required_dimensions(doc)


def validate_dimension_doc(doc, method=None):
	sync_dimensions_on_doc(doc, method=method)


def sync_dimensions_on_row(row, parent_doc):
	work_item_name = row.get("construction_work_item") if hasattr(row, "get") else None
	if work_item_name and frappe.db.exists("Construction Work Item", work_item_name):
		dimensions = get_dimensions_from_work_item(work_item_name)
		set_if_empty(row, "cost_code", dimensions.get("cost_code"))
		set_if_empty(row, "project", dimensions.get("project"))
		set_if_empty(row, "cost_center", dimensions.get("cost_center"))
		set_if_empty(row, "construction_boq", dimensions.get("construction_boq"))
		set_if_empty(row, "wbs_element", dimensions.get("wbs_element"))

	unit_name = row.get("unit") if hasattr(row, "get") else None
	if unit_name and frappe.db.exists("Unit", unit_name):
		dimensions = get_dimensions_from_unit(unit_name)
		set_if_empty(row, "project", dimensions.get("project"))


def validate_required_dimensions(doc):
	settings = get_settings()
	if not settings:
		return

	messages = []
	for row in get_dimension_rows(doc):
		row_label = _("Row {0}").format(row.idx or "")
		project = row.get("project") or doc.get("project")
		is_project_purchase = doc.doctype in PROJECT_PURCHASE_DOCTYPES

		if (
			is_project_purchase
			and project
			and settings.require_work_item_on_project_purchase
			and not row.get("construction_work_item")
		):
			messages.append(_("{0}: Construction Work Item is recommended for project financial traceability.").format(row_label))

		if (
			is_project_purchase
			and project
			and settings.require_cost_code_on_project_purchase
			and not row.get("cost_code")
		):
			messages.append(_("{0}: Cost Code is recommended for project financial traceability.").format(row_label))

		if (
			settings.require_unit_on_unit_specific_cost
			and not settings.allow_blank_unit_for_project_level_cost
			and not row.get("unit")
		):
			messages.append(_("{0}: Unit is required when unit-specific cost tracking is enabled.").format(row_label))

	if messages:
		handle_dimension_messages(messages)


def handle_dimension_messages(messages):
	settings = get_settings()
	mode = settings.default_dimension_mode or "Warning"
	blocking = bool(settings.enable_dimension_blocking) or mode == "Blocking"
	warnings = bool(settings.enable_dimension_warnings) and mode != "Silent"

	message = "<br>".join(messages)
	if blocking:
		frappe.throw(message)
	if warnings:
		frappe.msgprint(message, indicator="orange", alert=True)


def get_dimension_field_map():
	field_map = {}
	for doctype in (
		"GL Entry",
		"Journal Entry Account",
		"Purchase Invoice Item",
		"Sales Invoice Item",
		"Purchase Order Item",
		"Purchase Receipt Item",
		"Material Request Item",
		"Stock Entry Detail",
		"Payment Entry",
		"Payment Entry Reference",
	):
		meta = frappe.get_meta(doctype, cached=False)
		field_map[doctype] = {
			fieldname: bool(meta.get_field(fieldname))
			for fieldname in DIMENSION_FIELDS
		}
	return field_map


def backfill_draft_document_dimensions(doc):
	if isinstance(doc, str):
		raise ValueError("Pass a document object to backfill_draft_document_dimensions.")
	if doc.docstatus != 0:
		frappe.throw(_("Financial dimension backfill is allowed only for draft documents."))

	for row in get_dimension_rows(doc):
		sync_dimensions_on_row(row, doc)
	doc.save(ignore_permissions=True)
	return doc.name


@frappe.whitelist()
def backfill_draft_dimensions(doctype, name):
	doc = frappe.get_doc(doctype, name)
	return backfill_draft_document_dimensions(doc)


def get_dimension_rows(doc):
	rows = []
	for fieldname in ITEM_TABLE_FIELDS:
		rows.extend(doc.get(fieldname) or [])
	return rows


def set_if_empty(row, fieldname, value):
	if value and hasattr(row, fieldname) and not row.get(fieldname):
		row.set(fieldname, value)


def get_settings():
	if not frappe.db.exists("DocType", "Financial Dimension Settings"):
		return None
	return frappe.get_cached_doc("Financial Dimension Settings")


def is_sync_enabled():
	settings = get_settings()
	return bool(settings and settings.enable_financial_dimension_sync)
