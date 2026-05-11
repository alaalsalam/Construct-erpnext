import frappe
from frappe import _
from frappe.utils import flt


ACTUAL_QTY_FIELDS = (
	"consumed_qty",
	"measured_qty",
	"certified_qty",
	"received_qty",
	"invoiced_qty",
)

ACTUAL_AMOUNT_FIELDS = (
	"consumed_amount",
	"measurement_amount",
	"certified_amount",
	"invoiced_amount",
	"committed_amount",
)


def sync_boq_item_from_work_item(work_item_name):
	work_item = frappe.get_doc("Construction Work Item", work_item_name)
	if not work_item.construction_boq:
		return None

	boq = frappe.get_doc("Construction BOQ", work_item.construction_boq)
	row = _find_boq_item_row(boq, work_item)
	if not row:
		return None

	_sync_row(row, work_item)
	_update_boq_execution_totals(boq)
	boq.flags.ignore_validate_update_after_submit = True
	boq.save(ignore_permissions=True)
	return row.name


def sync_boq_from_work_items(construction_boq):
	boq = frappe.get_doc("Construction BOQ", construction_boq)
	relinked = relink_boq_items_to_work_items(boq.name)
	if relinked:
		boq = frappe.get_doc("Construction BOQ", construction_boq)

	work_items = frappe.get_all(
		"Construction Work Item",
		filters={"construction_boq": boq.name, "disabled": 0},
		fields=[
			"name",
			"project",
			"construction_boq",
			"boq_item_row_id",
			"wbs_element",
			"cost_code",
			"item_code",
			"description",
			"planned_quantity",
			"requested_qty",
			"ordered_qty",
			"received_qty",
			"invoiced_qty",
			"consumed_qty",
			"measured_qty",
			"certified_qty",
			"committed_amount",
			"invoiced_amount",
			"consumed_amount",
			"measurement_amount",
			"certified_amount",
			"remaining_qty",
			"actual_cost",
		],
	)
	work_item_map = {item.name: item for item in work_items}
	synced = 0

	for row in boq.items or []:
		work_item = None
		if row.get("construction_work_item"):
			work_item = work_item_map.get(row.construction_work_item)
		if not work_item:
			work_item = _match_work_item_from_row(row, work_items)
		if not work_item:
			_clear_row_execution(row)
			continue

		_sync_row(row, work_item)
		synced += 1

	_update_boq_execution_totals(boq)
	boq.flags.ignore_validate_update_after_submit = True
	boq.save(ignore_permissions=True)
	return {"boq": boq.name, "synced_rows": synced, "relinked_rows": relinked}


def relink_boq_items_to_work_items(construction_boq):
	boq = frappe.get_doc("Construction BOQ", construction_boq)
	work_items = frappe.get_all(
		"Construction Work Item",
		filters={"construction_boq": boq.name, "disabled": 0},
		fields=["name", "boq_item_row_id", "wbs_element", "cost_code", "item_code", "description"],
	)
	relinked = 0

	for row in boq.items or []:
		if row.get("construction_work_item"):
			continue
		match = _match_work_item_from_row(row, work_items)
		if match:
			row.construction_work_item = match.name
			relinked += 1

	if relinked:
		boq.flags.ignore_validate_update_after_submit = True
		boq.save(ignore_permissions=True)

	return relinked


@frappe.whitelist()
def refresh_boq_execution_summary(construction_boq):
	frappe.only_for(("System Manager", "Construction Manager", "Budget Controller"))
	return sync_boq_from_work_items(construction_boq)


@frappe.whitelist()
def refresh_proj_0002_boq_display():
	boq_name = "BOQ-PROJ-0002-001"
	if not frappe.db.exists("Construction BOQ", boq_name):
		frappe.throw(_("Construction BOQ {0} was not found.").format(boq_name))
	return sync_boq_from_work_items(boq_name)


@frappe.whitelist()
def ensure_proj_0002_boq_item_links():
	"""Create presentation Item links for PROJ-0002 BOQ rows that still need them."""
	boq_name = "BOQ-PROJ-0002-001"
	if not frappe.db.exists("Construction BOQ", boq_name):
		frappe.throw(_("Construction BOQ {0} was not found.").format(boq_name))

	boq = frappe.get_doc("Construction BOQ", boq_name)
	item_group = _get_presentation_item_group()
	unique_rows = []
	seen = set()

	for row in boq.items or []:
		key = (_clean(row.description), row.uom or "")
		if not key[0] or key in seen:
			continue
		seen.add(key)
		unique_rows.append(row)

	item_map = {}
	created = 0
	for index, row in enumerate(unique_rows, start=1):
		item_code = f"PROJ-0002-BOQ-ITEM-{index:03d}"
		if not frappe.db.exists("Item", item_code):
			item = frappe.new_doc("Item")
			item.item_code = item_code
			item.item_name = row.description[:140]
			item.item_group = item_group
			item.stock_uom = row.uom or "Nos"
			item.is_stock_item = 0
			item.is_purchase_item = 1
			item.is_sales_item = 0
			item.description = row.description
			item.insert(ignore_permissions=True)
			created += 1
		item_map[(_clean(row.description), row.uom or "")] = item_code

	linked_rows = 0
	for row in boq.items or []:
		if row.item_code:
			continue
		item_code = item_map.get((_clean(row.description), row.uom or ""))
		if not item_code:
			continue
		row.item_code = item_code
		linked_rows += 1

	if linked_rows:
		boq.flags.ignore_validate_update_after_submit = True
		boq.save(ignore_permissions=True)

	return {
		"boq": boq.name,
		"items_created": created,
		"boq_rows_linked": linked_rows,
		"work_items_updated": 0,
	}


