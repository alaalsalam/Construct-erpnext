import frappe


def execute():
    legacy_workspaces = [
        "GCS Admin",
        "GCS Finance",
        "GCS Maintenance",
        "GCS Payroll",
        "GCS Portal",
        "GCS Production",
        "GCS Projects",
        "GCS Security",
    ]

    for workspace in legacy_workspaces:
        if frappe.db.exists("Workspace", workspace):
            frappe.db.set_value(
                "Workspace",
                workspace,
                {
                    "is_hidden": 1,
                    "public": 0,
                },
                update_modified=False,
            )
