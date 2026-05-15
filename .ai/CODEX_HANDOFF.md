# Codex Handoff

Read project memory and working rules first, continue from NEXT_ACTION, implement one task at a time, update memory after every task.

Current branch: feature/final-real-estate-erp-completion (review branch: feature/final-business-logic-review-uat)

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

Real Estate Inventory foundation status:
- Branch: feature/real-estate-inventory-foundation.
- New module: construct_erpnext/real_estate_inventory.
- New DocTypes: Real Estate Project, Building, Floor, Unit Type, Unit, Property Owner, Property Ownership.
- Inventory services: construct_erpnext.real_estate_inventory.inventory_utils.
- New reports: Unit Inventory Report, Unit Availability Report, Ownership Summary Report, Real Estate Project Summary.
- Validation inventory is retained:
  - Real Estate Project REP-2026-00001 / مشروع البرج السكني المتكامل العقاري.
  - Building A / البرج A.
  - Floors A-G, A-01, A-02.
  - Units A-101, A-102, A-201, A-G01, P-01.
  - Property Owner POWN-2026-00001 / مالك استثماري رئيسي.
  - Property Ownership OWN-2026-00001 for A-101 at 100 percent.
- Current inventory counts: total 5, available 3, reserved 1, sold 0, rented 1, blocked 0.
- Tenant is not stored on Unit. Lease Contract, Sales Contract, Reservation, Smart Matching, and Unit Cost Allocation were not created.
- Property Ownership uses fieldname property_owner because owner is reserved by Frappe.
- Inventory reports and product workspaces load.

Unit Cost Allocation and Unit Profitability foundation status:
- Branch: feature/unit-cost-profitability-foundation.
- New module: construct_erpnext/unit_costing.
- New DocTypes: Unit Cost Allocation and Unit Cost Allocation Line.
- Unit fields added: latest_cost_allocation, allocated_cost_source, allocated_cost_date, profitability_status.
- Existing Unit fields reused: allocated_cost, expected_sale_price, expected_monthly_rent, expected_margin, expected_margin_percent.
- Allocation service: construct_erpnext.unit_costing.allocation_utils.
- New reports: Unit Cost Allocation Report, Unit Profitability Report, Real Estate Project Profitability Summary, Building Profitability Summary.
- Unit Costing workspace links are synced through construct_erpnext.unit_costing.setup.after_migrate.
- Validation allocation UCA-2026-00001 is retained for REP-2026-00001 with source amount 3500000, total allocated 3500000, and unallocated amount 0.
- All five Arabic validation units are currently Profitable after allocation.
- Unit Cost Allocation is operational management control only and creates no accounting entries.
- No tenant fields, Lease Contract, Sales Contract, Reservation, or Smart Matching were created.

Financial Dimensions Traceability foundation status:
- Branch: feature/financial-dimensions-traceability.
- New Single DocType: Financial Dimension Settings.
- New setup: construct_erpnext.cfo_analytics.setup.after_migrate.
- Accounting Dimensions created on construction.yemenfrappe.com:
  - Construction Work Item / construction_work_item.
  - Cost Code / cost_code.
  - Unit / unit.
- Existing construction_work_item and cost_code fields on procurement rows were reused because they already matched the intended Link DocTypes.
- Unit fields were added by ERPNext Accounting Dimension setup to supported accounting/transaction doctypes.
- Dimension sync service: construct_erpnext.cfo_analytics.financial_dimensions.
- Draft-only backfill method: construct_erpnext.cfo_analytics.financial_dimensions.backfill_draft_dimensions.
- Validation backfilled draft Purchase Invoice ACC-PINV-2026-00002 only; no submitted documents or historical GL rows were changed.
- New reports: GL Dimension Traceability, Unit Financial Ledger, Work Item Financial Ledger, Cost Code Financial Analysis, Project Unit Cost Matrix.
- Existing historical GL rows show blank new dimensions unless future controlled repost/backfill is approved.

End-to-end traceability validation status:
- Branch: feature/end-to-end-traceability-validation.
- Validation file: .ai/TRACEABILITY_VALIDATION.md.
- Accounting Dimensions exist for Construction Work Item, Cost Code, and Unit.
- Draft Purchase Invoice ACC-PINV-2026-00002 was synced with dimensions and remains Draft.
- Do not submit ACC-PINV-2026-00002 until normal Invoice Authorization is completed.
- Stock Entry MAT-STE-2026-00001 has operational row links, but its historical GL dimension fields are blank because it predates dimension activation.
- Traceability reports load and degrade gracefully for historical blank GL dimensions.
- No submitted documents were amended, no broad GL backfill was run, and no Reservation/Sales/Rental DocTypes were created.

Product readiness and bilingual UX status:
- Branch: feature/product-readiness-bilingual-ux.
- Arabic translations: construct_erpnext/translations/ar.csv.
- Product workspace readiness sync: construct_erpnext.setup.product_readiness.sync_product_workspace_readiness.
- Client presentation guide: .ai/CLIENT_PRESENTATION_WALKTHROUGH.md.
- Readiness checklist: .ai/PRODUCT_READINESS_CHECKLIST.md.
- Custom report labels in completed modules use Frappe translation wrappers.
- Product-facing workspaces are grouped for presentation and daily operations.
- Sales & Rental remains a placeholder; no Reservation, Sales Contract, Lease Contract, CRM Matching, Portal feature, accounting document, submitted-document amendment, or GL backfill was created.
- Dashboard cards/charts are deferred until KPI sign-off; use Executive Control Center reports for presentation.

Unit Reservation foundation status:
- Branch: feature/unit-reservation-foundation.
- New DocTypes: Unit Reservation Settings, Unit Reservation.
- New reservation utility module: construct_erpnext.real_estate_inventory.reservation_utils.
- New setup hook: construct_erpnext.real_estate_inventory.setup.after_migrate.
- Daily expiry scheduler: construct_erpnext.real_estate_inventory.reservation_utils.expire_overdue_reservations.
- New reports: Unit Reservation Register, Active Unit Reservations, Expiring Unit Reservations, Unit Reservation Impact.
- Validation records retained:
  - Customer: عميل مهتم بشراء وحدة سكنية.
  - Active reservation RES-2026-00001 for A-101.
  - Cancelled validation reservation RES-2026-00003 for P-01.
  - Expired validation reservation RES-2026-00004 for A-G01.
