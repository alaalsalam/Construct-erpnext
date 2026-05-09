# Codex Handoff

Read project memory and working rules first, continue from NEXT_ACTION, implement one task at a time, update memory after every task.

Current branch: feature/measurement-book-foundation.

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

Procurement linkage status:
- New module: construct_erpnext/procurement_control.
- New Single DocType: Procurement Control Settings.
- App-managed Custom Fields link ERPNext procurement/stock child rows to Construction Work Item, Construction BOQ, WBS Element, Cost Code, and Site Warehouse.
- Warehouse has site warehouse metadata fields.
- Procurement hooks sync BOQ metadata on row validate and recalculate Work Item procurement totals on submit/cancel.
- Purchase Invoice submit authorization remains active; El Salvador withholding remains disabled.
- Stock Entry material assignment hook remains active.
- Whitelisted Material Request generation exists at construct_erpnext.procurement_control.material_request.create_material_request_from_work_items.
- New reports: Work Item Procurement Summary, BOQ Procurement Pipeline, Site Warehouse Consumption, Procurement Budget Control.
- Baseline ERPNext masters are now configured on construction.yemenfrappe.com.
- Operational baseline records retained and normalized to Arabic, non-country-specific names:
  - Company: شركة التطوير العقاري والبناء
  - Fiscal Year: 2026
  - Project: مشروع البرج السكني المتكامل / PROJ-0001
  - Cost Center: مركز تكلفة - مشروع البرج السكني المتكامل - RED
  - Site Warehouse: مخزن موقع مشروع البرج السكني المتكامل - RED / SITE-001
  - Supplier: مقاول الأعمال الإنشائية
  - Items: خرسانة جاهزة C30, حديد تسليح, خدمة مقاول أعمال إنشائية
  - UOMs: عدد, متر, متر مربع, متر مكعب, كجم
  - Item Groups: مواد البناء, خدمات المقاولين
  - Cost Code: CC-CONC / أعمال الخرسانة الإنشائية
  - WBS Element: PROJ-0001-01.01 / أعمال خرسانة الأساسات
- System Settings language is ar; timezone was left unchanged.
- Full procurement validation passed with retained submitted records:
  - Construction BOQ: ANK-BOQ-FOUNDATION-001
  - Construction Work Item: CWI-2026-00001
  - Material Request: MAT-MR-2026-00001
  - Purchase Order: PUR-ORD-2026-00003
  - Purchase Receipt: MAT-PRE-2026-00001
  - Purchase Invoice: ACC-PINV-2026-00001
  - Stock Entry: MAT-STE-2026-00001
- Work Item procurement totals after validation:
  - requested_qty 100, ordered_qty 100, received_qty 100, invoiced_qty 100, consumed_qty 25
  - committed_amount 3500000, invoiced_amount 3500000, consumed_amount 875000
  - procurement_status Fully Invoiced
- Reports and product workspaces loaded successfully after full procurement validation.

Measurement Book foundation status:
- New module: construct_erpnext/measurement_ipc.
- New DocTypes: Measurement Book and Measurement Entry.
- Measurement Book Verification Workflow is created after migration by construct_erpnext.measurement_ipc.setup.ensure_measurement_book_workflow.
- Measurement Entry is standalone and links Measurement Book to Construction Work Item for future IPC and field/mobile capture.
- Construction Work Item now tracks measured_qty, measurement_amount, measurement_progress_percent, last_measurement_date, and measurement_status.
- certified_qty is not updated by Measurement Book; certification remains reserved for IPC.
- New reports: Measurement Book Register, Work Item Measurement Progress, Measurement Verification Queue.
- Retained Arabic validation records:
  - Measurement Book: MB-2026-00001 / قياسات أعمال خرسانة الأساسات
  - Measurement Entry: ME-2026-00001 for CWI-2026-00001
- Validation passed: Measurement Book workflow reached Verified, Work Item measured_qty is 25, measurement_progress_percent is 25, and certified_qty remains 0.
- Interim Payment Certificate DocType has not been created.

Next operational task: Design and implement Interim Payment Certificate foundation.
