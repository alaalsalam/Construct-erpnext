# Codex Handoff

Read project memory and working rules first, continue from NEXT_ACTION, implement one task at a time, update memory after every task.

Current branch: feature/construction-boq-foundation.

Canonical repository path: /home/frappe/frappe-bench/apps/construct_erpnext.
Old path /home/frappe/frappe-bench/apps/Construct-erpnext was removed by renaming the real repository folder.
Do not use Construct-erpnext as a working root anymore.
Keep the internal Python package folder /home/frappe/frappe-bench/apps/construct_erpnext/construct_erpnext.

El Salvador localization is disabled for the generic product build:
- after_install logs "Generic product setup completed."
- Purchase Invoice validate no longer calls the SV withholding handler.
- Legacy El Salvador setup helpers remain isolated in construct_erpnext/setup/legacy_el_salvador.py and are not executed automatically.

construction.yemenfrappe.com installation status:
- Backup completed with files under sites/construction.yemenfrappe.com/private/backups/20260509_183222-*.
- Installed apps now include frappe, erpnext, hrms, and construct_erpnext.
- construct_erpnext was installed from local branch feature/product-delocalization at commit 5686ee9 plus uncommitted delocalization changes.
- Artifact verification found zero requested El Salvador fields, tax accounts/templates, or salary components.
- Active hooks show Purchase Invoice submit authorization remains active and construct_erpnext SV withholding is not active on Purchase Invoice validate.
- Current deployment target is ERPNext v15: Frappe 15.107.2, ERPNext 15.107.0, HRMS 15.58.2. Do not upgrade to v16 without a separate approved migration plan.
- Repository changes were committed and pushed on feature/product-delocalization:
  - 2606941 chore: initialize project memory and disable country-specific localization
- v15 smoke test status: blocked at site/database level because MariaDB refused connections on 127.0.0.1. Static app metadata and hook inspection passed.
- Path normalization status: apps/construct_erpnext is now the real git repository, not a symlink.
- Bench venv import path: /home/frappe/frappe-bench/apps/construct_erpnext/construct_erpnext/__init__.py.
- Plain system python3 import failed because it is not using the bench environment.
- Product workspace cleanup status:
  - 8 product-facing workspaces are installed and visible.
  - 8 legacy GCS workspaces are retained but hidden/non-public.
  - Visibility is enforced by construct_erpnext.patches.hide_legacy_gcs_workspaces and is reversible.
  - BOQ foundation is now implemented; IPC, Measurement Book, and real estate DocTypes have not been created yet.

Construction BOQ foundation status:
- New module: construct_erpnext/construction_boq.
- New DocTypes: Cost Code, WBS Element, Construction BOQ, Construction BOQ Item, Construction Work Item.
- New reports: Construction BOQ Cost Analysis, Construction BOQ Variance.
- Workflow: Construction BOQ Approval Workflow is created after migration by construct_erpnext.construction_boq.setup.ensure_construction_boq_workflow.
- Approved BOQs generate Construction Work Items from child BOQ rows.
- Validation on construction.yemenfrappe.com passed with rollback-only records: totals calculated, workflow approval submitted the BOQ, work item generated, reports loaded, and workspace links appeared.

Next operational task: Implement BOQ linkage with procurement and site warehouses.
