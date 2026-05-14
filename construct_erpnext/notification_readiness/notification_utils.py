import frappe
from frappe import _
from frappe.utils import today


DEFAULT_SETTINGS = [
	("Reservation Expiry", "Unit Reservation", 3),
	("Installment Due", "Sales Contract", 7),
	("Rent Due", "Lease Contract", 7),
	("Lease Expiry", "Lease Contract", 30),
	("Document Expiry", "Property Document", 30),
	("Backlog Matched Unit", "Backlog Request", 1),
]


def ensure_default_reminder_settings():
	for scenario, target_doctype, lead_days in DEFAULT_SETTINGS:
		existing = frappe.db.exists("Reminder Setting", {"scenario": scenario})
		doc = frappe.get_doc("Reminder Setting", existing) if existing else frappe.new_doc("Reminder Setting")
		doc.scenario = scenario
		doc.status = doc.status or "Enabled"
		if not existing or not doc.lead_days or doc.lead_days == 7:
			doc.lead_days = lead_days
		doc.channel = doc.channel or "Internal Log"
		doc.target_doctype = target_doctype
		doc.message_template = doc.message_template or _("Review {scenario} for {source_document}.")
		doc.last_evaluated_on = today()
		doc.save(ignore_permissions=True)


@frappe.whitelist()
def create_phase_j_validation_data():
	ensure_default_reminder_settings()
	logs = []
	logs.append(_log_for_reservation_expiry())
	logs.append(_log_for_installment_due())
	logs.append(_log_for_rent_due())
	logs.append(_log_for_lease_expiry())
	logs.append(_log_for_document_expiry())
	logs.append(_log_for_backlog())
	return {"automation_logs": [row for row in logs if row]}


def _get_or_create_log(scenario, source_doctype, source_document, **kwargs):
	if not source_document:
		return None
	existing = frappe.db.exists("Automation Log", {"scenario": scenario, "source_doctype": source_doctype, "source_document": source_document})
	doc = frappe.get_doc("Automation Log", existing) if existing else frappe.new_doc("Automation Log")
	doc.scenario = scenario
	doc.status = kwargs.get("status") or "Pending"
	doc.due_date = kwargs.get("due_date")
	doc.channel = "Internal Log"
	doc.source_doctype = source_doctype
	doc.source_document = source_document
	doc.party_type = kwargs.get("party_type")
	doc.party = kwargs.get("party")
	doc.message = kwargs.get("message") or _("Prepared internal reminder. No external notification was sent.")
	doc.action_notes = kwargs.get("action_notes") or _("Ready for future automation review.")
	doc.save(ignore_permissions=True)
	return doc.name


def _log_for_reservation_expiry():
	row = frappe.db.get_value("Unit Reservation", {"real_estate_project": "REP-2026-00002"}, ["name", "customer", "lead", "valid_until"], as_dict=True)
	if not row:
		row = frappe.db.get_value("Unit Reservation", {}, ["name", "customer", "lead", "valid_until"], as_dict=True)
	if not row:
		return None
	party_type, party = ("Customer", row.customer) if row.customer else ("Lead", row.lead) if row.lead else (None, None)
	return _get_or_create_log("Reservation Expiry", "Unit Reservation", row.name, due_date=row.valid_until, party_type=party_type, party=party)


def _log_for_installment_due():
	contract = "SC-PROJ-0002-001" if frappe.db.exists("Sales Contract", "SC-PROJ-0002-001") else frappe.db.get_value("Sales Contract", {}, "name")
	if not contract:
		return None
	doc = frappe.get_doc("Sales Contract", contract)
	due_date = None
	for row in doc.get("installment_schedule") or []:
		if row.get("outstanding_amount", 0) or row.get("amount", 0):
			due_date = row.get("due_date")
			break
	return _get_or_create_log("Installment Due", "Sales Contract", doc.name, due_date=due_date, party_type="Customer", party=doc.customer)


def _log_for_rent_due():
	lease = "LC-2026-00001" if frappe.db.exists("Lease Contract", "LC-2026-00001") else frappe.db.get_value("Lease Contract", {}, "name")
	if not lease:
		return None
	doc = frappe.get_doc("Lease Contract", lease)
	due_date = None
	for row in doc.get("rent_schedule") or []:
		if row.get("outstanding_amount", 0) or row.get("rent_amount", 0):
			due_date = row.get("due_date")
			break
	return _get_or_create_log("Rent Due", "Lease Contract", doc.name, due_date=due_date, party_type="Customer", party=doc.customer)


def _log_for_lease_expiry():
	lease = "LC-2026-00001" if frappe.db.exists("Lease Contract", "LC-2026-00001") else frappe.db.get_value("Lease Contract", {}, "name")
	if not lease:
		return None
	doc = frappe.get_doc("Lease Contract", lease)
	return _get_or_create_log("Lease Expiry", "Lease Contract", doc.name, due_date=doc.lease_end_date, party_type="Customer", party=doc.customer)


def _log_for_document_expiry():
	row = frappe.db.get_value("Property Document", {"status": ["!=", "Expired"]}, ["name", "expiry_date", "customer", "supplier", "property_owner"], as_dict=True)
	if not row:
		return None
	party_type, party = (None, None)
	if row.customer:
		party_type, party = "Customer", row.customer
	elif row.supplier:
		party_type, party = "Supplier", row.supplier
	elif row.property_owner:
		party_type, party = "Property Owner", row.property_owner
	return _get_or_create_log("Document Expiry", "Property Document", row.name, due_date=row.expiry_date, party_type=party_type, party=party)


def _log_for_backlog():
	backlog = frappe.db.get_value("Backlog Request", {"status": "Active"}, "name") or frappe.db.get_value("Backlog Request", {}, "name")
	if not backlog:
		return None
	doc = frappe.get_doc("Backlog Request", backlog)
	return _get_or_create_log("Backlog Matched Unit", "Backlog Request", doc.name, due_date=today(), party_type=doc.get("party_type"), party=doc.get("party"))
