import json

import frappe
from frappe import _
from frappe.utils import flt, getdate, today


ACTIVE_AGREEMENT_STATUSES = ("Authorized", "Approved", "Active")
FINAL_AGREEMENT_STATUSES = ("Completed", "Closed", "Cancelled")
CERTIFIED_IPC_STATUSES = (
	"Approved",
	"Invoice Created",
	"Partially Paid",
	"Paid",
	"Closed",
)


def normalize_work_items(work_items):
	if isinstance(work_items, str):
		work_items = json.loads(work_items)
	return [row for row in (work_items or []) if row]


def get_or_create_contractor_agreement(project, contractor, construction_boq=None):
	filters = {
		"project": project,
		"contractor": contractor,
		"contract_status": ["in", ACTIVE_AGREEMENT_STATUSES],
		"docstatus": ["!=", 2],
	}
	if construction_boq:
		filters["construction_boq"] = construction_boq

	existing = frappe.get_all("Subcontract", filters=filters, pluck="name", limit=1)
	if existing:
		return existing[0]

	return create_agreement_from_work_items(
		project=project,
		contractor=contractor,
		work_items=[],
		construction_boq=construction_boq,
	)


@frappe.whitelist()
def create_agreement_from_work_items(
	project, contractor, work_items=None, agreement_type="Unit Rate", construction_boq=None
):
	work_items = normalize_work_items(work_items)
	if not project or not contractor:
		frappe.throw(_("Project and Contractor are required."))

	company = frappe.db.get_value("Project", project, "company") or frappe.defaults.get_user_default(
		"Company"
	)
	if not company:
		frappe.throw(_("Company is required to create Contractor Agreement."))

	agreement = frappe.new_doc("Subcontract")
	agreement.company = company
	agreement.project = project
	agreement.contractor = contractor
	agreement.contract_title = _("Contractor Agreement for {0}").format(contractor)
	agreement.agreement_date = today()
	agreement.agreement_type = agreement_type or "Unit Rate"
	agreement.construction_boq = construction_boq
	agreement.contract_status = "Draft"
	agreement.workflow_state = "Draft"
	agreement.retention_percent = 10

	for work_item_name in work_items:
		work_item = frappe.get_doc("Construction Work Item", work_item_name)
		append_agreement_item_from_work_item(agreement, work_item)

	recalculate_agreement_totals(agreement)
	agreement.insert(ignore_permissions=True)
	return agreement.name


def append_agreement_item_from_work_item(agreement, work_item):
	validate_work_item_assignment(work_item.name, agreement.name if agreement.name else None)
	agreement.append(
		"activities",
		{
			"activity_name": work_item.description[:140] if work_item.description else work_item.name,
			"description": work_item.description,
			"construction_work_item": work_item.name,
			"construction_boq": work_item.construction_boq,
			"wbs_element": work_item.wbs_element,
			"cost_code": work_item.cost_code,
			"item_code": work_item.item_code,
			"uom": work_item.uom,
			"agreed_quantity": work_item.planned_quantity,
			"agreed_rate": work_item.unit_rate,
			"agreed_amount": flt(work_item.planned_quantity) * flt(work_item.unit_rate),
			"negotiated_amount": flt(work_item.planned_quantity) * flt(work_item.unit_rate),
			"item_status": "Planned",
		},
	)


def sync_agreement_items_from_work_items(agreement):
	for row in agreement.activities:
		if not row.construction_work_item:
			continue
		work_item = frappe.get_doc("Construction Work Item", row.construction_work_item)
		row.construction_boq = work_item.construction_boq
		row.wbs_element = work_item.wbs_element
		row.cost_code = work_item.cost_code
		row.item_code = work_item.item_code
		row.uom = work_item.uom
		if not row.description:
			row.description = work_item.description
		if not row.activity_name:
			row.activity_name = work_item.description[:140] if work_item.description else work_item.name
		if not flt(row.agreed_quantity):
			row.agreed_quantity = work_item.planned_quantity
		if not flt(row.agreed_rate):
			row.agreed_rate = work_item.unit_rate
		row.agreed_amount = flt(row.agreed_quantity) * flt(row.agreed_rate)
		row.negotiated_amount = row.agreed_amount


def recalculate_agreement_totals(agreement):
	recalculate_agreement_progress(agreement)
	total = sum(flt(row.agreed_amount) for row in agreement.activities)
	certified = sum(flt(row.total_certified_amount) for row in agreement.activities)
	measured = sum(flt(row.measured_qty) * flt(row.agreed_rate) for row in agreement.activities)
	invoiced = sum(flt(row.invoiced_qty) * flt(row.agreed_rate) for row in agreement.activities)

	agreement.total_agreement_amount = total
	agreement.negotiated_amount = total
	agreement.certified_amount = certified
	agreement.measured_amount = measured
	agreement.invoiced_amount = invoiced
	agreement.remaining_agreement_amount = total - certified
	agreement.remaining_amount = total - certified - flt(agreement.paid_amount)
	agreement.measured_percent = measured / total * 100 if total else 0
	agreement.certified_percent = certified / total * 100 if total else 0


def recalculate_agreement_progress(agreement):
	for row in agreement.activities:
		if not row.construction_work_item:
			continue
		progress = get_work_item_progress(row.construction_work_item, agreement.name)
		row.measured_qty = progress["measured_qty"]
		row.certified_qty = progress["certified_qty"]
		row.invoiced_qty = progress["invoiced_qty"]
		row.previous_certified_amount = progress["previous_certified_amount"]
		row.current_certified_amount = progress["current_certified_amount"]
		row.total_certified_amount = progress["total_certified_amount"]
		row.remaining_qty = flt(row.agreed_quantity) - flt(row.certified_qty)
		row.remaining_amount = flt(row.agreed_amount) - flt(row.total_certified_amount)
		row.item_status = get_item_status(row)