- Current inventory counts after validation: total 5, available 2, reserved 2, sold 0, rented 1, blocked 0.
- No Sales Contract, Lease Contract, tenant field, invoice, payment, accounting document, or portal feature was created.

Presentation UX and Executive Dashboard Polish status:
- Branch: feature/presentation-ux-dashboard-polish.
- New presentation workspace: Executive Presentation Center.
- New KPI service: construct_erpnext.cfo_analytics.presentation.
- Product readiness sync now creates/updates presentation Number Cards and can create missing product workspaces from curated JSON.
- New Number Cards:
  - BOQ Total, Committed Amount, Certified Gross Amount, Net Payable, Retention Held, Contractor Outstanding.
  - Cash Flow Risk, EVM CPI, EVM SPI, EVM Overall Status.
  - Total Units, Available Units, Reserved Units, Rented Units.
  - Expected Gross Margin, Expected Margin %, Active Reservations, Expiring Reservations.
- Dashboard Charts are intentionally deferred until chart definitions and thresholds are approved for client presentation.
- Client presentation walkthrough and readiness checklist include the new presentation flow.
- No Sales Contract, Lease Contract, installment, rent schedule, CRM matching, portal feature, accounting document, GL backfill, or submitted document amendment was introduced.

Workspace and Form UX Completion status:
- Branch: feature/workspace-form-ux-completion.
- Product-facing workspace JSON is reordered by process flow.
- 32 completed custom DocTypes received form layout/readiness updates:
  - Section Break grouping,
  - concise field descriptions,
  - calculated/status field grouping,
  - improved List View fields.
- New readiness document: .ai/FORM_AND_WORKSPACE_UX_REVIEW.md.
- Arabic translations were extended for section labels and important UX descriptions.
- No fieldnames or fieldtypes were changed, and no optional fields were made required.
- No Sales Contract, Lease Contract, installment, rent schedule, CRM matching, portal feature, accounting document, GL backfill, or submitted document amendment was introduced.

Final readiness gate status:
- Branch: feature/workspace-form-ux-completion.
- New review file: .ai/FINAL_REVIEW_GATE.md.
- bench migrate, clear-cache, and clear-website-cache passed on construction.yemenfrappe.com.
- Product workspaces, key reports, key forms/list views, and completed validation records passed the review.
- Arabic translation CSV parsed successfully and required labels are present.
- Sales & Rental remains reservation-focused; Sales Contract, Lease Contract, Installment Plan, Rent Schedule, and CRM Matching DocTypes are absent.
- No accounting documents were created, no submitted records were amended, and no GL backfill was run.
- Decision: safe to start Sales Contract and Installment Plan foundation.

Deep UX hardening status:
- Branch: feature/final-form-workspace-ux-hardening.
- Universal Standard exists in bench apps but is not installed on construction.yemenfrappe.com; it was used as a read-only reference for translation/RTL UX patterns.
- 32 completed custom DocTypes were hardened with Tab Breaks, Section Breaks, Column Breaks, and preserved field descriptions.
- Workspace presentation was hardened with clearer process ordering and deterministic Number Cards on major workspaces.
- Arabic translations were expanded in construct_erpnext/translations/ar.csv and audited.
- New files:
  - .ai/TRANSLATION_COVERAGE_AUDIT.md
  - .ai/UX_HARDENING_GATE.md
- No new Sales/Rental contracts, installment/rent schedules, CRM matching, portal, accounting documents, submitted amendments, or GL backfills were introduced.

Next operational task: Start Sales Contract and Installment Plan foundation.

Sales Contract and Installment Plan foundation status:
- Branch: feature/sales-contract-installment-foundation.
- New module: construct_erpnext.estate_sales.
- New Single DocType: Sales Contract Settings.
- New Child DocType: Sales Installment Schedule.
- New DocType: Sales Contract (submittable).
- New service module: construct_erpnext.estate_sales.sales_contract_utils.
- New workflow: Sales Contract Approval Workflow (Draft -> Under Review -> Approved -> Active, with Approved/Active -> Cancelled and Active -> Closed).
- Workflow is created idempotently after migration by construct_erpnext.estate_sales.setup.after_migrate.ensure_sales_contract_workflow.
- New reports: Sales Contract Register, Sales Value Summary, Unit Sales Pipeline, Active Sales Contracts, Sold Units.
- Workspace links added to Sales & Rental, Real Estate Inventory, Executive Control Center, Executive Presentation Center, Reports & Analytics.
- Arabic translations extended in construct_erpnext/translations/ar.csv.
- Validation records retained:
  - Sales Contract SC-2026-00001 from reservation RES-2026-00001.
  - 5 installments with Booking 20%, Down Payment 30%, Construction Milestone 25%, Handover 20%, Post Handover 5%.
  - Unit A-101 status changed to Sold on Sales Contract submission.
  - Reservation RES-2026-00001 status changed to Converted.
- Sales Contract Settings defaults: mark_unit_sold_on_approval enabled, enable_sales_invoice_generation disabled, allow_duplicate_contract_for_unit disabled, require_customer enabled, require_installment_schedule enabled, installment_amount_tolerance_percent 5.
- Unit.status and Unit.marketing_status updated to Sold on Sales Contract submission (if settings allow).
- Previous unit status stored on Sales Contract for safe rollback on cancellation.
- No Sales Invoice, Payment Entry, Lease Contract, Rent Schedule, Commission, CRM Matching, Portal, accounting documents, or ERPNext core modifications were introduced.
- Next operational task: Review Sales Contract readiness before Sales Invoice and Collections foundation.

Sales Contract recovery note:
- Do not use raw SQL for workflow creation or repair.
- Workflow setup is in `construct_erpnext.estate_sales.setup.after_migrate.after_migrate` and uses Frappe ORM child table append syntax.
- Current retained validation record: SC-2026-00001 is Active, linked to RES-2026-00001, and Unit A-101 is Sold.
- Final retained installment schedule has four Arabic rows and totals 1,200,000, matching the net price.
- Final sales reports are: Sales Contract Register, Installment Schedule Report, Unit Sales Pipeline, Sales Value Summary, Reserved to Sold Conversion Report.

