import json

import frappe
from frappe import _
from frappe.utils import flt, getdate, now_datetime, today


CERTIFIED_IPC_STATUSES = (
	"Approved",
	"Invoice Created",
	"Partially Paid",
	"Paid",
	"Closed",
)


@frappe.whitelist()
def create_ipc_from_measurement_book(
	measurement_book, contractor=None, period_start=None, period_end=None
):
	book = frappe.get_doc("Measurement Book", measurement_book)
	if book.status not in ("Verified", "Locked") and book.workflow_state not in (
		"Verified",
		"Locked",
	):
		frappe.throw(_("Measurement Book must be Verified or Locked before creating IPC."))

	entries = frappe.get_all(
		"Measurement Entry",
		filters={
			"measurement_book": measurement_book,
			"status": ["in", ["Verified", "Locked"]],
		},
		fields=["name"],
		order_by="creation asc",
	)
	if not entries:
		frappe.throw(_("No verified Measurement Entries found for this Measurement Book."))

	ipc = frappe.get_doc(
		{
			"doctype": "Interim Payment Certificate",
			"company": book.company,
			"project": book.project,
			"contractor": contractor or book.contractor,
			"construction_boq": book.construction_boq,
			"measurement_book": book.name,
			"certificate_number": get_next_certificate_number(book.project),
			"certificate_sequence": get_next_certificate_sequence(book.project, contractor or book.contractor),
			"period_start": period_start or book.measurement_period_start,
			"period_end": period_end or book.measurement_period_end,
			"status": "Draft",
			"workflow_state": "Draft",
		}
	)

	for entry_ref in entries:
		entry = frappe.get_doc("Measurement Entry", entry_ref.name)
		if measurement_entry_has_active_ipc(entry.name):
			continue
		ipc.append("lines", make_ipc_line(entry, ipc.retention_percent))

	if not ipc.lines:
		frappe.throw(_("All verified Measurement Entries are already linked to active IPCs."))

	ipc.insert(ignore_permissions=True)
	return ipc.name


def get_next_certificate_number(project):
	sequence = get_next_certificate_sequence(project)
	return f"IPC-{sequence:03d}"


def get_next_certificate_sequence(project, contractor=None):
	filters = {"project": project}
	if contractor:
		filters["contractor"] = contractor
	return (frappe.db.count("Interim Payment Certificate", filters) or 0) + 1


def make_ipc_line(entry, retention_percent):
	work_item = frappe.get_doc("Construction Work Item", entry.construction_work_item)
	previous_qty = get_previous_certified_qty(work_item.name)
	return {
		"measurement_entry": entry.name,
		"measurement_book": entry.measurement_book,
		"construction_work_item": work_item.name,
		"construction_boq": work_item.construction_boq,
		"wbs_element": work_item.wbs_element,
		"cost_code": work_item.cost_code,
		"item_code": work_item.item_code,
		"description": entry.description or work_item.description,
		"uom": work_item.uom,
		"boq_qty": work_item.planned_quantity,
		"previous_certified_qty": previous_qty,
		"current_measured_qty": entry.accepted_qty,
		"current_certified_qty": entry.accepted_qty,
		"unit_rate": entry.unit_rate or work_item.unit_rate,
		"retention_percent": retention_percent,
		"engineer_comment": entry.engineer_comment,
		"qs_comment": entry.qs_comment,
	}


def measurement_entry_has_active_ipc(measurement_entry, exclude_ipc=None):
	if not measurement_entry:
		return False

	linked_ipc = frappe.db.get_value(
		"Measurement Entry", measurement_entry, "interim_payment_certificate"
	)
	if linked_ipc and linked_ipc != exclude_ipc:
		docstatus = frappe.db.get_value("Interim Payment Certificate", linked_ipc, "docstatus")
		if docstatus != 2:
			return True

	line_parent = frappe.db.sql(
		"""
		SELECT line.parent
		FROM `tabInterim Payment Certificate Line` line
		INNER JOIN `tabInterim Payment Certificate` ipc ON ipc.name = line.parent
		WHERE line.measurement_entry = %(measurement_entry)s
			AND ipc.docstatus != 2
			AND (%(exclude_ipc)s IS NULL OR ipc.name != %(exclude_ipc)s)
		LIMIT 1
		""",
		{"measurement_entry": measurement_entry, "exclude_ipc": exclude_ipc},
	)
	return bool(line_parent)


def get_previous_certified_qty(work_item, exclude_ipc=None):
	return flt(
		frappe.db.sql(
			"""
			SELECT COALESCE(SUM(line.current_certified_qty), 0)
			FROM `tabInterim Payment Certificate Line` line
			INNER JOIN `tabInterim Payment Certificate` ipc ON ipc.name = line.parent
			WHERE line.construction_work_item = %(work_item)s
				AND ipc.docstatus = 1
				AND ipc.status in %(statuses)s
				AND (%(exclude_ipc)s IS NULL OR ipc.name != %(exclude_ipc)s)
			""",
			{
				"work_item": work_item,
				"statuses": CERTIFIED_IPC_STATUSES,
				"exclude_ipc": exclude_ipc,
			},
		)[0][0]
	)


def recalculate_work_item_certification(work_item):
	if not work_item:
		return

	totals = frappe.db.sql(
		"""
		SELECT
			COALESCE(SUM(line.current_certified_qty), 0) AS certified_qty,
			COALESCE(SUM(line.current_amount), 0) AS certified_amount,
			MAX(ipc.period_end) AS last_certification_date,
			MAX(ipc.name) AS last_ipc
		FROM `tabInterim Payment Certificate Line` line
		INNER JOIN `tabInterim Payment Certificate` ipc ON ipc.name = line.parent
		WHERE line.construction_work_item = %(work_item)s
			AND ipc.docstatus = 1
			AND ipc.status in %(statuses)s
		""",
		{"work_item": work_item, "statuses": CERTIFIED_IPC_STATUSES},
		as_dict=True,
	)[0]

	planned_quantity = flt(
		frappe.db.get_value("Construction Work Item", work_item, "planned_quantity")
	)
	certified_qty = flt(totals.certified_qty)
	status = "Not Certified"
	if planned_quantity and certified_qty > planned_quantity:
		status = "Over Certified"
	elif planned_quantity and certified_qty == planned_quantity:
		status = "Fully Certified"
	elif certified_qty > 0:
		status = "Partially Certified"

	frappe.db.set_value(
		"Construction Work Item",
		work_item,
		{
			"certified_qty": certified_qty,
			"certified_amount": flt(totals.certified_amount),
			"certification_progress_percent": (
				certified_qty / planned_quantity * 100 if planned_quantity else 0
			),
			"certification_status": status,
			"last_certification_date": totals.last_certification_date,
			"last_ipc": totals.last_ipc,
			"remaining_qty": planned_quantity - certified_qty,
			"progress_percent": certified_qty / planned_quantity * 100
			if planned_quantity
			else 0,
		},
		update_modified=False,
	)


def recalculate_work_items_from_ipc(ipc):
	work_items = {line.construction_work_item for line in ipc.lines if line.construction_work_item}
	for work_item in work_items:
		recalculate_work_item_certification(work_item)


def update_payment_status_from_purchase_invoice(ipc_name):
	ipc = frappe.get_doc("Interim Payment Certificate", ipc_name)
	ipc.update_payment_status()
	ipc.save(ignore_permissions=True)
	return ipc.status


def parse_work_items(work_items):
	if isinstance(work_items, str):
		return json.loads(work_items)
	return work_items or []
