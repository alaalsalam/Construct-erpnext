import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


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
    ensure_sales_invoice_collection_settings()
    ensure_sales_invoice_collection_custom_fields()
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


def ensure_sales_invoice_collection_settings():
    if frappe.db.exists("DocType", "Sales Invoice Collection Settings"):
        settings = frappe.get_single("Sales Invoice Collection Settings")
        defaults = {
            "enable_sales_invoice_generation": 1,
            "auto_submit_sales_invoice": 0,
            "allow_grouped_installment_invoice": 1,
            "require_unit_dimension": 1,
            "auto_update_installment_status": 1,
            "overdue_grace_days": 0,
            "allow_partial_collection": 1,
            "block_duplicate_invoice_for_installment": 1,
            "require_customer_on_contract": 1,
            "require_unit_on_invoice_item": 1,
            "use_company_default_currency": 1,
        }
        changed = False
        for fieldname, value in defaults.items():
            if not frappe.db.exists(
                "Singles",
                {"doctype": "Sales Invoice Collection Settings", "field": fieldname},
            ):
                settings.set(fieldname, value)
                changed = True
        if changed:
            settings.save(ignore_permissions=True)


def ensure_sales_invoice_collection_custom_fields():
    if not frappe.db.exists("DocType", "Sales Invoice Item"):
        return

    custom_fields = {
        "Sales Invoice Item": [
            {
                "fieldname": "sales_contract",
                "label": "Sales Contract",
                "fieldtype": "Link",
                "options": "Sales Contract",
                "insert_after": "unit" if frappe.get_meta("Sales Invoice Item").has_field("unit") else "project",
                "description": "Sales Contract from which this invoice item was generated.",
            },
            {
                "fieldname": "sales_installment_reference",
                "label": "Sales Installment Reference",
                "fieldtype": "Data",
                "insert_after": "sales_contract",
                "description": "Internal child-row reference for the Sales Contract installment represented by this invoice item.",
            },
            {
                "fieldname": "real_estate_project",
                "label": "Real Estate Project",
                "fieldtype": "Link",
                "options": "Real Estate Project",
                "insert_after": "sales_installment_reference",
                "description": "Real estate project linked to the sold unit.",
            },
            {
                "fieldname": "unit_reservation",
                "label": "Unit Reservation",
                "fieldtype": "Link",
                "options": "Unit Reservation",
                "insert_after": "real_estate_project",
                "description": "Original reservation converted into the Sales Contract, if available.",
            },
        ],
        "Sales Invoice": [
            {
                "fieldname": "sales_contract",
                "label": "Sales Contract",
                "fieldtype": "Link",
                "options": "Sales Contract",
                "insert_after": "unit" if frappe.get_meta("Sales Invoice").has_field("unit") else "project",
                "description": "Sales Contract from which this Sales Invoice was generated.",
            },
            {
                "fieldname": "real_estate_project",
                "label": "Real Estate Project",
                "fieldtype": "Link",
                "options": "Real Estate Project",
                "insert_after": "sales_contract",
                "description": "Real estate project linked to the sold unit.",
            },
        ],
    }
    create_custom_fields(custom_fields, ignore_validate=True)


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