Sales Contract readiness review status:
- Branch: feature/sales-contract-readiness-review.
- Review file: .ai/SALES_CONTRACT_READINESS_REVIEW.md.
- SC-2026-00001 is Active, docstatus 1, linked to RES-2026-00001 and Unit A-101.
- Unit A-101 is Sold; RES-2026-00001 is Converted.
- Installment schedule has 4 rows totaling 1,200,000, matching net_price.
- Duplicate contract validation and draft installment mismatch validation were confirmed without saving validation documents.
- No Sales Invoice, Payment Entry, Journal Entry, or GL Entry exists for SC-2026-00001.
- Unit Accounting Dimension exists and unit fields are present on Sales Invoice Item and GL Entry.
- All required sales reports, key existing reports, and target workspaces load.
- ar.csv parses successfully; minor missing Arabic translations remain for generic labels Contract Information and Installments.
- Next operational task: Start Sales Invoice and Collections foundation.

Sales Invoice and Collections foundation status:
- Branch: feature/sales-invoice-collections-foundation.
- New Single DocType: Sales Invoice Collection Settings.
- Sales Installment Schedule now tracks invoice_status, invoice_amount, paid_amount, outstanding_amount, invoiced_on, paid_on, and overdue_days.
- Sales Contract now tracks total_invoiced_amount, total_collected_amount, total_outstanding_amount, collection_status, first_sales_invoice, and latest_payment_entry.
- New service modules:
  - construct_erpnext.estate_sales.sales_invoice_utils
  - construct_erpnext.estate_sales.collections_utils
- Draft invoice generation is available from Sales Contract installments and from the Sales Contract form button.
- Payment Entry integration is read/sync only through standard ERPNext references; it does not create or alter Payment Entry accounting logic.
- New reports: Sales Invoice from Installments Report, Sales Collection Report, Overdue Sales Installments, Unit Revenue Report, Sales Contract Collection Summary.
- New KPI cards: Total Invoiced Sales, Total Collected Sales, Outstanding Sales Amount, Overdue Installments Count, Overdue Installments Amount.
- Retained validation record:
  - Sales Invoice ACC-SINV-2026-00001 is Draft and linked to the first installment of SC-2026-00001.
  - Its item carries unit A-101, project PROJ-0001, cost center Main - YCRE, sales_contract SC-2026-00001, real estate project REP-2026-00001, and reservation RES-2026-00001.
  - SC-2026-00001 totals: invoiced 300,000; collected 0; outstanding 300,000; collection_status Partially Invoiced.
- No Sales Invoice submission, Payment Entry, Journal Entry, Lease Contract, Rent Schedule, Commission, CRM Matching, Portal, or GL backfill was created.
- Next operational task: Review Sales Invoice and Collections readiness before Lease Contract foundation.

Sales Invoice and Collections readiness review status:
- Branch: feature/sales-invoice-collections-readiness-review.
- Review file: .ai/SALES_INVOICE_COLLECTIONS_READINESS_REVIEW.md.
- Static validation passed: Python modules compile, ar.csv parses, metadata files exist, workspace/report/KPI links exist in JSON and translations.
- Live site validation did not complete because MariaDB refused connections and `mariadb.service` is failed with `Result: oom-kill`.
- Attempting to start MariaDB from this shell failed because interactive sudo/password authentication is required.
- No business/accounting documents or new features were created during the review.
- Current readiness decision: not safe to proceed to Lease Contract until MariaDB is restored and live Sales Invoice/Collections validation is rerun.
- Next operational task: Restore MariaDB service and rerun Sales Invoice and Collections readiness validation before Lease Contract foundation.

CMD-24A recovery and validation status:
- MariaDB was active again at rerun time, but prior `oom-kill` remains a real operational risk.
- Non-interactive sudo still cannot start MariaDB: server owner must run `sudo systemctl start mariadb` if the service stops again.
- DB connection and app list checks passed.
- Live validation passed for Sales Invoice Collection Settings, SC-2026-00001, ACC-SINV-2026-00001, installment link, contract totals, Unit dimension propagation, reports, workspaces, and KPI cards.
- Draft invoice remains unsubmitted; no GL Entry, Payment Entry, Journal Entry, Lease Contract, Rent Schedule, Commission, CRM Matching, Portal, or GL backfill was created.
- Readiness decision is now safe to proceed to Lease Contract and Rent Schedule foundation.
- Next operational task: Start Lease Contract and Rent Schedule foundation.

Lease Contract and Rent Schedule foundation status:
- Branch: feature/lease-contract-rent-schedule-foundation.
- New module: construct_erpnext.estate_rental.
- New Single DocType: Lease Contract Settings.
- New DocType: Lease Contract (submittable).
- New Child DocType: Rent Schedule.
- New service module: construct_erpnext.estate_rental.lease_contract_utils.
- Whitelisted reservation conversion path: construct_erpnext.estate_rental.lease_contract.create_lease_contract_from_reservation.
- Workflow: Lease Contract Approval Workflow created idempotently through Frappe ORM in estate_rental setup.
- Reports: Lease Contract Register, Rent Schedule Report, Active Leases Report, Lease Expiry Report, Rental Value Summary.
- KPI cards: Active Lease Contracts, Scheduled Rental Value, Expiring Leases, plus existing Rented Units.
- Retained validation record:
  - Unit A-G01 is Rented.
  - Reservation RES-2026-00005 is Converted.
  - Lease Contract LC-2026-00001 is Active.
  - Rent Schedule has 12 monthly rows totaling 4,200,000.
- No rent invoice, Sales Invoice, Payment Entry, Journal Entry, commission, CRM matching, portal, or GL backfill was created.
- Lease readiness review status:
  - Branch: feature/lease-contract-readiness-review.
  - Review file: .ai/LEASE_CONTRACT_READINESS_REVIEW.md.
  - LC-2026-00001 is Active, docstatus 1, linked to RES-2026-00005 and Unit A-G01.
  - Unit A-G01 is Rented; RES-2026-00005 is Converted.
  - Rent Schedule has 12 monthly rows totaling 4,200,000, matching total contract rent.
  - Duplicate active lease validation is blocked without saving validation documents.
  - Unit Accounting Dimension exists and unit fields are present on Sales Invoice Item and GL Entry.
  - No Rent Invoice, Sales Invoice, Payment Entry, Journal Entry, GL Entry, commission, CRM matching, portal, or GL backfill exists from the lease.
  - Lease reports, key existing reports, and target workspaces load.
  - ar.csv parses successfully with lease translations present.
