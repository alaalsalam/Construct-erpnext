import frappe


WORKFLOW_NAME = "Lease Contract Approval Workflow"
WORKFLOW_STATES = [
	"Draft",
	"Under Review",
	"Approved",
	"Active",
	"Expired",
	"Terminated",
	"Cancelled",
	"Closed",
]
WORKFLOW_ACTIONS = [
	"Submit for Review",
	"Approve",
	"Activate",
	"Mark Expired",
	"Terminate",
	"Cancel",
	"Close",
	"Return to Draft",
]


def after_migrate():
	ensure_lease_contract_settings()
	ensure_lease_contract_workflow()


def ensure_lease_contract_settings():
	if not frappe.db.exists("DocType", "Lease Contract Settings"):
		return

	settings = frappe.get_single("Lease Contract Settings")
	defaults = {
		"default_lease_period_months": 12,
		"contract_number_prefix": "LC",
		"default_billing_frequency": "Monthly",
		"default_security_deposit_months": 0,
		"allow_duplicate_active_lease_for_unit": 0,
		"require_customer": 1,
		"require_rent_schedule": 1,
		"allow_backdated_lease": 1,
		"mark_unit_rented_on_activation": 1,
		"enable_rent_invoice_generation": 0,
		"auto_generate_rent_schedule": 1,
		"use_company_default_currency": 1,
	}
	changed = False
	for fieldname, value in defaults.items():
		if not frappe.db.exists(
			"Singles",
			{"doctype": "Lease Contract Settings", "field": fieldname},
		):
			settings.set(fieldname, value)
			changed = True
	if changed:
		settings.save(ignore_permissions=True)


def ensure_lease_contract_workflow():
	if not frappe.db.exists("DocType", "Lease Contract"):
		return

	ensure_workflow_masters()

	if frappe.db.exists("Workflow", WORKFLOW_NAME):
		workflow = frappe.get_doc("Workflow", WORKFLOW_NAME)
		if _workflow_is_valid(workflow):
			return
		frappe.delete_doc("Workflow", WORKFLOW_NAME, ignore_permissions=True, force=True)

	roles = [
		role
		for role in ("System Manager", "Sales Manager", "Accounts Manager", "Projects Manager")
		if frappe.db.exists("Role", role)
	]
	if "System Manager" not in roles:
		roles.insert(0, "System Manager")

	def allowed_role(preferred, fallback="System Manager"):
		return preferred if preferred in roles else fallback

	workflow = frappe.get_doc(
		{
			"doctype": "Workflow",
			"workflow_name": WORKFLOW_NAME,
			"document_type": "Lease Contract",
			"workflow_state_field": "workflow_state",
			"is_active": 1,
			"send_email_alert": 0,
			"states": [
				workflow_state("Draft", "0", allowed_role("Sales Manager"), "Warning"),
				workflow_state("Under Review", "0", allowed_role("Sales Manager"), "Primary"),
				workflow_state("Approved", "1", allowed_role("Accounts Manager"), "Success"),
				workflow_state("Active", "1", allowed_role("Sales Manager"), "Success"),
				workflow_state("Expired", "1", "System Manager", "Secondary"),
				workflow_state("Terminated", "1", "System Manager", "Danger"),
				workflow_state("Cancelled", "2", "System Manager", "Danger"),
				workflow_state("Closed", "1", "System Manager", "Secondary"),
			],
			"transitions": [
				workflow_transition("Draft", "Submit for Review", "Under Review", allowed_role("Sales Manager")),
				workflow_transition("Draft", "Submit for Review", "Under Review", "System Manager"),
				workflow_transition("Under Review", "Approve", "Approved", allowed_role("Accounts Manager")),
				workflow_transition("Under Review", "Approve", "Approved", "System Manager"),
				workflow_transition("Under Review", "Return to Draft", "Draft", "System Manager"),
				workflow_transition("Approved", "Activate", "Active", allowed_role("Sales Manager")),
				workflow_transition("Approved", "Activate", "Active", "System Manager"),
				workflow_transition("Active", "Mark Expired", "Expired", "System Manager"),
				workflow_transition("Active", "Terminate", "Terminated", "System Manager"),
				workflow_transition("Approved", "Cancel", "Cancelled", "System Manager"),
				workflow_transition("Expired", "Close", "Closed", "System Manager"),
				workflow_transition("Terminated", "Close", "Closed", "System Manager"),
			],
		}
	)
	workflow.insert(ignore_permissions=True)


def ensure_workflow_masters():
	for state in WORKFLOW_STATES:
		if not frappe.db.exists("Workflow State", state):
			frappe.get_doc({"doctype": "Workflow State", "workflow_state_name": state}).insert(
				ignore_permissions=True
			)

	for action in WORKFLOW_ACTIONS:
		if not frappe.db.exists("Workflow Action Master", action):
			frappe.get_doc(
				{"doctype": "Workflow Action Master", "workflow_action_name": action}
			).insert(ignore_permissions=True)


def workflow_state(state, doc_status, allow_edit, style):
	return {
		"state": state,
		"doc_status": doc_status,
		"allow_edit": allow_edit,
		"style": style,
	}


def workflow_transition(state, action, next_state, allowed):
	return {
		"state": state,
		"action": action,
		"next_state": next_state,
		"allowed": allowed,
	}


def _workflow_is_valid(workflow):
	if workflow.document_type != "Lease Contract":
		return False
	if workflow.workflow_state_field != "workflow_state":
		return False

	expected_states = set(WORKFLOW_STATES)
	actual_states = {row.state for row in workflow.states}
	if expected_states - actual_states:
		return False

	expected_transitions = {
		("Draft", "Submit for Review", "Under Review"),
		("Under Review", "Approve", "Approved"),
		("Approved", "Activate", "Active"),
		("Active", "Mark Expired", "Expired"),
		("Active", "Terminate", "Terminated"),
		("Approved", "Cancel", "Cancelled"),
		("Expired", "Close", "Closed"),
		("Terminated", "Close", "Closed"),
	}
	actual_transitions = {(row.state, row.action, row.next_state) for row in workflow.transitions}
	return not (expected_transitions - actual_transitions)
