from frappe import _

app_name = "construct_erpnext"
app_title = "Construct ERPNext"
app_publisher = "Sovereign IT Services"
app_description = "Real Estate Development ERP for ERPNext v15"
app_email = "git@sovit.xyz"
app_license = "AGPL-3.0"
required_apps = ["frappe", "erpnext", "hrms"]

# --- After Install ---
after_install = "construct_erpnext.setup.install.after_install"
after_migrate = [
    "construct_erpnext.construction_boq.setup.ensure_construction_boq_workflow",
    "construct_erpnext.procurement_control.setup.after_migrate",
    "construct_erpnext.measurement_ipc.setup.ensure_measurement_book_workflow",
    "construct_erpnext.measurement_ipc.setup.ensure_interim_payment_certificate_workflow",
    "construct_erpnext.contractor_management.setup.after_migrate",
    "construct_erpnext.cfo_analytics.setup.after_migrate",
    "construct_erpnext.unit_costing.setup.after_migrate",
    "construct_erpnext.real_estate_inventory.setup.after_migrate",
    "construct_erpnext.estate_sales.setup.after_migrate.after_migrate",
    "construct_erpnext.estate_rental.setup.after_migrate.after_migrate",
    "construct_erpnext.brokerage.setup.after_migrate.after_migrate",
    "construct_erpnext.real_estate_crm.setup.after_migrate.after_migrate",
    "construct_erpnext.smart_matching.setup.after_migrate.after_migrate",
    "construct_erpnext.backlog_matching.setup.after_migrate.after_migrate",
    "construct_erpnext.property_maintenance.setup.after_migrate.after_migrate",
    "construct_erpnext.setup.product_readiness.sync_product_workspace_readiness",
    "construct_erpnext.procurement_control.setup.ensure_purchase_control_summary_workspace_links",
]

# --- Asset Bundles ---
app_include_js = "/assets/construct_erpnext/js/construct_erpnext.bundle.js"
app_include_css = "/assets/construct_erpnext/css/construct_erpnext.bundle.css"

# --- Client Scripts for Stock DocTypes ---
doctype_js = {
    "Project": "public/js/project.js",
    "Task": "public/js/task.js",
    "Asset": "public/js/asset.js",
    "Purchase Invoice": "public/js/purchase_invoice.js",
    "Sales Invoice": "public/js/sales_invoice.js",
    "Payment Entry": "public/js/payment_entry.js",
    "Salary Slip": "public/js/salary_slip.js",
}

override_doctype_dashboards = {
    "Project": ["construct_erpnext.presentation.dashboard_overrides.extend_project_dashboard"],
    "Material Request": ["construct_erpnext.presentation.dashboard_overrides.extend_procurement_dashboard"],
    "Purchase Order": ["construct_erpnext.presentation.dashboard_overrides.extend_procurement_dashboard"],
    "Purchase Receipt": ["construct_erpnext.presentation.dashboard_overrides.extend_procurement_dashboard"],
    "Purchase Invoice": ["construct_erpnext.presentation.dashboard_overrides.extend_procurement_dashboard"],
    "Stock Entry": ["construct_erpnext.presentation.dashboard_overrides.extend_procurement_dashboard"],
    "Sales Invoice": ["construct_erpnext.presentation.dashboard_overrides.extend_sales_invoice_dashboard"],
    "Customer": ["construct_erpnext.presentation.dashboard_overrides.extend_customer_dashboard"],
    "Supplier": ["construct_erpnext.presentation.dashboard_overrides.extend_supplier_dashboard"],
}

# --- Override Stock Controllers ---
override_doctype_class = {
    "Project": "construct_erpnext.overrides.project.ConstructProject",
    "Task": "construct_erpnext.overrides.task.ConstructTask",
    "Journal Entry": "construct_erpnext.overrides.journal_entry.ConstructJournalEntry",
    "Salary Slip": "construct_erpnext.overrides.salary_slip.ConstructSalarySlip",
}