- Current next action: Start Rent Invoice and Collections foundation.

Phase 1 client presentation closure status:
- Branch: feature/phase-1-client-presentation-closure.
- Feature development is paused for client presentation.
- Phase 1 presentation scope is construction control, BOQ, procurement/site warehouse traceability, Measurement Book, IPC, Contractor Ledger/Retention, CFO analytics, Real Estate Inventory, Unit Cost Allocation/Profitability, Accounting Dimensions, Unit Reservation, Sales Contract/Installment foundation, and draft Sales Invoice from installment.
- Full collections, Rent/Lease full cycle, Commission, CRM, Smart Matching, Backlog Matching, Portal, WhatsApp/Meta, and production accounting automation are Phase 2.
- Lease/Rent links remain available but are marked as Phase 2 / Upcoming in primary workspaces.
- Lease-specific KPI cards were removed from primary workspace card lists for Phase 1 presentation clarity.
- Phase 1 validation passed after migrate/cache clear: key forms, reports, workspaces, KPI cards, ar.csv, and deferred-scope checks passed.
- New files:
  - .ai/PHASE_1_CLIENT_PRESENTATION_SUMMARY.md
  - .ai/PHASE_1_QA_CHECKLIST.md
- Current next action: Present Phase 1 to client and collect feedback before Phase 2 planning.

Phase 1 user guide status:
- Branch: feature/phase-1-client-presentation-closure.
- New guide: docs/PHASE_1_USER_GUIDE_AR.md.
- Guide is Arabic, client-facing, and covers Phase 1 structure, workspaces, testing scenarios, reports, limitations, and Phase 2 roadmap.
- Documentation-only change; no feature, DocType, migration, record, accounting document, or data change was made.
- Current next action: Review Phase 1 user guide before sending it to the client.

Phase 1 presentation data validation status:
- Branch: feature/phase-1-presentation-data.
- Commit bcb9497 contains construct_erpnext/setup/phase_1_presentation_data.py and is pushed to origin.
- Official validation command passed on construction.yemenfrappe.com.
- Verified counts: 4 Projects, 4 BOQs, 113 Construction Work Items, 50 Material Requests, 4 Real Estate Projects, 43 Units, 14 Unit Reservations, 1 Sales Contract, and 1 draft Sales Invoice.
- Key presentation records:
  - Projects: PROJ-0001, PROJ-0002, PROJ-0003, PROJ-0004.
  - BOQs: ANK-BOQ-FOUNDATION-001, BOQ-PROJ-0002-001, BOQ-PROJ-0003-001, BOQ-PROJ-0004-001.
  - Measurement/IPC: MB-2026-00001, ME-2026-00001, IPC-2026-00001, ACC-PINV-2026-00002.
  - Contractor: CA-2026-00001 and RET-2026-00001.
  - CFO: PFS/PCF/EVM records 00001 through 00004.
  - Real Estate: REP-2026-00001 through REP-2026-00004; unit status distribution is 22 Available, 8 Reserved, 10 Sold, 3 Rented.
  - Unit Costing: UCA-2026-00001 through UCA-2026-00004.
  - Sales: RES-2026-00001, SC-2026-00001, ACC-SINV-2026-00001.
- Presentation readiness decision: Ready with caveats.
- Caveats:
  - Procurement data is rich at Material Request/report level, but not a full PO/PR/PI/Stock chain for every project.
  - IPC has one complete example.
  - Sales has one contract and one draft invoice; no payment, submitted Sales Invoice, Journal Entry, or GL posting.
- New validation file: .ai/PHASE_1_PRESENTATION_DATA_VALIDATION.md.
- Current next action: Present Phase 1 using enriched presentation data and collect client feedback.

PROJ-0002 intensive presentation data status:
- Branch: feature/proj-0002-intensive-presentation-data.
- Main project for client presentation: `PROJ-0002` / `REP-2026-00002`.
- Data enrichment entry points:
  - `construct_erpnext.setup.phase_1_presentation_data.enrich_proj_0002_presentation_data`
  - `construct_erpnext.setup.phase_1_presentation_data.validate_proj_0002_presentation_data`
- Verified counts after enrichment:
  - 72 Construction Work Items.
  - 33 Material Requests.
  - 1 Purchase Order, 1 Purchase Receipt, 5 Purchase Invoices.
  - 2 Stock Entries.
  - 5 Measurement Books, including 4 verified presentation books.
  - 20 Measurement Entries.
  - 4 IPCs and 4 Retention Registers.
  - 24 Units and 2 Unit Cost Allocations.
  - 17 Unit Reservations, 3 Sales Contracts, 3 draft Sales Invoices.
- Main records:
  - BOQ: `BOQ-PROJ-0002-001`.
  - Measurement Books: `MB-2026-00005` to `MB-2026-00008`.
  - IPCs: `IPC-2026-00002` to `IPC-2026-00005`.
  - Sales Contracts: `SC-PROJ-0002-001` to `SC-PROJ-0002-003`.
  - Draft Sales Invoices: `ACC-SINV-2026-00002` to `ACC-SINV-2026-00004`.
- Safety status:
  - Payment Entries: 0.
  - Journal Entries: 0.
  - Submitted Sales Invoices: 0.
  - No GL backfill.
- Current next action: Present PROJ-0002 as the main Phase 1 client presentation scenario and collect feedback.

CMD-BOQ-01 BOQ screen/data quality status:
- Branch: feature/boq-screen-data-quality-proj-0002.
- Target BOQ: `BOQ-PROJ-0002-001`.
- BOQ rows are now linked to Construction Work Items through a new read-only field on Construction BOQ Item.
- BOQ Item now shows presentation execution fields for requested, ordered, received, invoiced, consumed, measured, certified, remaining, actual amount, remaining amount, variance, and execution status.
- Construction BOQ now has an Execution Summary tab with requested/ordered/invoiced/consumed/measured/certified totals.
- Refresh utility:
  - `construct_erpnext.construction_boq.boq_sync.refresh_proj_0002_boq_display`
  - `construct_erpnext.construction_boq.boq_sync.refresh_boq_execution_summary`
