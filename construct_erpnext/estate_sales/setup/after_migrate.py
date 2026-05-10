import frappe


WORKFLOW_NAME = "Sales Contract Approval Workflow"
WORKFLOW_STATES = ["Draft", "Under Review", "Approved", "Active", "Cancelled", "Closed"]
WORKFLOW_ACTIONS = [
    "Submit for Review",
    "Approve",
    "Activate",
    "Cancel",
    "Close",
    "Return to Draft",
]


def after_migrate():
    ensure_sales_installment_child_table_schema()
    ensure_sales_contract_workflow()


def ensure_sales_installment_child_table_schema():
    """Ensure child-table linkage columns exist after older metadata attempts.

    A previous partial setup created Sales Installment Schedule before it was
    marked as a child table. Frappe does not always retrofit the standard
    parent columns when `istable` changes later, so this keeps the migration
    idempotent without deleting data.
    """
    if not frappe.db.exists("DocType", "Sales Installment Schedule"):
        return

    from frappe.database.schema import add_column

    for column in ("parent", "parentfield", "parenttype"):
        if not frappe.db.has_column("Sales Installment Schedule", column):
            add_column("Sales Installment Schedule", column, "Data", length=140)


def ensure_sales_contract_workflow():
    """Create or repair the Sales Contract Approval Workflow idempotently.

    This intentionally uses Frappe ORM child tables (`states` and `transitions`).
    Do not create workflow rows through direct MariaDB SQL.
    """
    if not frappe.db.exists("DocType", "Sales Contract"):
        return

    ensure_workflow_masters()

    if frappe.db.exists("Workflow", WORKFLOW_NAME):
        workflow = frappe.get_doc("Workflow", WORKFLOW_NAME)
        if _workflow_is_valid(workflow):
            return
        frappe.delete_doc("Workflow", WORKFLOW_NAME, ignore_permissions=True, force=True)

    roles = [
        role
        for role in ("System Manager", "Sales Manager", "Projects Manager", "Accounts Manager")
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
            "document_type": "Sales Contract",
            "workflow_state_field": "workflow_state",
            "is_active": 1,
            "send_email_alert": 0,
            "states": [
                workflow_state("Draft", "0", allowed_role("Sales Manager"), "Warning"),
                workflow_state("Under Review", "0", allowed_role("Sales Manager"), "Primary"),
                workflow_state("Approved", "1", allowed_role("Accounts Manager"), "Success"),
                workflow_state("Active", "1", allowed_role("Sales Manager"), "Success"),
                workflow_state("Cancelled", "2", "System Manager", "Danger"),
                workflow_state("Closed", "1", "System Manager", "Secondary"),
            ],
            "transitions": [
                workflow_transition(
                    "Draft", "Submit for Review", "Under Review", allowed_role("Sales Manager")
                ),
                workflow_transition("Draft", "Submit for Review", "Under Review", "System Manager"),
                workflow_transition(
                    "Under Review", "Approve", "Approved", allowed_role("Accounts Manager")
                ),
                workflow_transition("Under Review", "Approve", "Approved", "System Manager"),
                workflow_transition("Approved", "Activate", "Active", allowed_role("Sales Manager")),
                workflow_transition("Approved", "Activate", "Active", "System Manager"),
                workflow_transition("Under Review", "Return to Draft", "Draft", "System Manager"),
                workflow_transition("Approved", "Cancel", "Cancelled", "System Manager"),
                workflow_transition("Active", "Close", "Closed", "System Manager"),
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
    if workflow.document_type != "Sales Contract":
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
        ("Under Review", "Return to Draft", "Draft"),
        ("Approved", "Cancel", "Cancelled"),
        ("Active", "Close", "Closed"),
    }
    actual_transitions = {
        (row.state, row.action, row.next_state) for row in workflow.transitions
    }
    return not (expected_transitions - actual_transitions)
