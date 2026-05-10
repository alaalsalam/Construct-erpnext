import frappe


RESERVATION_WORKFLOW_NAME = "Unit Reservation Workflow"
RESERVATION_STATES = ["Draft", "Reserved", "Converted", "Expired", "Cancelled"]
RESERVATION_ACTIONS = ["Reserve", "Convert", "Expire", "Cancel"]


def after_migrate():
	ensure_unit_reservation_workflow()


def ensure_unit_reservation_workflow():
	if not frappe.db.exists("DocType", "Unit Reservation"):
		return

	ensure_workflow_masters()
	if frappe.db.exists("Workflow", RESERVATION_WORKFLOW_NAME):
		return

	roles = [
		role
		for role in ("System Manager", "Sales Manager", "Projects Manager")
		if frappe.db.exists("Role", role)
	]
	if not roles:
		roles = ["System Manager"]

	def allowed_role(preferred, fallback="System Manager"):
		return preferred if preferred in roles else fallback

	workflow = frappe.get_doc(
		{
			"doctype": "Workflow",
			"workflow_name": RESERVATION_WORKFLOW_NAME,
			"document_type": "Unit Reservation",
			"workflow_state_field": "workflow_state",
			"is_active": 1,
			"send_email_alert": 0,
			"states": [
				{"state": "Draft", "doc_status": "0", "allow_edit": allowed_role("Sales Manager")},
				{"state": "Reserved", "doc_status": "1", "allow_edit": allowed_role("Sales Manager")},
				{"state": "Converted", "doc_status": "1", "allow_edit": "System Manager"},
				{"state": "Expired", "doc_status": "1", "allow_edit": "System Manager"},
				{"state": "Cancelled", "doc_status": "2", "allow_edit": "System Manager"},
			],
			"transitions": [
				{"state": "Draft", "action": "Reserve", "next_state": "Reserved", "allowed": allowed_role("Sales Manager")},
				{"state": "Draft", "action": "Reserve", "next_state": "Reserved", "allowed": "System Manager"},
				{"state": "Reserved", "action": "Convert", "next_state": "Converted", "allowed": allowed_role("Sales Manager")},
				{"state": "Reserved", "action": "Convert", "next_state": "Converted", "allowed": "System Manager"},
				{"state": "Reserved", "action": "Expire", "next_state": "Expired", "allowed": "System Manager"},
				{"state": "Reserved", "action": "Cancel", "next_state": "Cancelled", "allowed": allowed_role("Sales Manager")},
				{"state": "Reserved", "action": "Cancel", "next_state": "Cancelled", "allowed": "System Manager"},
			],
		}
	)
	workflow.insert(ignore_permissions=True)


def ensure_workflow_masters():
	for state in RESERVATION_STATES:
		if not frappe.db.exists("Workflow State", state):
			frappe.get_doc({"doctype": "Workflow State", "workflow_state_name": state}).insert(
				ignore_permissions=True
			)

	for action in RESERVATION_ACTIONS:
		if not frappe.db.exists("Workflow Action Master", action):
			frappe.get_doc({"doctype": "Workflow Action Master", "workflow_action_name": action}).insert(
				ignore_permissions=True
			)