- Refresh result for `BOQ-PROJ-0002-001`: 72 synced rows and 72 linked Work Items.
- New report: Project Purchase Control Summary.
- Workspace links are added idempotently after product workspace sync in after_migrate.
- Use Project Purchase Control Summary as the cleanest presentation screen for Expected / Actual / Remaining / Variance, then open BOQ for details.
- Do not delete/merge duplicate-looking BOQ rows without deeper review because rows are linked to Work Items, Measurement Entries, and IPCs.
- Current next action: Finalize PROJ-0002 presentation readiness after BOQ screen enhancement.

CMD-DELIVERY-01 final PROJ-0002 handover readiness:
- Branch: feature/boq-screen-data-quality-proj-0002.
- `BOQ-PROJ-0002-001` is Approved through normal workflow:
  - docstatus 1, status Approved, workflow_state Approved.
- BOQ row quality:
  - 72/72 rows linked to Construction Work Item, WBS Element, Cost Code, UOM, and Item.
  - 36 presentation Item masters were created/reused for BOQ row item links.
  - Work Items were not force-saved for item_code because existing overrun scenarios can trigger Work Item quantity validation; the BOQ row and Project Purchase Control Summary expose the Item link.
- Preferred examples:
  - `CWI-2026-00008`: normal/certified, 48,000 planned and certified, 0% variance.
  - `CWI-2026-00006`: overrun, 680 planned, 850 requested, 20% variance.
  - `CWI-2026-00003`: partial/remaining, 1,800 planned, 1,170 measured/certified, 630 remaining.
- Project Purchase Control Summary now falls back to BOQ row Item if Work Item item_code is empty.
- Validation passed after migrate/cache clear; official PROJ-0002 validator confirmed report loads and safety:
  - Payment Entries 0.
  - Journal Entries 0.
  - Submitted Sales Invoices 0.
- New handover files:
  - `.ai/PROJ_0002_FINAL_PRESENTATION_READINESS.md`
  - `.ai/CLIENT_HANDOVER_NOTES_PHASE_1.md`
- Current next action: Present PROJ-0002 Phase 1 to client and collect handover feedback.

CMD-UX-02 connections/grid presentation status:
- Branch: feature/connections-grid-proj-0002-depth.
- Added custom DocType dashboard connection files for BOQ, Work Item, Measurement/IPC, Contractor, CFO, Real Estate, Unit Costing, Reservation, and Sales Contract forms.
- Added `override_doctype_dashboards` hooks for ERPNext Project, procurement/stock documents, Sales Invoice, Customer, and Supplier.
- Validated linked-document sidebar counts:
  - Project `PROJ-0002`: 72 Work Items, 33 Material Requests, 4 IPCs, 8 Contractor Accounts, 24 Units, 17 Reservations, 3 Sales Contracts, 3 Sales Invoices.
  - BOQ `BOQ-PROJ-0002-001`: Work Items, procurement, stock, Measurement Entries, and IPCs.
  - Sales Invoice `ACC-SINV-2026-00002`: Sales Contract, Unit Reservation, Unit, Real Estate Project.
- Improved grid columns for Construction BOQ Item, Sales Installment Schedule, Rent Schedule, Project Cash Flow Forecast Period, IPC Line, Unit Cost Allocation Line, and IPC Deduction.
- Added list indicators for key custom parent DocTypes.
- PROJ-0002 data was not further enriched because validation already meets the requested depth.
- Follow-up branch `feature/project-complete-related-connections` makes the Project form the main connected entry point:
  - Procurement/stock documents now count through child item `project` links.
  - Sales Invoice now counts through Sales Invoice Item `project` links.
  - Contractor Ledger Entry and WBS Element are visible from Project connections.
  - `PROJ-0002` live counts confirm construction, procurement, contractor, CFO, real estate, reservation, sales, and draft invoice documents are all reachable from the Project form.
- Current next action: Present PROJ-0002 Phase 1 from the Project form with complete related-document connections, then collect client feedback.

BOQ grid planned/expected visibility follow-up:
- Branch: `feature/boq-grid-planned-expected-visibility`.
- `Construction BOQ Item` now has a concise presentation grid:
  - Construction Work Item.
  - Description.
  - Planned Qty.
  - Wastage %.
  - Expected Qty.
  - Actual Qty.
  - Remaining Qty.
  - Variance %.
  - Execution Status.
- `actual_qty` is a new read-only display field calculated by `construct_erpnext.construction_boq.boq_sync` from downstream procurement, stock, measurement, and certification quantities.
- `BOQ-PROJ-0002-001` was refreshed after migration:
  - 72 synced rows.
  - Example rows validated for normal, overrun, and remaining scenarios.
- Current next action: Present PROJ-0002 Phase 1 from the Project form and BOQ grid with visible planned, expected, actual, remaining, and variance values.

Workspace compact sequential layout follow-up:
- Branch: `feature/workspace-compact-sequential-layout`.
- Public product workspaces now appear first in the intended client presentation sequence:
  - Executive Presentation Center, Executive Control Center, Construction Control, Procurement & Site Warehouses, Measurement & IPC, Contractor Management, Real Estate Inventory, Sales & Rental, Reports & Analytics.
- Internal section headers were removed from workspace content, leaving only one page title plus KPI/cards.
- Workspace cards now use `col=3` to reduce vertical scrolling.
- Hidden legacy GCS workspaces remain hidden from primary navigation.
- Current next action: Present PROJ-0002 Phase 1 using the compact sequential workspaces and BOQ grid.

Arabic field help hardening follow-up:
- Branch: `feature/arabic-field-help-hardening`.
- `Project Financial Snapshot` now has clearer English source descriptions for BOQ, procurement, measurement, IPC, contractor, CFO risk, and executive summary fields, with matching Arabic translations for the most visible presentation labels and help text.
- `Construction BOQ` now has clearer source descriptions explaining planned, expected, actual, remaining, variance, totals, and linked Work Items.
- `ar.csv` parsing passed, migrate passed, and cache clear passed on `construction.yemenfrappe.com`.
- Current next action: Review Arabic field help on key presentation screens, then present PROJ-0002 Phase 1.