def _find_boq_item_row(boq, work_item):
	for row in boq.items or []:
		if work_item.boq_item_row_id and row.name == work_item.boq_item_row_id:
			return row
		if row.get("construction_work_item") == work_item.name:
			return row
	return _match_work_item_from_row(None, [work_item], boq=boq)


def _match_work_item_from_row(row, work_items, boq=None):
	if row:
		for item in work_items:
			if item.get("boq_item_row_id") and item.boq_item_row_id == row.name:
				return item

		candidates = []
		for item in work_items:
			if row.cost_code and item.get("cost_code") != row.cost_code:
				continue
			if row.wbs_element and item.get("wbs_element") != row.wbs_element:
				continue
			if row.item_code and item.get("item_code") != row.item_code:
				continue
			if row.description and item.get("description"):
				if _clean(row.description) != _clean(item.description):
					continue
			candidates.append(item)
		return candidates[0] if len(candidates) == 1 else None

	if boq:
		for boq_row in boq.items or []:
			match = _match_work_item_from_row(boq_row, work_items)
			if match:
				return boq_row
	return None


def _sync_row(row, work_item):
	row.construction_work_item = work_item.name
	for fieldname in (
		"requested_qty",
		"ordered_qty",
		"received_qty",
		"invoiced_qty",
		"consumed_qty",
		"measured_qty",
		"certified_qty",
	):
		row.set(fieldname, flt(work_item.get(fieldname)))

	expected_qty = flt(row.final_quantity) or flt(row.quantity)
	actual_qty = max(flt(row.get(fieldname)) for fieldname in ACTUAL_QTY_FIELDS)
	row.remaining_qty = max(expected_qty - actual_qty, 0)

	expected_amount = flt(row.final_amount) or flt(row.amount)
	actual_amount = max(flt(work_item.get(fieldname)) for fieldname in ACTUAL_AMOUNT_FIELDS)
	if not actual_amount:
		actual_amount = flt(work_item.get("actual_cost"))

	row.actual_amount = actual_amount
	row.remaining_amount = max(expected_amount - actual_amount, 0)
	row.variance_amount = actual_amount - expected_amount
	row.variance_percent = (row.variance_amount / expected_amount * 100) if expected_amount else 0
	row.execution_status = _derive_execution_status(row, expected_qty, actual_qty)


def _clear_row_execution(row):
	for fieldname in (
		"construction_work_item",
		"requested_qty",
		"ordered_qty",
		"received_qty",
		"invoiced_qty",
		"consumed_qty",
		"measured_qty",
		"certified_qty",
		"remaining_qty",
		"actual_amount",
		"remaining_amount",
		"variance_amount",
		"variance_percent",
	):
		row.set(fieldname, None if fieldname == "construction_work_item" else 0)
	row.execution_status = "Not Started"


def _derive_execution_status(row, expected_qty, actual_qty):
	if flt(row.variance_percent) > 10:
		return "Overrun"
	if actual_qty and expected_qty and actual_qty <= expected_qty * 0.7:
		return "Underrun"
	if flt(row.certified_qty):
		return "Certified"
	if flt(row.measured_qty):
		return "Partially Measured"
	if expected_qty and flt(row.consumed_qty) >= expected_qty:
		return "Fully Consumed"
	if flt(row.consumed_qty):
		return "Partially Consumed"
	if flt(row.invoiced_qty):
		return "Invoiced"
	if flt(row.received_qty):
		return "Received"
	if flt(row.ordered_qty):
		return "Ordered"
	if flt(row.requested_qty):
		return "Requested"
	return "Not Started"


def _update_boq_execution_totals(boq):
	total_actual = 0
	total_invoiced = 0
	total_consumed = 0
	total_measured = 0
	total_certified = 0
	total_requested = 0
	total_ordered = 0

	for row in boq.items or []:
		rate = flt(row.unit_rate)
		total_requested += flt(row.requested_qty) * rate
		total_ordered += flt(row.ordered_qty) * rate
		total_invoiced += flt(row.invoiced_qty) * rate
		total_consumed += flt(row.consumed_qty) * rate
		total_measured += flt(row.measured_qty) * rate
		total_certified += flt(row.certified_qty) * rate
		total_actual += flt(row.actual_amount)

	boq.total_requested_amount = total_requested
	boq.total_ordered_amount = total_ordered
	boq.total_invoiced_amount = total_invoiced
	boq.total_consumed_amount = total_consumed
	boq.total_measured_amount = total_measured
	boq.total_certified_amount = total_certified
	boq.total_actual_cost = total_actual
	boq.variance_amount = flt(boq.total_actual_cost) - flt(boq.total_amount)
	boq.variance_percent = (
		flt(boq.variance_amount) / flt(boq.total_amount) * 100 if flt(boq.total_amount) else 0
	)


def _clean(value):
	return " ".join((value or "").strip().lower().split())


def _get_presentation_item_group():
	for item_group in ("مواد البناء", "خدمات المقاولين"):
		if frappe.db.exists("Item Group", item_group):
			return item_group
	item_group = frappe.get_all(
		"Item Group",
		filters={"is_group": 0},
		pluck="name",
		limit_page_length=1,
	)
	return item_group[0] if item_group else "All Item Groups"
