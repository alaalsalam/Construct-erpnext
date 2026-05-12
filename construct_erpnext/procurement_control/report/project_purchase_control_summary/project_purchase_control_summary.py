import frappe
from frappe import _
from frappe.utils import flt
from construct_erpnext.reporting.report_utils import count_where, sum_field, summary_value


def execute(filters=None):
	filters = frappe._dict(filters or {})
	data = get_data(filters)
	return get_columns(), data, None, None, None, False


def get_columns():
	return [
		{"label": _("Work Item"), "fieldname": "work_item", "fieldtype": "Link", "options": "Construction Work Item", "width": 150},
		{"label": _("Description"), "fieldname": "description", "fieldtype": "Data", "width": 220},
		{"label": _("Cost Code"), "fieldname": "cost_code", "fieldtype": "Link", "options": "Cost Code", "width": 120},
		{"label": _("WBS"), "fieldname": "wbs_element", "fieldtype": "Link", "options": "WBS Element", "width": 120},
		{"label": _("Item"), "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 120},
		{"label": _("Planned Qty"), "fieldname": "planned_qty", "fieldtype": "Float", "width": 105},
		{"label": _("Wastage %"), "fieldname": "wastage_percent", "fieldtype": "Percent", "width": 95},
		{"label": _("Expected Qty"), "fieldname": "expected_qty", "fieldtype": "Float", "width": 105},
		{"label": _("Requested Qty"), "fieldname": "requested_qty", "fieldtype": "Float", "width": 110},
		{"label": _("Ordered Qty"), "fieldname": "ordered_qty", "fieldtype": "Float", "width": 105},
		{"label": _("Received Qty"), "fieldname": "received_qty", "fieldtype": "Float", "width": 110},
		{"label": _("Invoiced Qty"), "fieldname": "invoiced_qty", "fieldtype": "Float", "width": 110},
		{"label": _("Consumed Qty"), "fieldname": "consumed_qty", "fieldtype": "Float", "width": 115},
		{"label": _("Measured Qty"), "fieldname": "measured_qty", "fieldtype": "Float", "width": 115},
		{"label": _("Certified Qty"), "fieldname": "certified_qty", "fieldtype": "Float", "width": 115},
		{"label": _("Remaining Qty"), "fieldname": "remaining_qty", "fieldtype": "Float", "width": 115},
		{"label": _("Planned Amount"), "fieldname": "planned_amount", "fieldtype": "Currency", "width": 125},
		{"label": _("Actual Amount"), "fieldname": "actual_amount", "fieldtype": "Currency", "width": 125},
		{"label": _("Remaining Amount"), "fieldname": "remaining_amount", "fieldtype": "Currency", "width": 135},
		{"label": _("Variance Amount"), "fieldname": "variance_amount", "fieldtype": "Currency", "width": 130},
		{"label": _("Variance %"), "fieldname": "variance_percent", "fieldtype": "Percent", "width": 105},
		{"label": _("Execution Status"), "fieldname": "execution_status", "fieldtype": "Data", "width": 135},
		{"label": _("Risk Status"), "fieldname": "risk_status", "fieldtype": "Data", "width": 110},
	]


def get_data(filters):
	conditions = {"disabled": 0}
	for fieldname in ("project", "construction_boq", "cost_code", "wbs_element", "item_category"):
		if filters.get(fieldname):
			conditions[fieldname] = filters.get(fieldname)

	work_items = frappe.get_all(
		"Construction Work Item",
		filters=conditions,
		fields=[
			"name",
			"construction_boq",
			"boq_item_row_id",
			"description",
			"cost_code",
			"wbs_element",
			"item_code",
			"planned_quantity",
			"unit_rate",
			"planned_amount",
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
		],
		order_by="construction_boq, wbs_element, cost_code, name",
	)

	boq_rows = _get_boq_rows(work_items)
	data = []
	for item in work_items:
		boq_row = boq_rows.get((item.construction_boq, item.boq_item_row_id)) or {}
		expected_qty = flt(boq_row.get("final_quantity")) or flt(item.planned_quantity)
		planned_amount = flt(boq_row.get("final_amount")) or flt(item.planned_amount)
		actual_amount = max(
			flt(item.consumed_amount),
			flt(item.measurement_amount),
			flt(item.certified_amount),
			flt(item.invoiced_amount),
			flt(item.committed_amount),
		)
		actual_qty = max(
			flt(item.consumed_qty),
			flt(item.measured_qty),
			flt(item.certified_qty),
			flt(item.received_qty),
			flt(item.invoiced_qty),
		)
		remaining_qty = max(expected_qty - actual_qty, 0)
		variance_amount = actual_amount - planned_amount
		variance_percent = (variance_amount / planned_amount * 100) if planned_amount else 0
		execution_status = _derive_execution_status(item, expected_qty, actual_qty, variance_percent)
		if filters.get("execution_status") and execution_status != filters.execution_status:
			continue

		data.append({
			"work_item": item.name,
			"description": item.description,
			"cost_code": item.cost_code,
			"wbs_element": item.wbs_element,
			"item_code": item.item_code or boq_row.get("item_code"),
			"planned_qty": flt(item.planned_quantity),
			"wastage_percent": flt(boq_row.get("wastage_percent")),
			"expected_qty": expected_qty,
			"requested_qty": flt(item.requested_qty),
			"ordered_qty": flt(item.ordered_qty),
			"received_qty": flt(item.received_qty),
			"invoiced_qty": flt(item.invoiced_qty),
			"consumed_qty": flt(item.consumed_qty),
			"measured_qty": flt(item.measured_qty),
			"certified_qty": flt(item.certified_qty),
			"remaining_qty": remaining_qty,
			"planned_amount": planned_amount,
			"actual_amount": actual_amount,
			"remaining_amount": max(planned_amount - actual_amount, 0),
			"variance_amount": variance_amount,
			"variance_percent": variance_percent,
			"execution_status": execution_status,
			"risk_status": _risk_status(execution_status, variance_percent, actual_qty, expected_qty),
		})
	return data


def _get_boq_rows(work_items):
	row_names = [item.boq_item_row_id for item in work_items if item.boq_item_row_id]
	if not row_names:
		return {}
	rows = frappe.get_all(
		"Construction BOQ Item",
		filters={"name": ["in", row_names]},
		fields=[
			"name",
			"parent",
			"wastage_percent",
			"final_quantity",
			"final_amount",
			"item_code",
		],
	)
	return {(row.parent, row.name): row for row in rows}


def _derive_execution_status(item, expected_qty, actual_qty, variance_percent):
	if variance_percent > 10:
		return "Overrun"
	if actual_qty and expected_qty and actual_qty <= expected_qty * 0.7:
		return "Underrun"
	if flt(item.certified_qty):
		return "Certified"
	if flt(item.measured_qty):
		return "Partially Measured"
	if expected_qty and flt(item.consumed_qty) >= expected_qty:
		return "Fully Consumed"
	if flt(item.consumed_qty):
		return "Partially Consumed"
	if flt(item.invoiced_qty):
		return "Invoiced"
	if flt(item.received_qty):
		return "Received"
	if flt(item.ordered_qty):
		return "Ordered"
	if flt(item.requested_qty):
		return "Requested"
	return "Not Started"


def _risk_status(execution_status, variance_percent, actual_qty, expected_qty):
	if execution_status == "Overrun":
		return "Overrun"
	if execution_status == "Underrun":
		return "Underrun"
	if execution_status == "Not Started":
		return "Not Started"
	if variance_percent > 0 or (expected_qty and actual_qty > expected_qty):
		return "Watch"
	return "Normal"


def get_report_summary(data):
	return [
		summary_value("Planned Amount", sum_field(data, "planned_amount"), "Currency", "Blue"),
		summary_value("Actual Amount", sum_field(data, "actual_amount"), "Currency", "Orange"),
		summary_value("Remaining Amount", sum_field(data, "remaining_amount"), "Currency", "Blue"),
		summary_value("Overrun Items", count_where(data, "risk_status", "Overrun"), "Int", "Red"),
		summary_value("Underrun Items", count_where(data, "risk_status", "Underrun"), "Int", "Orange"),
		summary_value("Not Started Items", count_where(data, "risk_status", "Not Started"), "Int", "Grey"),
	]