PROJ-0002 contractor invoicing follow-up:
- Four IPC-linked Purchase Invoices were authorized and submitted through normal ERPNext controls:
  - `ACC-PINV-2026-00004` through `ACC-PINV-2026-00007`.
- These are linked to IPCs `IPC-2026-00002` through `IPC-2026-00005`.
- Total submitted contractor invoicing for PROJ-0002 is `202,619,475.00`; contractor net outstanding after retention/deduction tracking is `182,332,527.50`.
- No Payment Entries were created; collection/payment remains open.
- A fresh financial snapshot `PFS-2026-00005` and EVM snapshot `EVM-2026-00005` were created after invoicing.
- `Project Financial Snapshot Report` now excludes archived snapshots, so PROJ-0002 presentation shows the current snapshot only.

PROJ-0002 contractor payment follow-up:
- Payment Entries were created for the net payable amount of each IPC-linked Purchase Invoice:
  - `ACC-PAY-2026-00005` through `ACC-PAY-2026-00008`.
- Earlier full-gross payments `ACC-PAY-2026-00001` through `ACC-PAY-2026-00004` were cancelled because they overpaid retention from the contractor-control perspective.
- Contractor Account outstanding balances are now zero while retention remains held.
- Purchase Invoice outstanding still reflects retained/deducted balances; use Contractor Account Statement and Contractor Exposure Summary to explain net payment vs retention.
- Contractor ledger reversal was fixed to use the original Payment Entry as the valid Dynamic Link reference during cancellation.

PROJ-0002 diversified payment presentation follow-up:
- To avoid a flat all-paid presentation, PROJ-0002 now intentionally includes three contractor payment states:
  - Fully paid: `IPC-2026-00002` / `ACC-PINV-2026-00004` / `ACC-PAY-2026-00005`, paid `98,867,790.00`, contractor outstanding `0.00`.
  - Partially paid: `IPC-2026-00003` / `ACC-PINV-2026-00005` / `ACC-PAY-2026-00009`, paid `22,300,110.00`, contractor outstanding `22,300,110.00`.
  - Invoiced but unpaid: `IPC-2026-00004` and `IPC-2026-00005`, contractor outstanding `23,753,247.50` and `15,111,270.00`.
- Full net payments `ACC-PAY-2026-00006`, `ACC-PAY-2026-00007`, and `ACC-PAY-2026-00008` were cancelled through normal ERPNext cancellation to create partial/unpaid presentation states.
- Contractor payment reversal now refreshes IPC payment status, so cancelled payments do not leave stale `Paid` statuses.
- Contractor Account Statement filters out reversed ledger rows; use it and Contractor Exposure Summary as the main contractor-control presentation screens.
- Purchase Invoice outstanding may include retention/deduction balances; explain this as ERPNext accounting payable view versus contractor net payable/control view.
- Current next action: Review PROJ-0002 diversified presentation data across all Phase 1 reports before the client presentation.

Arabic reports/dashboard polish follow-up:
- Branch: `feature/arabic-reports-dashboard-polish`.
- Added report summary cards to the key PROJ-0002 presentation reports across procurement, IPC, contractor, CFO, unit profitability, reservation impact, and sales collection.
- Added visual indicator formatting for status/risk fields in prioritized reports using a safe global badge helper in `construct_erpnext.bundle.js`.
- Added PROJ-0002-specific Number Cards in Executive Presentation Center for BOQ total, actual amount, remaining amount, overrun items, certified amount, and unit profitability.
- Added `Sales Contracts` and `Draft Sales Invoices` KPI cards.
- Dashboard Charts remain intentionally deferred until KPI/chart definitions are signed off.
- New guide: `.ai/REPORTS_DASHBOARD_PRESENTATION_GUIDE.md`.
- Current next action: Present PROJ-0002 to client using polished Arabic reports and dashboards.

CMD-REPORT-02 report table and generic KPI follow-up:
- Project-specific PROJ-0002 Number Cards were removed from the general Executive Presentation Center workspace.
- Product readiness setup now cleans deprecated PROJ-0002 Number Cards and keeps only generic workspace KPIs.
- PROJ-0002 presentation should use filtered reports, especially Project Purchase Control Summary, Project Financial Snapshot Report, Project Cash Flow Forecast Report, Project EVM Metrics Report, Unit Profitability Report, and Sales Contract Register.
- Report execute outputs were made explicit six-value returns so report summaries remain additive and do not replace table rows.
- Report JS formatters now have a local fallback to avoid blank tables if the global indicator helper is unavailable.

Report table visibility hotfix:
- The affected reports now return `None` for `report_summary` to avoid the UI blank-table rendering issue seen with dashboard summaries.
- Do not re-enable report_summary until the desk/theme rendering issue is confirmed fixed in the browser.

Final report UI reset:
- Custom report JS formatters were removed from the affected reports after browser screenshots showed blank table cells despite valid server data.
- The current intended state is plain Frappe query report rendering: filters plus table data only.

Safe report dashboard restoration:
- Report dashboards are now rendered as HTML in the report message area, not through `report_summary`.
- Keep `report_summary` disabled until the Frappe/theme interaction that blanked table cells is fully isolated.

CMD-CONTRACTOR-01 contractor agreement linkage:
- Existing `Subcontract` is now the Contractor Agreement layer; do not create a competing Contractor Agreement DocType unless a future migration plan is approved.
- PROJ-0002 active agreements:
  - `SC-2026-0002` الإنشائي.
  - `SC-2026-0003` الكهرباء.
  - `SC-2026-0004` التشطيبات.
  - `SC-2026-0005` الواجهات.
- Work Items carry `subcontract`, `contractor`, and `agreement_item_reference`.
- Measurement Book, Measurement Entry, IPC, and IPC Line carry `subcontract` where linked.
- New reports are the preferred presentation layer for agreement progress and IPC traceability.
- Current next action: Present PROJ-0002 Phase 1 to client using the contractor agreement linkage story and collect handover feedback.