def get_work_item_progress(work_item, agreement=None):
	measured_qty = 0
	for entry in frappe.get_all(
		"Measurement Entry",
		filters={
			"construction_work_item": work_item,
			"status": ["in", ["Verified", "Locked"]],
		},
		fields=["accepted_qty"],
	):
		measured_qty += flt(entry.accepted_qty)

	certified_qty = 0
	previous_certified_amount = 0
	current_certified_amount = 0
	total_certified_amount = 0
	invoiced_qty = 0
	for line in frappe.get_all(
		"Interim Payment Certificate Line",
		filters={"construction_work_item": work_item},
		fields=[
			"name",
			"parent",
			"current_certified_qty",
			"previous_certified_amount",
			"current_amount",
			"total_certified_amount",
		],
	):
		ipc = frappe.db.get_value(
			"Interim Payment Certificate",
			line.parent,
			["docstatus", "status", "subcontract", "purchase_invoice"],
			as_dict=True,
		)
		if not ipc or ipc.docstatus != 1 or ipc.status not in CERTIFIED_IPC_STATUSES:
			continue
		if agreement and ipc.subcontract and ipc.subcontract != agreement:
			continue
		certified_qty += flt(line.current_certified_qty)
		previous_certified_amount += flt(line.previous_certified_amount)
		current_certified_amount += flt(line.current_amount)
		total_certified_amount += flt(line.total_certified_amount)
		if ipc.purchase_invoice:
			invoiced_qty += flt(line.current_certified_qty)

	return {
		"measured_qty": measured_qty,
		"certified_qty": certified_qty,
		"invoiced_qty": invoiced_qty,
		"previous_certified_amount": previous_certified_amount,
		"current_certified_amount": current_certified_amount,
		"total_certified_amount": total_certified_amount,
	}


def get_item_status(row):
	agreed_qty = flt(row.agreed_quantity)
	measured_qty = flt(row.measured_qty)
	certified_qty = flt(row.certified_qty)
	if agreed_qty and certified_qty > agreed_qty:
		return "Overrun"
	if agreed_qty and certified_qty >= agreed_qty:
		return "Fully Certified"
	if certified_qty:
		return "Partially Certified"
	if measured_qty:
		return "Partially Measured"
	return "Planned"


def get_active_agreement_for_work_item(work_item):
	value = frappe.db.get_value("Construction Work Item", work_item, "subcontract")
	if value:
		status = frappe.db.get_value("Subcontract", value, ["docstatus", "contract_status"], as_dict=True)
		if status and status.docstatus != 2 and status.contract_status in ACTIVE_AGREEMENT_STATUSES:
			return value
	return None


def validate_work_item_assignment(work_item, agreement=None):
	if not work_item:
		return
	active = get_active_agreement_for_work_item(work_item)
	if active and active != agreement:
		frappe.throw(
			_("Construction Work Item {0} is already assigned to active Contractor Agreement {1}.").format(
				work_item, active
			)
		)


def link_work_items_to_agreement(agreement):
	from construct_erpnext.contractor_management.ledger_utils import get_or_create_contractor_account

	account = get_or_create_contractor_account(
		agreement.project, agreement.contractor, agreement.name, agreement.company
	)
	for row in agreement.activities:
		if not row.construction_work_item:
			continue
		frappe.db.set_value(
			"Construction Work Item",
			row.construction_work_item,
			{
				"subcontract": agreement.name,
				"contractor": agreement.contractor,
				"agreement_item_reference": row.name,
			},
			update_modified=False,
		)
	if account:
		agreement.db_set("contract_status", agreement.contract_status or "Active", update_modified=False)


def unlink_work_items_from_agreement(agreement):
	for row in agreement.activities:
		if row.construction_work_item:
			frappe.db.set_value(
				"Construction Work Item",
				row.construction_work_item,
				{"subcontract": None, "contractor": None, "agreement_item_reference": None},
				update_modified=False,
			)


def update_agreement_from_measurement_entry(measurement_entry):
	entry = frappe.get_doc("Measurement Entry", measurement_entry) if isinstance(measurement_entry, str) else measurement_entry
	agreement_name = entry.subcontract or frappe.db.get_value(
		"Construction Work Item", entry.construction_work_item, "subcontract"
	)
	if not agreement_name:
		return
	agreement = frappe.get_doc("Subcontract", agreement_name)
	recalculate_agreement_totals(agreement)
	agreement.save(ignore_permissions=True)


def update_agreement_from_ipc(ipc):
	ipc = frappe.get_doc("Interim Payment Certificate", ipc) if isinstance(ipc, str) else ipc
	agreements = {ipc.subcontract} if ipc.subcontract else set()
	for line in ipc.lines:
		if line.subcontract:
			agreements.add(line.subcontract)
		elif line.construction_work_item:
			value = frappe.db.get_value("Construction Work Item", line.construction_work_item, "subcontract")
			if value:
				agreements.add(value)
	for agreement_name in filter(None, agreements):
		agreement = frappe.get_doc("Subcontract", agreement_name)
		recalculate_agreement_totals(agreement)
		agreement.save(ignore_permissions=True)


@frappe.whitelist()
def refresh_contractor_agreement(agreement):
	doc = frappe.get_doc("Subcontract", agreement)
	sync_agreement_items_from_work_items(doc)
	recalculate_agreement_totals(doc)
	doc.save(ignore_permissions=True)
	return doc.name

