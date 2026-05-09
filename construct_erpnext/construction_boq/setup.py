import frappe


WORKFLOW_NAME = "Construction BOQ Approval Workflow"
WORKFLOW_STATES = ["Draft", "Under Review", "Approved", "Locked", "Cancelled"]
WORKFLOW_ACTIONS = ["Submit for Review", "Approve", "Lock", "Cancel"]


def ensure_construction_boq_workflow():
	if not frappe.db.exists("DocType", "Construction BOQ"):
		return

	ensure_workflow_masters()

	if frappe.db.exists("Workflow", WORKFLOW_NAME):
		return

	workflow = frappe.get_doc(
		{
			"doctype": "Workflow",
			"workflow_name": WORKFLOW_NAME,
			"document_type": "Construction BOQ",
			"workflow_state_field": "workflow_state",
			"is_active": 1,
			"send_email_alert": 0,
			"states": [
				workflow_state("Draft", "0", "System Manager", "Primary"),
				workflow_state("Under Review", "0", "Projects Manager", "Warning"),
				workflow_state("Approved", "1", "Accounts Manager", "Success"),
				workflow_state("Locked", "1", "System Manager", "Success"),
				workflow_state("Cancelled", "0", "System Manager", "Danger"),
			],
			"transitions": [
				workflow_transition(
					"Draft", "Submit for Review", "Under Review", "System Manager"
				),
				workflow_transition(
					"Draft", "Submit for Review", "Under Review", "Construction Manager"
				),
				workflow_transition("Under Review", "Approve", "Approved", "Projects Manager"),
				workflow_transition("Under Review", "Approve", "Approved", "System Manager"),
				workflow_transition("Approved", "Lock", "Locked", "Accounts Manager"),
				workflow_transition("Approved", "Lock", "Locked", "System Manager"),
				workflow_transition("Draft", "Cancel", "Cancelled", "System Manager"),
				workflow_transition("Under Review", "Cancel", "Cancelled", "System Manager"),
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
			frappe.get_doc({"doctype": "Workflow Action Master", "workflow_action_name": action}).insert(
				ignore_permissions=True
			)


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
