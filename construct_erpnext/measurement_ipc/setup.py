import frappe


WORKFLOW_NAME = "Measurement Book Verification Workflow"
WORKFLOW_STATES = ["Draft", "Submitted", "Under Verification", "Verified", "Locked", "Cancelled"]
WORKFLOW_ACTIONS = ["Submit for Verification", "Start Verification", "Verify", "Lock", "Cancel"]

IPC_WORKFLOW_NAME = "Interim Payment Certificate Approval Workflow"
IPC_WORKFLOW_STATES = [
	"Draft",
	"Submitted",
	"Under Review",
	"Certified",
	"Approved",
	"Invoice Created",
	"Partially Paid",
	"Paid",
	"Closed",
	"Rejected",
]
IPC_WORKFLOW_ACTIONS = [
	"Submit for Review",
	"Start Review",
	"Certify",
	"Approve",
	"Mark Rejected",
	"Mark Closed",
]


def ensure_measurement_book_workflow():
	if not frappe.db.exists("DocType", "Measurement Book"):
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
			"Site Engineer",
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
			"document_type": "Measurement Book",
			"workflow_state_field": "workflow_state",
			"is_active": 1,
			"send_email_alert": 0,
			"states": [
				{"state": "Draft", "doc_status": "0", "allow_edit": "System Manager"},
				{"state": "Submitted", "doc_status": "0", "allow_edit": "System Manager"},
				{
					"state": "Under Verification",
					"doc_status": "0",
					"allow_edit": allowed_role("QS Engineer"),
				},
				{"state": "Verified", "doc_status": "1", "allow_edit": "System Manager"},
				{"state": "Locked", "doc_status": "1", "allow_edit": "System Manager"},
				{"state": "Cancelled", "doc_status": "0", "allow_edit": "System Manager"},
			],
			"transitions": [
				{
					"state": "Draft",
					"action": "Submit for Verification",
					"next_state": "Submitted",
					"allowed": allowed_role("Site Engineer"),
				},
				{
					"state": "Draft",
					"action": "Submit for Verification",
					"next_state": "Submitted",
					"allowed": "System Manager",
				},
				{
					"state": "Submitted",
					"action": "Start Verification",
					"next_state": "Under Verification",
					"allowed": allowed_role("QS Engineer"),
				},
				{
					"state": "Under Verification",
					"action": "Verify",
					"next_state": "Verified",
					"allowed": allowed_role("Projects Manager"),
				},
				{
					"state": "Under Verification",
					"action": "Verify",
					"next_state": "Verified",
					"allowed": "System Manager",
				},
				{
					"state": "Verified",
					"action": "Lock",
					"next_state": "Locked",
					"allowed": allowed_role("Projects Manager"),
				},
				{
					"state": "Verified",
					"action": "Lock",
					"next_state": "Locked",
					"allowed": "System Manager",
				},
				{
					"state": "Draft",
					"action": "Cancel",
					"next_state": "Cancelled",
					"allowed": "System Manager",
				},
				{
					"state": "Submitted",
					"action": "Cancel",
					"next_state": "Cancelled",
					"allowed": "System Manager",
				},
			],
		}
	)
	workflow.insert(ignore_permissions=True)


def ensure_interim_payment_certificate_workflow():
	if not frappe.db.exists("DocType", "Interim Payment Certificate"):
		return

	ensure_workflow_masters(IPC_WORKFLOW_STATES, IPC_WORKFLOW_ACTIONS)

	if frappe.db.exists("Workflow", IPC_WORKFLOW_NAME):
		return

	roles = [
		role
		for role in (
			"System Manager",
			"Projects Manager",
			"Accounts Manager",
			"Construction Manager",
			"QS Engineer",
			"Finance Officer",
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
			"workflow_name": IPC_WORKFLOW_NAME,
			"document_type": "Interim Payment Certificate",
			"workflow_state_field": "workflow_state",
			"is_active": 1,
			"send_email_alert": 0,
			"states": [
				{"state": "Draft", "doc_status": "0", "allow_edit": "System Manager"},
				{"state": "Submitted", "doc_status": "0", "allow_edit": "System Manager"},
				{"state": "Under Review", "doc_status": "0", "allow_edit": allowed_role("QS Engineer")},
				{"state": "Certified", "doc_status": "0", "allow_edit": allowed_role("Projects Manager")},
				{"state": "Approved", "doc_status": "1", "allow_edit": allowed_role("Accounts Manager")},
				{"state": "Invoice Created", "doc_status": "1", "allow_edit": allowed_role("Accounts Manager")},
				{"state": "Partially Paid", "doc_status": "1", "allow_edit": allowed_role("Accounts Manager")},
				{"state": "Paid", "doc_status": "1", "allow_edit": allowed_role("Accounts Manager")},
				{"state": "Closed", "doc_status": "1", "allow_edit": "System Manager"},
				{"state": "Rejected", "doc_status": "0", "allow_edit": "System Manager"},
			],
			"transitions": [
				{"state": "Draft", "action": "Submit for Review", "next_state": "Submitted", "allowed": allowed_role("QS Engineer")},
				{"state": "Draft", "action": "Submit for Review", "next_state": "Submitted", "allowed": "System Manager"},
				{"state": "Submitted", "action": "Start Review", "next_state": "Under Review", "allowed": allowed_role("Projects Manager")},
				{"state": "Submitted", "action": "Start Review", "next_state": "Under Review", "allowed": "System Manager"},
				{"state": "Under Review", "action": "Certify", "next_state": "Certified", "allowed": allowed_role("QS Engineer")},
				{"state": "Under Review", "action": "Certify", "next_state": "Certified", "allowed": "System Manager"},
				{"state": "Certified", "action": "Approve", "next_state": "Approved", "allowed": allowed_role("Accounts Manager")},
				{"state": "Certified", "action": "Approve", "next_state": "Approved", "allowed": "System Manager"},
				{"state": "Draft", "action": "Mark Rejected", "next_state": "Rejected", "allowed": "System Manager"},
				{"state": "Submitted", "action": "Mark Rejected", "next_state": "Rejected", "allowed": "System Manager"},
				{"state": "Under Review", "action": "Mark Rejected", "next_state": "Rejected", "allowed": "System Manager"},
				{"state": "Certified", "action": "Mark Rejected", "next_state": "Rejected", "allowed": "System Manager"},
				{"state": "Paid", "action": "Mark Closed", "next_state": "Closed", "allowed": "System Manager"},
			],
		}
	)
	workflow.insert(ignore_permissions=True)


def ensure_workflow_masters(states=None, actions=None):
	for state in states or WORKFLOW_STATES:
		if not frappe.db.exists("Workflow State", state):
			frappe.get_doc({"doctype": "Workflow State", "workflow_state_name": state}).insert(
				ignore_permissions=True
			)

	for action in actions or WORKFLOW_ACTIONS:
		if not frappe.db.exists("Workflow Action Master", action):
			frappe.get_doc({"doctype": "Workflow Action Master", "workflow_action_name": action}).insert(
				ignore_permissions=True
			)