# --- Document Events ---
doc_events = {
    "*": {
        "after_insert": "construct_erpnext.gcs_security.audit.log_insert",
        "on_update": "construct_erpnext.gcs_security.audit.log_update",
        "on_trash": "construct_erpnext.gcs_security.audit.log_delete",
    },
    "Purchase Invoice": {
        "validate": [
            "construct_erpnext.procurement_control.events.validate_procurement_doc",
            "construct_erpnext.cfo_analytics.financial_dimensions.validate_dimension_doc",
        ],
        "on_submit": [
            "construct_erpnext.gcs_admin.invoice_auth.check_authorization",
            "construct_erpnext.procurement_control.events.recalculate_procurement_doc",
            "construct_erpnext.contractor_management.events.sync_purchase_invoice",
        ],
        "on_cancel": [
            "construct_erpnext.procurement_control.events.recalculate_procurement_doc",
            "construct_erpnext.contractor_management.events.reverse_purchase_invoice",
        ],
        # El Salvador localization disabled for generic product build.
        # Country-specific withholding must be enabled explicitly per deployment.
    },
    "Payment Entry": {
        "on_submit": [
            "construct_erpnext.contractor_management.events.sync_payment_entry",
            "construct_erpnext.estate_sales.collections_utils.update_contract_from_payment_entry",
            "construct_erpnext.estate_rental.rent_collections_utils.update_lease_from_payment_entry",
        ],
        "on_cancel": [
            "construct_erpnext.contractor_management.events.reverse_payment_entry",
            "construct_erpnext.estate_sales.collections_utils.update_contract_from_payment_entry",
            "construct_erpnext.estate_rental.rent_collections_utils.update_lease_from_payment_entry",
        ],
    },
    "Material Request": {
        "validate": [
            "construct_erpnext.procurement_control.events.validate_procurement_doc",
            "construct_erpnext.cfo_analytics.financial_dimensions.validate_dimension_doc",
        ],
        "on_submit": "construct_erpnext.procurement_control.events.recalculate_procurement_doc",
        "on_cancel": "construct_erpnext.procurement_control.events.recalculate_procurement_doc",
    },
    "Purchase Order": {
        "validate": [
            "construct_erpnext.procurement_control.events.validate_purchase_order",
            "construct_erpnext.cfo_analytics.financial_dimensions.validate_dimension_doc",
        ],
        "on_submit": "construct_erpnext.procurement_control.events.recalculate_procurement_doc",
        "on_cancel": "construct_erpnext.procurement_control.events.recalculate_procurement_doc",
    },
    "Purchase Receipt": {
        "validate": [
            "construct_erpnext.procurement_control.events.validate_procurement_doc",
            "construct_erpnext.cfo_analytics.financial_dimensions.validate_dimension_doc",
        ],
        "on_submit": "construct_erpnext.procurement_control.events.recalculate_procurement_doc",
        "on_cancel": "construct_erpnext.procurement_control.events.recalculate_procurement_doc",
    },
    "Sales Invoice": {
        "validate": [
            "construct_erpnext.estate_sales.sales_invoice_utils.validate_sales_invoice_dimensions",
            "construct_erpnext.estate_rental.rent_invoice_utils.validate_rent_invoice_dimensions",
            "construct_erpnext.cfo_analytics.financial_dimensions.validate_dimension_doc",
        ],
        "on_submit": [
            "construct_erpnext.gcs_admin.reminders.schedule_payment_reminders",
            "construct_erpnext.estate_sales.sales_invoice_utils.sync_installments_from_sales_invoice",
            "construct_erpnext.estate_rental.rent_invoice_utils.sync_rent_schedule_from_sales_invoice",
        ],
        "on_cancel": [
            "construct_erpnext.estate_sales.sales_invoice_utils.release_installments_on_invoice_cancel",
            "construct_erpnext.estate_rental.rent_invoice_utils.release_rent_schedule_on_invoice_cancel",
        ],
    },
    "Stock Entry": {
        "validate": [
            "construct_erpnext.procurement_control.events.validate_procurement_doc",
            "construct_erpnext.cfo_analytics.financial_dimensions.validate_dimension_doc",
        ],
        "on_submit": [
            "construct_erpnext.gcs_projects.material.assign_cost_to_activity",
            "construct_erpnext.procurement_control.events.recalculate_procurement_doc",
        ],
        "on_cancel": "construct_erpnext.procurement_control.events.recalculate_procurement_doc",
    },
    "Salary Slip": {
        "on_submit": "construct_erpnext.gcs_payroll.distribution.distribute_costs",
    },
    "Journal Entry": {
        "validate": "construct_erpnext.cfo_analytics.financial_dimensions.validate_dimension_doc",
    },
    "Physical Advancement": {
        "on_submit": "construct_erpnext.gcs_projects.advancement.update_project_progress",
    },
    "Check Request": {
        "on_update_after_submit": "construct_erpnext.gcs_finance.treasury.handle_check_status_change",
    },
}