CMD-INTEGRATION-01 integrated Phase 1 source branch:
- Branch: `feature/phase-1-integrated-presentation-ready`.
- Integrates report/dashboard table stability fixes from `feature/fix-report-tables-and-generic-kpis` with contractor agreement linkage from `feature/contractor-agreements-boq-ipc-linkage`.
- Bench validation initially failed because `/home/frappe/frappe-bench/sites/apps.txt` listed `frappe_book_tutor`; corrected it to `book_tutor` and kept backup `apps.txt.bak-cmd-integration-01`.
- Migrate, cache clear, website cache clear, and `bench build --app construct_erpnext` passed after the correction.
- This is the source branch for CMD-27 Sales Invoice Posting and Collections Completion.

CMD-27 sales collections completion:
- Branch: `feature/sales-invoice-posting-collections-completion`.
- Backup before accounting posting:
  - `./construction.yemenfrappe.com/private/backups/20260514_220814-construction_yemenfrappe_com-database.sql.gz`.
- Submitted Sales Invoice: `ACC-SINV-2026-00002`.
- Created/submitted Payment Entry: `ACC-PAY-2026-00010`.
- Payment amount is intentionally partial: `1,210,000.00` of `2,420,000.00`.
- `SC-PROJ-0002-001` collection status is now `Partially Collected`.
- GL Entries for the Sales Invoice and Payment Entry carry Unit `BLD-PROJ-000-001-S-01-03`.
- New sales reports: Buyer Statement, Sales Installment Collection Status, Unit Revenue and Collection Summary.
- Do not submit the remaining draft sales invoices unless the user explicitly asks and accounting review approves it.
- Current next action: Review completed sales collections, then decide whether to proceed with rent invoice collections or Phase 2 CRM.

CMD-FINAL-01 Phase A baseline:
- Branch: `feature/final-real-estate-erp-completion`.
- Started from `feature/sales-invoice-posting-collections-completion` at `23de8e7`.
- Baseline migrate/cache/build passed on `construction.yemenfrappe.com`.
- `BOQ-PROJ-0002-001` remains Approved.
- PROJ-0002 Contractor Agreements remain active.
- `ACC-SINV-2026-00002` remains submitted / partly paid and GL carries Unit dimension.
- Current next action: Continue CMD-FINAL-01 Phase B: implement Rent Invoice and Rent Collections foundation.

CMD-FINAL-01 Phase B rent invoice and collections:
- Branch: `feature/final-real-estate-erp-completion`.
- Added `Rent Invoice Collection Settings`, rent invoice services, rent Payment Entry services, rent reports, rent KPI cards, workspace links, and Arabic translations.
- Submitted one rent invoice through standard ERPNext validation: `ACC-SINV-2026-00005` for `LC-2026-00001`, amount `350,000.00`.
- Created/submitted one partial rent Payment Entry: `ACC-PAY-2026-00011`, amount `175,000.00`.
- GL Entries for the rent invoice carry Unit `A-G01`.
- `LC-2026-00001` collection status is `Partially Collected`.
- Reports validated with rows: Tenant Statement, Rent Invoice from Schedule Report, Rent Collection Report, Overdue Rent Report, Unit Rental Revenue Report, Lease Collection Summary.
- `ar.csv` parses cleanly after removing old blank/comment rows and fixing comma-heavy source strings.
- Current next action: Continue CMD-FINAL-01 Phase C: implement Brokerage and Commission foundation.

CMD-FINAL-01 Phase C brokerage and commission:
- Branch: `feature/final-real-estate-erp-completion`.
- Added `Broker`, `Commission Rule`, and `Commission Entry` DocTypes under the new `Brokerage` module.
- Added `construct_erpnext.brokerage.commission_utils` for safe operational commission creation from Sales Contract, Lease Contract, or Sales Invoice.
- Validation records:
  - Broker `وسيط عقاري رئيسي`.
  - Rule `عمولة مبيعات عقارية 2.5%`.
  - Entry `COM-2026-00001` for `SC-PROJ-0002-001`.
  - Commission amount `302,500.00` on base `12,100,000.00`.
- Commission reports load with rows: Commission Register, Broker Performance Report, Commission Payable Summary.
- Workspace links are present in Sales & Rental, Executive Control Center, and Reports & Analytics.
- No broker Payment Entry, Journal Entry, or GL posting was created.
- Current next action: Continue CMD-FINAL-01 Phase D: implement Real Estate CRM foundation.

CMD-FINAL-01 Phase D real estate CRM:
- Branch: `feature/final-real-estate-erp-completion`.
- Added `Customer Requirement`, `Viewing Appointment`, and `Real Estate Follow Up`.
- Validation records for `REP-2026-00002`:
  - Requirements `REQ-2026-00001` to `REQ-2026-00005`.
  - Viewing Appointments `VA-2026-00001` to `VA-2026-00003`.
  - Follow Ups `REFU-2026-00001` to `REFU-2026-00004`.
- Reports load with rows: Customer Requirement Register, Sales Pipeline by Requirement, Viewing Schedule Report, Follow Up Report, Lead Source Summary.
- Workspace links are present in Sales & Rental, Executive Control Center, and Reports & Analytics.
- No accounting documents were created.
- Current next action: Continue CMD-FINAL-01 Phase E: implement Smart Matching foundation.

CMD-FINAL-01 Phase E smart matching:
- Added `Matching Settings`, `Match Result`, and `Match Result Item` under `Smart Matching`.
- Matching consumes `Customer Requirement` records and recommends available Units only.
- Validation ran for 5 requirements on `REP-2026-00002`.
- Match Results: `MATCH-2026-00001` to `MATCH-2026-00005`.
- Final Matching Performance Summary: 2 Open results, 4 available-unit recommendations, and 3 No Suitable Match results.
- No reservations, contracts, invoices, Payment Entries, Journal Entries, or GL Entries were created.
- Current next action: Continue CMD-FINAL-01 Phase F: implement Backlog Matching foundation.

CMD-FINAL-01 Phase F backlog matching:
- Added `Backlog Request` and `Backlog Match Attempt` under `Backlog Matching`.
- Backlogs were created from unmatched Smart Matching results.
- Validation records:
  - Backlog Requests `BLR-2026-00001` to `BLR-2026-00003`.
  - Attempts `BMA-2026-00001` to `BMA-2026-00006`; latest attempts show 6 available units checked and no match.
