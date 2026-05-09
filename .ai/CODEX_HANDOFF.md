# Codex Handoff

Read project memory and working rules first, continue from NEXT_ACTION, implement one task at a time, update memory after every task.

Current branch: feature/ipc-foundation.

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
- Interim Payment Certificate foundation is now implemented.

IPC foundation status:
- New DocTypes: Interim Payment Certificate, Interim Payment Certificate Line, IPC Deduction.
- Existing Subcontract is used as the optional contractor contract reference; Contractor Contract was not created.
- IPC generation method: construct_erpnext.measurement_ipc.ipc.create_ipc_from_measurement_book.
- IPC must be generated from Verified or Locked Measurement Entries through a verified Measurement Book.
- Measurement Entry now links to Interim Payment Certificate once included in a submitted/non-cancelled IPC.
- Interim Payment Certificate Approval Workflow is created after migration by construct_erpnext.measurement_ipc.setup.ensure_interim_payment_certificate_workflow.
- Approved IPC updates Construction Work Item certified_qty and certification fields separately from measured_qty.
- Draft Purchase Invoice creation exists on approved IPC and does not submit automatically.
- New reports: IPC Register, IPC Line Details, Measurement to IPC Traceability, Contractor IPC Summary.
- Retained Arabic validation records:
  - IPC: IPC-2026-00001 / IPC-001
  - Remarks: مستخلص رقم 1 لأعمال خرسانة الأساسات
  - Purchase Invoice draft: ACC-PINV-2026-00002
- Validation passed:
  - IPC workflow reached Approved and then status Invoice Created after draft PI creation.
  - gross_amount 875000, retention_amount 87500, net_payable 787500.
  - Construction Work Item CWI-2026-00001 certified_qty 25, certified_amount 875000, certification_status Partially Certified.
  - Measurement Entry ME-2026-00001 is linked to IPC-2026-00001.
  - Purchase Invoice ACC-PINV-2026-00002 is Draft and uses currency YER.
  - Contractor Ledger, Contractor Contract, and Real Estate Unit DocTypes were not created.
- Site repair note: construct_erpnext was added to /home/frappe/frappe-bench/sites/apps.txt because the app was installed on construction.yemenfrappe.com but missing from bench app module mapping.

Contractor Ledger and Retention foundation status:
- Branch: feature/contractor-ledger-retention.
- New module: construct_erpnext/contractor_management.
- New DocTypes: Contractor Account, Contractor Ledger Entry, Retention Register, Advance Register, Guarantee Register.
- Contractor Ledger is an operational subledger and does not replace ERPNext GL.
- ERPNext Purchase Invoice and Payment Entry remain accounting source of truth.
- IPC submission creates operational ledger and retention records.
- Draft Purchase Invoice creation from IPC creates/updates operational ledger references only.
- Payment Entry hooks read ERPNext allocations for linked IPC Purchase Invoices and update operational ledger/payment status without overriding standard Payment Entry behavior.
- New reports: Contractor Account Statement, Retention Register Report, Advance Recovery Report, Contractor Exposure Summary, Guarantee Register Report.
- Existing IPC records can be synchronized with construct_erpnext.contractor_management.ledger_utils.sync_ipc.
- Migration and cache clears completed after MariaDB recovered from an OOM-kill failure.
- Existing IPC IPC-2026-00001 was synchronized into Contractor Account CA-2026-00001.
- Current contractor account totals: certified 875000, retention held 87500, invoiced 875000, paid 0, operational outstanding 787500.
- Retention Register RET-2026-00001 exists for 87500 with release due date 2027-05-09.
- Contractor reports and product workspaces load.
- Purchase Invoice ACC-PINV-2026-00002 remains draft; Payment Entry validation remains pending until the invoice is submitted through ERPNext controls.

Project Financial Snapshot and CFO Analytics status:
- Branch: feature/cfo-financial-snapshot.
- New module: construct_erpnext/cfo_analytics.
- New DocType: Project Financial Snapshot.
- Aggregation service: construct_erpnext.cfo_analytics.project_financials.
- Whitelisted methods: get_snapshot_data and create_snapshot.
- New reports: Project Financial Snapshot Report, CFO Project Control Summary, Work Item Financial Traceability, Contractor Financial Exposure.
- Validation snapshot PFS-2026-00001 was created for PROJ-0001 with Arabic title الملخص المالي لمشروع البرج السكني المتكامل.
- Snapshot values: BOQ 3500000, committed 3500000, invoiced 3500000, consumed 875000, measured 875000, certified gross 875000, certified net 787500, retention 87500, contractor outstanding 787500, cost risk Yellow, cash risk Red, overall At Risk.
- The CFO snapshot does not replace ERPNext accounting reports or GL and does not create Journal Entries.
- Cash Flow Forecast full engine and scheduled EVM automation remain deferred.

Cash Flow Forecast foundation status:
- Branch: feature/cash-flow-forecast-foundation.
- New DocTypes: Project Cash Flow Forecast, Project Cash Flow Forecast Period.
- Forecast service: construct_erpnext.cfo_analytics.cash_flow_forecast.
- Whitelisted methods: get_forecast_data and create_forecast.
- New reports: Project Cash Flow Forecast Report, Project Cash Requirement Summary, Contractor Payment Forecast, Retention Release Forecast.
- Validation forecast PCF-2026-00001 was created for PROJ-0001 with Arabic title توقع التدفق النقدي لمشروع البرج السكني المتكامل.
- Validation period: Monthly, 2026-05-01 to 2026-10-31, opening balance 0.
- Forecast values: inflow 0, Purchase Order outflow 0, Purchase Invoice outflow 3500000, IPC outflow 787500, retention release 0, total outflow 4287500, net cash flow -4287500, lowest balance -4287500, risk Red.
- Purchase Order outflow is zero because the submitted Purchase Order is fully invoiced.
- IPC outflow is counted because the linked IPC Purchase Invoice is still draft; submitted Purchase Invoice outstanding is counted separately.
- Retention release is outside the six-month validation range because due date is 2027-05-09.
- No accounting documents, Journal Entries, EVM scheduled tasks, or Real Estate/Sales/Rental DocTypes were created.

EVM Metrics foundation status:
- Branch: feature/evm-metrics-foundation.
- New DocType: Project EVM Metrics.
- EVM service: construct_erpnext.cfo_analytics.evm_metrics.
- Whitelisted methods: get_evm_data and create_evm_snapshot.
- New reports: Project EVM Metrics Report, EVM Forecast Summary, Project Performance Dashboard Report.
- Validation snapshot EVM-2026-00001 was created for PROJ-0001 with Arabic title مؤشرات القيمة المكتسبة لمشروع البرج السكني المتكامل.
- Validation values: BAC 3500000, EV 875000, AC 3500000, PV 1050000, CV -2625000, SV -175000, CPI 0.25, SPI 0.833333333, EAC 14000000, ETC 10500000, VAC -10500000, TCPI 0, forecast overrun 10500000, overall At Risk.
- EVM reports and product workspaces load.
- No scheduled jobs, accounting documents, Journal Entries, Real Estate Inventory, or Sales/Rental DocTypes were created.

Next operational task: Design and implement Real Estate Inventory foundation.
