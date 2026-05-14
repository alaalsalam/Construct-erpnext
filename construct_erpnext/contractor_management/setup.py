import frappe


WORKFLOW_NAME = "Contractor Agreement Approval Workflow"
WORKFLOW_STATES = [
	"Draft",
	"Under Review",
	"Approved",
	"Active",
	"Completed",
	"Cancelled",
	"Closed",
]
WORKFLOW_ACTIONS = [
	"Submit for Review",
	"Approve",
	"Activate",
	"Mark Completed",
	"Cancel",
	"Close",
]


def after_migrate():
	ensure_contractor_agreement_workflow()


def ensure_contractor_agreement_workflow():
	if not frappe.db.exists("DocType", "Subcontract"):
		return

	ensure_workflow_masters()

	if frappe.db.exists("Workflow", WORKFLOW_NAME):
		return

	roles = [
		role
		for role in (
			"System Manager",
			"Projects Manager",
			"Construction Manager",
			"Accounts Manager",
			"QS Engineer",
		)
		if frappe.db.exists("Role", role)
	]
	if not roles:
		roles = ["System Manager"]

	def allowed_role(preferred, fallback="System Manager"):
		return preferred if preferred in roles else fallback

	workflow = frappe.get_doc(
		{
			"doctype": "Workflow",
			"workflow_name": WORKFLOW_NAME,
			"document_type": "Subcontract",
			"workflow_state_field": "workflow_state",
			"is_active": 1,
			"send_email_alert": 0,
			"states": [
				{"state": "Draft", "doc_status": "0", "allow_edit": "System Manager"},
				{"state": "Under Review", "doc_status": "0", "allow_edit": allowed_role("Construction Manager")},
				{"state": "Approved", "doc_status": "1", "allow_edit": allowed_role("Projects Manager")},
				{"state": "Active", "doc_status": "1", "allow_edit": allowed_role("Projects Manager")},
				{"state": "Completed", "doc_status": "1", "allow_edit": allowed_role("Accounts Manager")},
				{"state": "Cancelled", "doc_status": "2", "allow_edit": "System Manager"},
				{"state": "Closed", "doc_status": "1", "allow_edit": "System Manager"},
			],
			"transitions": [
				{"state": "Draft", "action": "Submit for Review", "next_state": "Under Review", "allowed": allowed_role("Construction Manager")},
				{"state": "Draft", "action": "Submit for Review", "next_state": "Under Review", "allowed": "System Manager"},
				{"state": "Under Review", "action": "Approve", "next_state": "Approved", "allowed": allowed_role("Projects Manager")},
				{"state": "Under Review", "action": "Approve", "next_state": "Approved", "allowed": "System Manager"},
				{"state": "Approved", "action": "Activate", "next_state": "Active", "allowed": allowed_role("Projects Manager")},
				{"state": "Approved", "action": "Activate", "next_state": "Active", "allowed": "System Manager"},
				{"state": "Active", "action": "Mark Completed", "next_state": "Completed", "allowed": allowed_role("Projects Manager")},
				{"state": "Approved", "action": "Cancel", "next_state": "Cancelled", "allowed": "System Manager"},
				{"state": "Completed", "action": "Close", "next_state": "Closed", "allowed": "System Manager"},
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