- Reports load with rows: Backlog Request Register, Market Demand Gap Report, Backlog Matching Attempts Report.
- Workspace links are present in Sales & Rental, Executive Control Center, Reports & Analytics, and Real Estate Inventory.
- No notifications, reservations, contracts, invoices, Payment Entries, Journal Entries, or GL Entries were created.
- Current next action: Continue CMD-FINAL-01 Phase G: implement Maintenance foundation.

CMD-FINAL-01 Phase G property maintenance:
- Added `Property Maintenance Request` and `Property Maintenance Task`.
- Validation records for `REP-2026-00002`:
  - Requests `PMR-2026-00001` to `PMR-2026-00004`.
  - Linked maintenance tasks were created for each request.
  - Total estimated cost `9,000.00`; total actual cost `2,050.00`.
- Reports load with rows: Maintenance Request Register, Open Maintenance Requests, Maintenance Cost Summary, Maintenance by Unit Report.
- Workspace links are present in Real Estate Inventory, Executive Control Center, and Reports & Analytics.
- No accounting documents were created.
- Current next action: Continue CMD-FINAL-01 Phase H: implement Document Management foundation.

CMD-FINAL-01 Phase H property documents:
- Added `Property Document` and `Contract Attachment Register`.
- Validation records:
  - `PDOC-2026-00001` to `PDOC-2026-00003`.
  - `CAR-2026-00001` linked to `SC-PROJ-0002-001`.
- Reports load with rows: Property Document Register, Expiring Documents Report, Documents by Unit Report.
- Workspace links are present in Real Estate Inventory, Sales & Rental, Contractor Management, and Reports & Analytics.
- No external storage integration or accounting documents were created.
- Current next action: Continue CMD-FINAL-01 Phase I: implement Portal Readiness foundation.

CMD-FINAL-01 Phase I portal readiness:
- Added `Portal Access Profile` and `Portal Display Settings` under `Portal Readiness`.
- Validation records:
  - `PAP-2026-00001` Buyer linked to Sales Contract `SC-PROJ-0002-001`.
  - `PAP-2026-00002` Tenant linked to Lease Contract `LC-2026-00001`.
  - `PAP-2026-00003` Contractor linked to a PROJ-0002 Contractor Agreement / Subcontract.
  - `PAP-2026-00004` Owner linked to a Property Owner and Unit.
- Reports load with rows: Portal Access Register, Portal Access by Party.
- Workspace links are present in Sales & Rental, Real Estate Inventory, Contractor Management, Executive Control Center, and Reports & Analytics.
- No portal users, public routes, payment portal, Payment Entries, Journal Entries, or GL Entries were created.
- Current next action: Continue CMD-FINAL-01 Phase J: implement Notifications and Automation Readiness foundation.

CMD-FINAL-01 Phase J notifications and automation readiness:
- Added `Reminder Setting` and `Automation Log` under `Notification Readiness`.
- Default scenarios now exist for Reservation Expiry, Installment Due, Rent Due, Lease Expiry, Document Expiry, and Backlog Matched Unit.
- Validation records:
  - Reminder Settings `REMSET-2026-00001` to `REMSET-2026-00006`.
  - Pending internal Automation Logs `AUTOLOG-2026-00001` to `AUTOLOG-2026-00006`.
- Reports load with rows: Notification Readiness Report, Pending Reminder Actions.
- Workspace links are present in Sales & Rental, Real Estate Inventory, Contractor Management, Executive Control Center, and Reports & Analytics.
- No external messages, WhatsApp/Meta integration, Payment Entries, Journal Entries, or GL Entries were created.
- Current next action: Continue CMD-FINAL-01 Phase K: prepare permissions, print format readiness, and final QA documentation.

CMD-FINAL-01 Phase K final QA documentation:
- Added `.ai/ROLE_PERMISSION_MATRIX_DRAFT.md`.
- Added `.ai/PRINT_FORMAT_READINESS_PLAN.md`.
- Added `.ai/FULL_SYSTEM_QA_SCENARIOS.md`.
- Added `.ai/FINAL_COMPLETION_SUMMARY.md`.
- No permission restrictions, print format code, accounting documents, or workflow changes were applied.
- Current next action: Continue CMD-FINAL-01 Phase L: run final validation, update closure memory, and push final completion branch.

CMD-FINAL-01 Phase L final validation:
- Final validation passed for migration, cache clearing, and `bench build --app construct_erpnext`.
- Build note: unrelated `doppio/node_modules` asset link warning appears, but construct_erpnext assets build successfully.
- Representative report validation returned rows across construction, contractor agreements, sales, rent, commission, CRM, matching, backlog, maintenance, documents, portal readiness, and notification readiness.
- `ACC-SINV-2026-00002` remains submitted with outstanding `1,210,000.00`.
- `ACC-SINV-2026-00005` remains submitted with outstanding `175,000.00`.
- `ar.csv` parses cleanly.
- Current next action: Review final completed real estate ERP system and prepare production hardening / client UAT plan.

CMD-UAT-01 PROJ-0002 lease UAT finalization:
- Branch: `feature/proj-0002-uat-lease-demo-finalization`.
- Created one PROJ-0002 Lease Contract scenario through normal workflow:
  - Unit: `BLD-PROJ-000-001-S-G-02`.
  - Customer / tenant: `مستأجر تجاري محتمل`.
  - Reservation: `RES-2026-00006`.
  - Lease Contract: `LC-2026-00003`.
  - Lease status/workflow_state: `Active`.
  - Rent Schedule rows: 12.
  - Total scheduled rent: `948,000.00`.
- Unit status is now `Rented`.
- Reservation status is now `Converted`.
- Validated reports with rows:
  - Active Leases Report for `REP-2026-00002`.
  - Rent Schedule Report for `LC-2026-00003`.
  - Rental Value Summary for `REP-2026-00002`.
- No Rent Invoice, rent Payment Entry, Journal Entry, GL backfill, or raw SQL was created.
- Documentation corrected: `ACC-SINV-2026-00002` and `ACC-PAY-2026-00010` are no longer described as fully deferred; they are submitted/created controlled validation records for sales collections.
- Current next action: Run client UAT using PROJ-0002 scenario and collect feedback.
