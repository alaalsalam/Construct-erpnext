import frappe


WORKFLOW_NAME = "Measurement Book Verification Workflow"
WORKFLOW_STATES = ["Draft", "Submitted", "Under Verification", "Verified", "Locked", "Cancelled"]
WORKFLOW_ACTIONS = ["Submit for Verification", "Start Verification", "Verify", "Lock", "Cancel"]


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