# --- Scheduler Events ---
scheduler_events = {
    "daily": [
        "construct_erpnext.gcs_admin.reminders.send_payment_reminders",
        "construct_erpnext.gcs_maintenance.routines.check_preventive_schedules",
        "construct_erpnext.real_estate_inventory.reservation_utils.expire_overdue_reservations",
        "construct_erpnext.estate_sales.collections_utils.mark_overdue_installments",
        "construct_erpnext.estate_rental.rent_invoice_utils.mark_overdue_rent_schedules",
    ],
    "hourly": [
        "construct_erpnext.gcs_security.audit.process_audit_queue",
    ],
}

# --- Portal ---
portal_menu_items = [
    {"title": _("My Projects"), "route": "/project-portal", "role": "Customer"},
    {"title": _("Invoices"), "route": "/client-invoices", "role": "Customer"},
    {"title": _("Documents"), "route": "/client-documents", "role": "Customer"},
    {"title": _("Authorize Advancement"), "route": "/advancement-auth", "role": "Customer"},
    {"title": _("Payment History"), "route": "/payment-history", "role": "Customer"},
]

website_route_rules = [
    {"from_route": "/project-portal/<project>", "to_route": "project-portal/project"},
    {"from_route": "/advancement-auth/<advancement>", "to_route": "advancement-auth/advancement"},
]

# --- Permissions ---
permission_query_conditions = {
    "Project": "construct_erpnext.gcs_security.permissions.project_query_conditions",
    "Task": "construct_erpnext.gcs_security.permissions.task_query_conditions",
    "Construction Budget": "construct_erpnext.gcs_security.permissions.budget_query_conditions",
}

has_permission = {
    "Project": "construct_erpnext.gcs_security.permissions.has_project_permission",
    "Construction Budget": "construct_erpnext.gcs_security.permissions.has_budget_permission",
}

# --- Fixtures (Custom Fields on stock doctypes) ---
fixtures = [
    {
        "dt": "Custom Field",
        "filters": [["module", "in", [
            "GCS Projects",
            "GCS Production",
            "GCS Maintenance",
            "GCS Admin",
            "GCS Finance",
            "GCS Payroll",
            "GCS Security",
        ]]],
    },
    {
        "dt": "Property Setter",
        "filters": [["module", "in", [
            "GCS Projects",
            "GCS Production",
            "GCS Maintenance",
            "GCS Admin",
            "GCS Finance",
            "GCS Payroll",
            "GCS Security",
        ]]],
    },
    {
        "dt": "Role",
        "filters": [["name", "in", [
            "Construction Manager",
            "Budget Controller",
            "Site Inspector",
            "Construction Client",
            "Subcontractor Portal",
            "Maintenance Engineer",
            "Treasury Manager",
            "Audit Administrator",
            "Payroll Cost Allocator",
        ]]],
    },
]

# --- Jinja Extensions ---
jinja = {
    "methods": [
        "construct_erpnext.gcs_projects.utils.get_budget_summary",
        "construct_erpnext.gcs_projects.utils.get_advancement_pct",
        "construct_erpnext.gcs_portal.utils.get_client_projects",
    ],
}
