# Implementation Log

## 2026-05-09 14:52:21 CEST

- Project memory initialized.

## 2026-05-09 14:55:56 CEST

- Audited El Salvador localization references in hooks, installer, tax setup, payroll setup, withholding logic, Salary Slip override, setup custom fields, and README.
- Disabled automatic El Salvador setup from after_install and replaced it with generic setup logging.
- Removed Purchase Invoice validate hook for El Salvador withholding logic while keeping Purchase Invoice submit authorization.
- Moved legacy El Salvador installer helpers out of install.py into setup/legacy_el_salvador.py so install.py has no active SV setup path.
- Updated README to state country-specific localization is disabled and must be implemented per deployment.

## 2026-05-09 15:05:31 CEST

- Backed up construction.yemenfrappe.com with files before installation.
- Backup files:
  - sites/construction.yemenfrappe.com/private/backups/20260509_183222-construction_yemenfrappe_com-site_config_backup.json
  - sites/construction.yemenfrappe.com/private/backups/20260509_183222-construction_yemenfrappe_com-database.sql.gz
  - sites/construction.yemenfrappe.com/private/backups/20260509_183222-construction_yemenfrappe_com-files.tar
  - sites/construction.yemenfrappe.com/private/backups/20260509_183222-construction_yemenfrappe_com-private-files.tar
- Registered the existing cleaned checkout as apps/construct_erpnext via symlink to apps/Construct-erpnext and installed it editable in the bench environment.
- Installed construct_erpnext on construction.yemenfrappe.com; HRMS was installed automatically first because construct_erpnext declares it as a required app.
- Cleared site cache and website cache.
- Verified zero matches for requested El Salvador artifacts: sv_* target fields, IVA/ISR accounts/templates, and ISSS/AFP/Aguinaldo/ISR salary components.
- Verified Purchase Invoice validate no longer runs construct_erpnext El Salvador withholding logic; Purchase Invoice submit authorization remains active.

## 2026-05-09 15:07:11 CEST

- Reviewed current modules, workspace labels, DocTypes, reports, roles, and legacy localization terms for Product Stabilization.
- Identified current user-facing workspaces as implementation-era GCS workspaces.
- Defined final product workspace structure and role-oriented navigation in ARCHITECTURE.md.
- Classified existing DocTypes into reuse-now and hide-from-primary-navigation groups.
- Updated roadmap Phase 2 to focus on Workspace/UX cleanup without BOQ, IPC, or real estate schema changes.

## 2026-05-09 15:27:51 CEST

- Confirmed apps/construct_erpnext is a symlink to apps/Construct-erpnext, not a duplicate repository.
- Recorded canonical repository path as /home/frappe/frappe-bench/apps/Construct-erpnext.
- Recorded ERPNext v15 deployment decision for construction.yemenfrappe.com.
- Prepared current project memory and delocalization changes for commit.

## 2026-05-09 15:29:54 CEST

- Committed project memory and delocalization changes as 2606941.
- Pushed feature/product-delocalization to origin and set upstream tracking.
- Started v15 compatibility smoke test for construction.yemenfrappe.com.
- Site-level smoke checks were blocked because MariaDB on 127.0.0.1 refused connections.
- Static metadata check confirmed the requested DocType JSON files exist for Construction Budget, Budget Level, Physical Advancement, Project Cost Entry, Labor Hour Entry, Equipment Usage Log, Invoice Authorization, and Check Request.
- Static hook inspection confirmed construct_erpnext overrides and document events load from hooks.py, with Purchase Invoice submit authorization active and no construct_erpnext Purchase Invoice validate withholding hook.

## 2026-05-09 16:14:06 CEST

- Stopped previous workspace cleanup thread to make final canonical path decision.
- Verified apps/construct_erpnext was a symlink to apps/Construct-erpnext.
- Removed the symlink and renamed the real repository folder from /home/frappe/frappe-bench/apps/Construct-erpnext to /home/frappe/frappe-bench/apps/construct_erpnext.
- Verified branch feature/product-delocalization and clean git state after rename.
- Refreshed editable install with ./env/bin/pip install -e apps/construct_erpnext.
- Verified bench virtualenv import path resolves to /home/frappe/frappe-bench/apps/construct_erpnext/construct_erpnext/__init__.py.
- Plain system python3 import still fails because it is not using the bench virtualenv.

## 2026-05-09 16:31:59 CEST

- Implemented product-facing Workspace JSON fixtures for Executive Control Center, Construction Control, Procurement & Site Warehouses, Measurement & IPC, Contractor Management, Real Estate Inventory, Sales & Rental, and Reports & Analytics.
- Marked legacy GCS workspace JSON files as hidden and non-public.
- Added reversible patch construct_erpnext.patches.hide_legacy_gcs_workspaces because Frappe did not update existing workspace visibility from JSON alone.
- Ran migration on construction.yemenfrappe.com to sync workspaces and execute the visibility patch.
- Verified 8 product workspaces are visible and 8 legacy GCS workspaces are hidden/non-public.
- Verified existing construct DocType count remains 72 and no BOQ, IPC, Measurement Book, or Real Estate DocTypes were created.
- Verified product workspace links resolve statically and cleared site/website cache.

## 2026-05-09 17:01:22 CEST

- Created branch feature/construction-boq-foundation from feature/product-delocalization.
- Inspected existing Construction Budget, Budget Level, Project Cost Entry, Physical Advancement, Budget Change Order, Material Distribution, Insumo, and Insumo Price Scenario structures before implementing BOQ.
- Added internal Construction BOQ module inside construct_erpnext without renaming the package.
- Added DocTypes: Cost Code, WBS Element, Construction BOQ, Construction BOQ Item, and Construction Work Item.
- Implemented Document Controllers for BOQ item calculations, BOQ category totals, BOQ variance, WBS validation, Cost Code restrictions, and Work Item tracking calculations.
- Added Construction BOQ Approval Workflow through an idempotent after_migrate setup hook because Workflow records sync after DocType schema sync in Frappe v15.
- Added Script Reports: Construction BOQ Cost Analysis and Construction BOQ Variance.
- Updated Construction Control and Reports & Analytics workspace JSON with BOQ links.
- Ran python compile and JSON validation checks successfully.
- Ran bench migrate, clear-cache, and clear-website-cache on construction.yemenfrappe.com.
- Verified new DocTypes, reports, workflow, workspace links, BOQ calculations, workflow approval, work-item generation, and report loading using rollback-only validation records.
- Verified existing construct DocTypes remain accessible.

## 2026-05-09 17:21:02 CEST

- Created branch feature/boq-procurement-control from feature/construction-boq-foundation.
- Inspected ERPNext procurement, stock, and warehouse DocType fields before adding app-level Custom Fields.
- Added internal Procurement Control module inside construct_erpnext without modifying ERPNext core.
- Added Procurement Control Settings as a Single DocType for sync, warning, blocking, tolerance, and default site warehouse behavior.
- Added idempotent Custom Field setup for Material Request Item, Purchase Order Item, Purchase Receipt Item, Purchase Invoice Item, Stock Entry Detail, and Warehouse.
- Extended Construction Work Item with procurement quantity, amount, status, and variance tracking fields.
- Added procurement hooks to auto-fill BOQ metadata on procurement rows and recalculate Work Item procurement totals after submit/cancel.
- Preserved existing Purchase Invoice authorization and Stock Entry material hooks while keeping El Salvador withholding disabled.
- Added draft Material Request generation from material Work Items as a whitelisted app method.
- Added Script Reports: Work Item Procurement Summary, BOQ Procurement Pipeline, Site Warehouse Consumption, and Procurement Budget Control.
- Updated Procurement & Site Warehouses and Reports & Analytics workspaces with procurement control links.
- Ran migration and cache clears on construction.yemenfrappe.com.
- Validated custom fields, settings, reports, workspaces, metadata sync, procurement recalculation, and report loading with rollback-only records.
- Full normal Material Request workflow validation is pending baseline ERPNext Company, Item Group, UOM, and Item masters on the site.

## 2026-05-09 17:42:32 CEST

- Created branch feature/operational-baseline-procurement-smoke from feature/boq-procurement-control.
- Inspected construction.yemenfrappe.com baseline masters and found no Company, Fiscal Year, Cost Center, Warehouse, UOM, Item Group, Item, Supplier, or Project records.
- Created reusable operational baseline records:
  - Company: Yemen Construction & Real Estate Development
  - Fiscal Year: 2026
  - UOM: Nos, m, m2, m3, kg
  - Supplier Group: All Supplier Groups
  - Item Groups: All Item Groups, Construction Materials, Construction Services
  - Cost Center: Al Nakheel Tower Development - YCRE
  - Site Warehouse: Al Nakheel Site Warehouse - YCRE
  - Supplier: Al Amal Contracting
  - Items: Concrete C30, Reinforcement Steel, Contractor Service
  - Project: Al Nakheel Tower Development / PROJ-0001
- Allowed ERPNext to create the standard chart of accounts and default company warehouses for YCRE, then configured Global Defaults and Procurement Control Settings.
- Set System Settings language to en and time zone to Asia/Aden because amount-in-words generation was blocked when the locale was unset.
- Created and retained BOQ validation records:
  - Cost Code: STR-CONC
  - WBS Element: PROJ-0001-01.01
  - Construction BOQ: ANK-BOQ-FOUNDATION-001
  - Construction Work Item: CWI-2026-00001
- Ran full procurement validation through ERPNext documents:
  - Material Request MAT-MR-2026-00001 submitted.
  - Purchase Order PUR-ORD-2026-00003 submitted.
  - Purchase Receipt MAT-PRE-2026-00001 submitted.
  - Purchase Invoice ACC-PINV-2026-00001 submitted with Invoice Authorization IA-00001.
  - Stock Entry MAT-STE-2026-00001 submitted for material issue/consumption.
- Verified Construction Work Item procurement totals:
  - requested_qty 100, ordered_qty 100, received_qty 100, invoiced_qty 100, consumed_qty 25.
  - committed_amount 3500000, invoiced_amount 3500000, consumed_amount 875000.
  - procurement_status Fully Invoiced.
- Verified reports load: Work Item Procurement Summary, BOQ Procurement Pipeline, Site Warehouse Consumption, Procurement Budget Control, Construction BOQ Cost Analysis, Construction BOQ Variance.
- Verified workspaces load: Executive Control Center, Construction Control, Procurement & Site Warehouses, Reports & Analytics.
- Kept baseline and submitted validation records because they are realistic reusable implementation records needed for future validation.

## 2026-05-09 18:32:29 CEST

- Created branch feature/measurement-book-foundation from feature/operational-baseline-procurement-smoke.
- Normalized reusable operational baseline records to clear Arabic, non-country-specific names:
  - Company: شركة التطوير العقاري والبناء
  - Project: مشروع البرج السكني المتكامل / PROJ-0001
  - Cost Center: مركز تكلفة - مشروع البرج السكني المتكامل - RED
  - Site Warehouse: مخزن موقع مشروع البرج السكني المتكامل - RED with site_code SITE-001
  - Supplier: مقاول الأعمال الإنشائية
  - Items: خرسانة جاهزة C30, حديد تسليح, خدمة مقاول أعمال إنشائية
  - UOMs: عدد, متر, متر مربع, متر مكعب, كجم
  - Item Groups: مواد البناء, خدمات المقاولين
  - Cost Code: CC-CONC / أعمال الخرسانة الإنشائية
  - WBS Element: PROJ-0001-01.01 / أعمال خرسانة الأساسات
- Set System Settings language to ar and kept the existing timezone unchanged.
- Retained ERPNext Company country value because Country is mandatory and no generic Country master exists.
- Retained submitted Construction BOQ document number ANK-BOQ-FOUNDATION-001 because it is linked to submitted procurement records; Arabic title/description is stored in remarks.
- Added internal Measurement IPC module and created DocTypes: Measurement Book and Measurement Entry.
- Extended Construction Work Item with measured quantity, measurement amount, measurement progress, last measurement date, and measurement status fields.
- Implemented Document Controllers and utility functions for measurement metadata fetch, quantity calculations, previous/cumulative/remaining quantities, Measurement Book totals, and Work Item measurement recalculation.
- Added Measurement Book Verification Workflow through an idempotent after_migrate setup hook for Frappe v15 compatibility.
- Added Script Reports: Measurement Book Register, Work Item Measurement Progress, and Measurement Verification Queue.
- Updated Measurement & IPC and Reports & Analytics workspaces with measurement links.
- Ran bench migrate, clear-cache, and clear-website-cache on construction.yemenfrappe.com.
- Created and retained reusable Arabic measurement validation records:
  - Measurement Book: MB-2026-00001 / قياسات أعمال خرسانة الأساسات
  - Measurement Entry: ME-2026-00001 for CWI-2026-00001
- Verified Measurement Book workflow transitions Draft -> Submitted -> Under Verification -> Verified.
- Verified Measurement Entry calculations: accepted_qty 25, cumulative_measured_qty 25, remaining_qty 75, measured_amount 875000.
- Verified Construction Work Item measurement values: measured_qty 25, measurement_progress_percent 25, measurement_status Partially Measured, certified_qty remains 0.
- Verified procurement reports, measurement reports, product workspaces, Construction BOQ, and Construction Work Item still load.
- Confirmed Interim Payment Certificate DocType was not created.

## 2026-05-09 19:29:32 CEST

- Performed a site health repair pass for construction.yemenfrappe.com before starting IPC foundation.
- Verified installed site apps: frappe, erpnext, hrms, and construct_erpnext on branch feature/measurement-book-foundation.
- Found scheduler disabled/inactive through bench doctor.
- Enabled scheduler for construction.yemenfrappe.com.
- Re-ran bench doctor and confirmed scheduler is no longer reported disabled/inactive; workers online: 2.
- Cleared site cache and website cache.
- Ran a read-only DocType fetch through bench execute to confirm site/database access is healthy.
- No ERPNext core changes, schema changes, migrations, or new DocTypes were performed during this repair pass.

## 2026-05-09 19:57:46 CEST

- Created branch feature/ipc-foundation from feature/measurement-book-foundation.
- Inspected Subcontract, Subcontract Activity, Supplier, Construction Work Item, Measurement Book, Measurement Entry, Construction BOQ, Project Cost Entry, Invoice Authorization, Purchase Invoice, and Payment Entry context before coding.
- Decided to use existing Subcontract as the optional contractor contract reference for IPC because it supports project, contractor, company, contract title, status, amount, activities, and dates.
- Added Interim Payment Certificate, Interim Payment Certificate Line, and IPC Deduction DocTypes inside measurement_ipc.
- Converted Measurement Entry interim_payment_certificate placeholder from Data to Link once IPC DocType existed; retained ipc_line_reference as Data for child-row traceability.
- Added IPC generation from verified Measurement Book entries through construct_erpnext.measurement_ipc.ipc.create_ipc_from_measurement_book.
- Implemented IPC controller calculations, duplicate Measurement Entry prevention, workflow/status sync, Measurement Entry linking/releasing, Work Item certification recalculation, draft Purchase Invoice creation, and payment status update hooks.
- Extended Construction Work Item with certified_amount, certification_progress_percent, last_ipc, last_certification_date, and certification_status.
- Added Interim Payment Certificate Approval Workflow through after_migrate setup.
- Added Script Reports: IPC Register, IPC Line Details, Measurement to IPC Traceability, and Contractor IPC Summary.
- Updated Measurement & IPC, Contractor Management, Executive Control Center, and Reports & Analytics workspace links for IPC.
- Ran JSON validation, Python compile checks, migration, site cache clear, and website cache clear.
- Fixed site module map by adding construct_erpnext to /home/frappe/frappe-bench/sites/apps.txt because the site had the app installed but the bench app list did not include it.
- Created retained Arabic validation IPC:
  - IPC: IPC-2026-00001
  - Certificate number: IPC-001
  - Remarks: مستخلص رقم 1 لأعمال خرسانة الأساسات
  - Source Measurement Book: MB-2026-00001 / قياسات أعمال خرسانة الأساسات
  - Measurement Entry: ME-2026-00001
- Verified IPC workflow transitions Draft -> Submitted -> Under Review -> Certified -> Approved.
- Verified IPC calculations: gross_amount 875000, retention_amount 87500, net_payable 787500.
- Verified Work Item certification values: certified_qty 25, certified_amount 875000, certification_progress_percent 25, certification_status Partially Certified, remaining_qty 75.
- Created draft Purchase Invoice ACC-PINV-2026-00002 from approved IPC; it remains unsubmitted to preserve existing Invoice Authorization controls.
- Verified IPC status moved to Invoice Created and outstanding_amount is 787500 while Purchase Invoice is draft.
- Verified IPC reports, measurement reports, procurement reports, and product workspaces load.
- Confirmed Contractor Ledger, Contractor Contract, and Real Estate Unit DocTypes were not created.

## 2026-05-09 21:41:05 CEST

- Created branch feature/contractor-ledger-retention from feature/ipc-foundation.
- Inspected contractor and finance context from existing app DocTypes and IPC implementation before coding.
- Added internal Contractor Management module foundation.
- Created DocTypes: Contractor Account, Contractor Ledger Entry, Retention Register, Advance Register, and Guarantee Register.
- Implemented contractor_management.ledger_utils for idempotent contractor account creation, ledger entry creation, retention creation from IPC, advance recovery from IPC, Purchase Invoice sync, Payment Entry sync, account recalculation, reversal entries, and explicit existing IPC sync.
- Integrated Interim Payment Certificate submission/cancellation and draft Purchase Invoice creation with the operational contractor ledger.
- Added Payment Entry and Purchase Invoice hooks that read ERPNext accounting documents and update operational contractor controls without overriding standard accounting behavior.
- Added Script Reports: Contractor Account Statement, Retention Register Report, Advance Recovery Report, Contractor Exposure Summary, and Guarantee Register Report.
- Updated Contractor Management, Executive Control Center, and Reports & Analytics workspaces with contractor ledger and retention links.
- No Journal Entry automation was added.
- MariaDB recovered after an OOM-kill failure and the site migration completed successfully.
- Cleared site cache and website cache.
- Synchronized existing Arabic IPC IPC-2026-00001 into the contractor ledger through the explicit sync helper.
- Created Contractor Account CA-2026-00001 for مقاول الأعمال الإنشائية and مشروع البرج السكني المتكامل.
- Created ledger entries for IPC Certified, Retention Held, and Purchase Invoice Created.
- Created Retention Register RET-2026-00001 with retention amount 87500, remaining retention 87500, and release due date 2027-05-09.
- Verified Contractor Account totals: certified 875000, retention held 87500, invoiced 875000, paid 0, operational outstanding 787500.
- Verified reports load: Contractor Account Statement, Retention Register Report, Advance Recovery Report, Contractor Exposure Summary, Guarantee Register Report.
- Verified workspaces load: Contractor Management, Executive Control Center, Reports & Analytics.
- Purchase Invoice ACC-PINV-2026-00002 remains draft; Payment Entry validation remains pending until standard invoice submission/authorization is completed.

## 2026-05-09 21:55:15 CEST

- Created branch feature/cfo-financial-snapshot from feature/contractor-ledger-retention.
- Inspected existing field structures for Construction BOQ, Construction Work Item, Measurement Entry, Interim Payment Certificate, Contractor Account, Retention Register, and ERPNext procurement child tables before coding.
- Added internal CFO Analytics module.
- Created Project Financial Snapshot DocType.
- Implemented construct_erpnext.cfo_analytics.project_financials with deterministic aggregation for BOQ totals, procurement totals, measurement totals, IPC totals, contractor totals, variances, progress percentages, and risk statuses.
- Added whitelisted methods get_snapshot_data and create_snapshot.
- Added Script Reports: Project Financial Snapshot Report, CFO Project Control Summary, Work Item Financial Traceability, and Contractor Financial Exposure.
- Updated Executive Control Center and Reports & Analytics workspace links.
- Ran migration, site cache clear, and website cache clear on construction.yemenfrappe.com.
- Created retained Arabic validation snapshot:
  - Project Financial Snapshot: PFS-2026-00001
  - Title: الملخص المالي لمشروع البرج السكني المتكامل
- Verified snapshot values:
  - BOQ total 3500000
  - requested_amount 3500000
  - committed_amount 3500000
  - received_amount 3500000
  - procurement_invoiced_amount 3500000
  - consumed_amount 875000
  - measured_amount 875000
  - certified_gross_amount 875000
  - certified_net_amount 787500
  - retention_held_amount 87500
  - contractor_outstanding_amount 787500
  - procurement_progress_percent 100
  - measurement_progress_percent 25
  - certification_progress_percent 25
  - cost_risk_status Yellow
  - cash_risk_status Red
  - overall_status At Risk
- Verified new CFO reports, existing procurement report, measurement report, IPC report, Contractor Account Statement, Executive Control Center, and Reports & Analytics load successfully.
- No Journal Entry, Cash Flow Forecast full engine, scheduled EVM automation, Real Estate Inventory, or El Salvador localization was created.

## 2026-05-09 22:06:26 CEST

- Created branch feature/cash-flow-forecast-foundation from feature/cfo-financial-snapshot.
- Inspected live ERPNext and app field metadata for Purchase Order, Purchase Order Item, Purchase Invoice, Purchase Invoice Item, Payment Entry, Payment Entry Reference, IPC, Retention Register, Contractor Account, Contractor Ledger Entry, Project Financial Snapshot, Construction Work Item, and Construction BOQ.
- Added Project Cash Flow Forecast and Project Cash Flow Forecast Period DocTypes inside cfo_analytics.
- Implemented construct_erpnext.cfo_analytics.cash_flow_forecast with deterministic period building, source aggregation, double-counting prevention, running balance, deficit, and cash risk calculations.
- Added whitelisted methods get_forecast_data and create_forecast.
- Added reports: Project Cash Flow Forecast Report, Project Cash Requirement Summary, Contractor Payment Forecast, and Retention Release Forecast.
- Updated Executive Control Center and Reports & Analytics with cash flow forecast links.
- Ran migration, site cache clear, and website cache clear on construction.yemenfrappe.com.
- Created retained Arabic validation forecast:
  - Project Cash Flow Forecast: PCF-2026-00001
  - Title: توقع التدفق النقدي لمشروع البرج السكني المتكامل
  - Period: Monthly from 2026-05-01 to 2026-10-31
  - Opening balance: 0
- Verified forecast values:
  - total_expected_inflow 0
  - purchase_order_outflow 0 because the submitted Purchase Order is fully invoiced
  - purchase_invoice_outflow 3500000 from submitted Purchase Invoice outstanding
  - ipc_outflow 787500 because IPC-2026-00001 has only a draft linked Purchase Invoice
  - retention_release_outflow 0 because retention release due date 2027-05-09 is outside the six-month validation range
  - total_expected_outflow 4287500
  - net_cash_flow -4287500
  - lowest_projected_balance -4287500
  - cash_risk_status Red
- Verified cash flow reports, existing Project Financial Snapshot, IPC, Contractor Account, Executive Control Center, and Reports & Analytics load successfully.
- No Journal Entry, Payment Entry, Purchase Invoice submission, EVM scheduled task, Real Estate Inventory, Sales/Rental DocTypes, or El Salvador localization was created.

## 2026-05-09 22:26:27 CEST

- Created branch feature/evm-metrics-foundation from feature/cash-flow-forecast-foundation.
- Inspected Project, Construction BOQ, Construction Work Item, Project Financial Snapshot, Project Cash Flow Forecast, IPC, Contractor Account, Contractor Ledger Entry, Purchase Invoice, Stock Entry Detail, Physical Advancement, Activity Schedule, Construction Budget, and Budget Level source fields before implementation.
- Added Project EVM Metrics DocType inside cfo_analytics.
- Implemented construct_erpnext.cfo_analytics.evm_metrics with deterministic BAC, EV, AC, PV, CV, SV, CPI, SPI, EAC, ETC, VAC, TCPI, actual progress, forecast overrun, and risk calculations.
- Added whitelisted methods get_evm_data and create_evm_snapshot.
- Added reports: Project EVM Metrics Report, EVM Forecast Summary, and Project Performance Dashboard Report.
- Updated Executive Control Center and Reports & Analytics workspace links.
- Ran JSON validation, Python compile checks, migration, site cache clear, and website cache clear.
- Created retained Arabic validation EVM snapshot:
  - Project EVM Metrics: EVM-2026-00001
  - Title: مؤشرات القيمة المكتسبة لمشروع البرج السكني المتكامل
  - Planned progress percent: 30
- Verified EVM values:
  - BAC 3500000
  - EV 875000
  - AC 3500000
  - PV 1050000
  - CV -2625000
  - SV -175000
  - CPI 0.25
  - SPI 0.833333333
  - EAC 14000000
  - ETC 10500000
  - VAC -10500000
  - TCPI 0
  - forecast_overrun_amount 10500000
  - actual_progress_percent 25
  - cost_status Red
  - schedule_status Red
  - overall_evm_status At Risk
- Verified EVM reports, existing Project Financial Snapshot, existing Cash Flow Forecast, existing IPC, existing Contractor Account, Executive Control Center, and Reports & Analytics load successfully.
- No scheduled jobs, Journal Entries, accounting documents, Real Estate Inventory, Sales/Rental DocTypes, or El Salvador localization were created.

## 2026-05-09 22:42:21 CEST

- Created branch feature/real-estate-inventory-foundation from feature/evm-metrics-foundation.
- Added internal Real Estate Inventory module.
- Created DocTypes: Real Estate Project, Building, Floor, Unit Type, Unit, Property Owner, and Property Ownership.
- Implemented inventory_utils and Document Controllers for:
  - Real Estate Project uniqueness per ERPNext Project.
  - Building code uniqueness per Real Estate Project.
  - Floor code uniqueness per Building.
  - Unit code uniqueness per Building/Floor.
  - Unit status and marketing_status alignment.
  - Unit expected margin and expected margin percent calculation.
  - Real Estate Project, Building, and Floor unit count recalculation.
  - Property Ownership percentage validation with active ownership total capped at 100 percent.
- Corrected Property Ownership technical fieldname from owner to property_owner because owner is reserved by Frappe document metadata.
- Added reports: Unit Inventory Report, Unit Availability Report, Ownership Summary Report, and Real Estate Project Summary.
- Updated Real Estate Inventory, Executive Control Center, and Reports & Analytics workspace links.
- Ran JSON validation, Python compile checks, migration, site cache clear, and website cache clear.
- Created retained Arabic validation inventory:
  - Real Estate Project: REP-2026-00001 / مشروع البرج السكني المتكامل العقاري.
  - Building: A / البرج A.
  - Floors: A-G الطابق الأرضي, A-01 الطابق الأول, A-02 الطابق الثاني.
  - Unit Types: شقة سكنية, محل تجاري, موقف سيارة, مخزن.
  - Units: A-101, A-102, A-201, A-G01, P-01.
  - Property Owner: POWN-2026-00001 / مالك استثماري رئيسي.
  - Property Ownership: OWN-2026-00001, A-101 owned 100 percent by مالك استثماري رئيسي.
- Verified unit counts:
  - Project total_units 5, available 3, reserved 1, sold 0, rented 1, blocked 0.
  - Building A total_units 5.
  - Floors A-G total_units 2, A-01 total_units 2, A-02 total_units 1.
- Verified Unit margin calculations and status/marketing_status alignment.
- Verified over-ownership validation blocks active ownership above 100 percent.
- Verified inventory reports, Real Estate Inventory workspace, Executive Control Center, Reports & Analytics, and existing EVM/Cash Flow/IPC reports load.
- Confirmed no tenant fields exist on Unit and no Lease Contract, Sales Contract, Reservation, Smart Matching, accounting documents, or El Salvador localization were introduced.

## 2026-05-09 23:05:22 CEST

- Created branch feature/unit-cost-profitability-foundation from feature/real-estate-inventory-foundation.
- Inspected Real Estate Project, Building, Floor, Unit, Project Financial Snapshot, Project Cash Flow Forecast, Project EVM Metrics, Construction BOQ, Construction Work Item, Purchase Invoice, Stock Entry, Interim Payment Certificate, Contractor Account, and Project Cost Entry fields before implementation.
- Added internal Unit Costing module.
- Created DocTypes: Unit Cost Allocation and Unit Cost Allocation Line.
- Updated Unit with latest_cost_allocation, allocated_cost_source, allocated_cost_date, and profitability_status fields while reusing existing allocated_cost, expected_sale_price, expected_monthly_rent, expected_margin, and expected_margin_percent fields.
- Implemented construct_erpnext.unit_costing.allocation_utils for project cost source lookup, unit selection, allocation calculation, allocation application, unit profitability recalculation, and whitelisted allocation helpers.
- Added an idempotent Unit Costing after_migrate workspace sync so installed Workspace records receive the new links reliably.
- Added reports: Unit Cost Allocation Report, Unit Profitability Report, Real Estate Project Profitability Summary, and Building Profitability Summary.
- Updated Real Estate Inventory, Executive Control Center, and Reports & Analytics workspace links.
- Ran JSON validation, Python compile checks, migration, site cache clear, and website cache clear.
- Updated retained Arabic validation units with requested area and expected sale values.
- Created and applied Unit Cost Allocation UCA-2026-00001:
  - Real Estate Project: REP-2026-00001 / مشروع البرج السكني المتكامل العقاري.
  - Allocation basis: By Area.
  - Cost source: BOQ Total.
  - Source amount: 3500000.
  - Total allocated amount: 3500000.
  - Unallocated amount: 0.
  - Remarks: توزيع تكلفة مشروع البرج السكني على الوحدات.
- Verified unit profitability results:
  - A-101 allocated 928030.303, margin 271969.697, margin percent 22.664141414, Profitable.
  - A-102 allocated 861742.424, margin 288257.576, margin percent 25.065876153, Profitable.
  - A-201 allocated 994318.182, margin 305681.818, margin percent 23.513986014, Profitable.
  - A-G01 allocated 596590.909, margin 1203409.091, margin percent 66.856060606, Profitable.
  - P-01 allocated 119318.182, margin 30681.818, margin percent 20.454545455, Profitable.
- Verified project profitability summary: 5 units, total area 528, expected sales value 5600000, allocated cost 3500000, expected gross margin 2100000, expected margin 37.5 percent.
- Verified Unit Costing reports, existing Unit Inventory Report, EVM report, IPC Register, and product workspaces load successfully.
- Confirmed no tenant fields exist on Unit and no Lease Contract, Sales Contract, Reservation, Smart Matching, Journal Entries, accounting documents, Server Scripts, or El Salvador localization were introduced.

## 2026-05-10 09:16:27 CEST

- Created branch feature/financial-dimensions-traceability from feature/unit-cost-profitability-foundation.
- Audited ERPNext v15 Accounting Dimension implementation and accounting_dimension_doctypes on construction.yemenfrappe.com.
- Existing Accounting Dimension records before this task: none.
- Existing operational fields before this task:
  - construction_work_item and cost_code already existed on Material Request Item, Purchase Order Item, Purchase Receipt Item, Purchase Invoice Item, and Stock Entry Detail.
  - Existing fields were Link fields with correct options and were safely reused by the Accounting Dimension setup.
  - Unit dimension field did not exist on target accounting rows before this task.
- Added ADR-017 for the dual tracking model: operational tracking remains for BOQ/Measurement/IPC/Contractor Ledger/Unit Cost Allocation, while Accounting Dimensions support financial reporting and GL drilldown.
- Added Single DocType Financial Dimension Settings with non-blocking defaults.
- Added idempotent CFO Analytics after_migrate setup to create Accounting Dimensions:
  - Construction Work Item / construction_work_item
  - Cost Code / cost_code
  - Unit / unit
- ERPNext Accounting Dimension setup created or reused dimension fields on supported doctypes, including GL Entry, Journal Entry Account, Purchase Invoice Item, Sales Invoice Item, Purchase Order Item, Purchase Receipt Item, Material Request Item, Stock Entry Detail, and Payment Entry.
- Added financial dimension sync service:
  - sync_dimensions_on_row
  - validate_dimension_doc
  - backfill_draft_dimensions
  - get_dimension_field_map
- Integrated dimension sync into validate hooks for Material Request, Purchase Order, Purchase Receipt, Purchase Invoice, Stock Entry, Journal Entry, and Sales Invoice.
- Preserved existing procurement metadata sync, Purchase Invoice authorization, contractor ledger events, and disabled El Salvador withholding.
- Added reports:
  - GL Dimension Traceability
  - Unit Financial Ledger
  - Work Item Financial Ledger
  - Cost Code Financial Analysis
  - Project Unit Cost Matrix
- Updated Executive Control Center, Reports & Analytics, Real Estate Inventory, and Construction Control workspace links.
- Ran JSON validation, Python compile checks, migration, site cache clear, and website cache clear.
- Draft-only validation:
  - Ran backfill_draft_dimensions on draft Purchase Invoice ACC-PINV-2026-00002.
  - Purchase Invoice Item retained construction_work_item CWI-2026-00001 and cost_code CC-CONC.
  - Unit remained blank because the IPC Purchase Invoice is project-level contractor cost, and blank Unit is allowed by settings.
  - Document remained Draft and was not submitted.
- New traceability reports load successfully and degrade safely for existing historical GL rows that predate dimensions.
- Existing Project Financial Snapshot Report, Unit Profitability Report, and IPC Register still load successfully.
- No Reservation, Sales Contract, Lease Contract, CRM Matching, accounting document, broad GL backfill, submitted-document amendment, utility-billing install, or El Salvador localization was introduced.
- Arabic implementation note: تم تفعيل أبعاد مالية مبدئية تسمح بتحليل التكلفة حسب بند العمل، كود التكلفة، والوحدة العقارية، مع بقاء القياسات والمستخلصات كمسار تشغيلي مستقل.

## 2026-05-10 09:32:24 CEST

- Created branch feature/end-to-end-traceability-validation from feature/financial-dimensions-traceability.
- Validated Accounting Dimensions on construction.yemenfrappe.com:
  - Construction Work Item / construction_work_item.
  - Cost Code / cost_code.
  - Unit / unit.
- Verified Financial Dimension Settings remains warning/non-blocking by default.
- Verified expected dimension fields exist on Purchase Invoice Item, Stock Entry Detail, Journal Entry Account, GL Entry, and Sales Invoice Item.
- Ran draft-only dimension backfill on ACC-PINV-2026-00002.
- Confirmed ACC-PINV-2026-00002 remains Draft and its item row has construction_work_item CWI-2026-00001, cost_code CC-CONC, project PROJ-0001, construction_boq ANK-BOQ-FOUNDATION-001, and wbs_element PROJ-0001-01.01.
- Unit remains blank on ACC-PINV-2026-00002 because this is a project-level contractor cost and blank Unit is allowed by settings.
- Did not submit ACC-PINV-2026-00002 because Invoice Authorization is active and no Authorized Invoice Authorization exists for that invoice.
- Verified MAT-STE-2026-00001 Stock Entry Detail is linked to CWI-2026-00001 and CC-CONC.
- Documented that MAT-STE-2026-00001 GL rows have blank new dimension values because the Stock Entry was submitted before Accounting Dimensions were enabled.
- Ran traceability reports and confirmed they load without errors:
  - GL Dimension Traceability.
  - Unit Financial Ledger.
  - Work Item Financial Ledger.
  - Cost Code Financial Analysis.
  - Project Unit Cost Matrix.
  - Work Item Procurement Summary.
  - Construction BOQ Variance.
  - Measurement to IPC Traceability.
  - Contractor Account Statement.
  - Project Financial Snapshot Report.
  - Project Cash Flow Forecast Report.
  - Project EVM Metrics Report.
  - Unit Profitability Report.
- Added .ai/TRACEABILITY_VALIDATION.md with the end-to-end checklist, known limitations, and recommendation to proceed.
- No submitted documents were amended, no historical GL backfill was run, no accounting documents were created, and no Reservation/Sales/Rental DocTypes were created.
- Arabic validation note: تم التحقق من مسار التتبع الكامل من جدول الكميات إلى بند العمل والمشتريات والمخزون والقياسات والمستخلصات والأبعاد المالية والتقارير، مع بقاء قيود دفتر الأستاذ التاريخية دون تعديل.

## 2026-05-10 10:05:00 CEST

- Created branch feature/product-readiness-bilingual-ux from feature/end-to-end-traceability-validation.
- Audited completed product modules:
  - construction_boq
  - procurement_control
  - measurement_ipc
  - contractor_management
  - cfo_analytics
  - real_estate_inventory
  - unit_costing
  - cfo_analytics financial dimension helpers
- Added concise English DocType descriptions for completed product DocTypes and key field descriptions for important workflow/control fields.
- Confirmed all custom Script Report column labels in completed modules use Frappe translation wrappers.
- Added curated Arabic translation file:
  - construct_erpnext/translations/ar.csv
  - 248 valid CSV rows covering product DocTypes, workspaces, reports, workflow states, report columns, and key descriptions.
- Polished product-facing workspace grouping in JSON and added an idempotent after_migrate readiness sync:
  - construct_erpnext.setup.product_readiness.sync_product_workspace_readiness
- Kept Sales & Rental as a placeholder with a clear future-phase note.
- Created Arabic client presentation walkthrough:
  - .ai/CLIENT_PRESENTATION_WALKTHROUGH.md
- Created product readiness checklist:
  - .ai/PRODUCT_READINESS_CHECKLIST.md
- Validation completed:
  - Metadata JSON and Arabic CSV parse successfully.
  - python3 compileall passed.
  - Migration, clear-cache, and clear-website-cache completed successfully after correcting the readiness sync path helper.
  - All custom product DocTypes loaded.
  - All eight product workspaces loaded.
  - All requested custom reports loaded without errors.
  - Legacy GCS workspaces remain hidden and non-public.
  - No Reservation, Sales Contract, Lease Contract, CRM Matching, Portal feature, accounting document, submitted-document amendment, or GL backfill was created.
- Dashboard/card decision: no Number Cards or Dashboard Charts were created in this phase because executive metrics should be signed off with finance leadership before promotion; existing executive reports are linked and presentation-ready.

## 2026-05-10 Unit Reservation Foundation

- Created branch feature/unit-reservation-foundation from feature/product-readiness-bilingual-ux.
- Added Unit Reservation Settings Single DocType.
- Added Unit Reservation submittable transaction DocType with controller logic for:
  - reservation number generation,
  - unit metadata fetch,
  - party/date/amount validation,
  - duplicate active reservation prevention,
  - Unit status and marketing_status update to Reserved,
  - safe cancellation and expiry release.
- Added reservation utilities:
  - get_active_reservation_for_unit,
  - has_active_reservation,
  - release_unit_if_no_active_reservation,
  - expire_overdue_reservations,
  - recalculate_reservation_counts.
- Added daily scheduler hook for overdue reservation expiry when enabled in settings.
- Added Unit Reservation Workflow. Draft cancellation was intentionally not added as a workflow transition because Frappe v15 cannot cancel before submit; draft reservations can be edited or discarded normally.
- Added reports:
  - Unit Reservation Register,
  - Active Unit Reservations,
  - Expiring Unit Reservations,
  - Unit Reservation Impact.
- Updated Sales & Rental, Real Estate Inventory, Executive Control Center, and Reports & Analytics workspace links.
- Added Arabic translations for reservation DocTypes, fields, workflow states/actions, reports, and workspace labels.
- Arabic validation completed on construction.yemenfrappe.com:
  - Created/reused Customer: عميل مهتم بشراء وحدة سكنية.
  - Created active reservation RES-2026-00001 for Unit A-101.
  - A-101 status and marketing_status changed to Reserved.
  - Duplicate reservation for A-101 was blocked.
  - Cancellation validation RES-2026-00003 released P-01 back to Available.
  - Expiry validation RES-2026-00004 released A-G01 back to Available.
  - Project counts became total 5, available 2, reserved 2, sold 0, rented 1, blocked 0.
- Reports loaded successfully, including reservation reports plus selected existing Unit Costing, EVM, Cash Flow, and IPC reports.
- No Sales Contract, Lease Contract, tenant field on Unit, invoice, payment, accounting document, GL backfill, utility-billing install, or El Salvador localization was introduced.

## 2026-05-10 Presentation UX and Executive Dashboard Polish

- Created branch feature/presentation-ux-dashboard-polish from feature/unit-reservation-foundation.
- Audited Frappe v15 presentation capabilities:
  - Workspace, Workspace Link, Workspace Number Card, Number Card, Dashboard Chart, and Workspace Chart exist.
  - Number Cards are safe for deterministic app-backed KPIs.
  - Dashboard Charts are supported, but custom chart sources need finance-approved definitions before client promotion.
- Added Executive Presentation Center workspace as a client-facing presentation route across:
  - Project overview,
  - construction cost control,
  - procurement and site consumption,
  - measurement and IPC,
  - contractor financial control,
  - CFO forecasting,
  - real estate inventory and profitability,
  - reservation,
  - deep financial traceability.
- Added deterministic KPI Number Card methods in construct_erpnext.cfo_analytics.presentation.
- Added idempotent Number Card setup to construct_erpnext.setup.product_readiness.sync_product_workspace_readiness.
- Added curated KPI cards for BOQ total, commitments, certified gross, net payable, retention, contractor outstanding, cash risk, EVM, units, profitability, and reservations.
- Added Arabic translations for presentation workspace sections and KPI labels.
- Updated Arabic client walkthrough with Presentation UX and Dashboard Flow.
- Updated readiness checklist with Presentation UX Readiness.
- Validation completed:
  - Metadata workspace JSON and Arabic CSV parse successfully.
  - python3 compileall passed.
  - Migration, clear-cache, and clear-website-cache completed successfully.
  - Executive Presentation Center installed with 45 links, 10 displayed Number Cards, and no Dashboard Charts.
  - 18 presentation Number Card records exist and returned deterministic values from existing site data.
  - All Executive Presentation Center links resolve to existing DocTypes or Reports.
  - 24 key presentation reports loaded without errors.
  - Existing product workspaces load, no visible GCS workspace label appears in primary navigation, and forbidden Sales/Rental/Portal phase DocTypes were not created.
- No Sales Contract, Lease Contract, Installment Plan, Rent Schedule, CRM Matching, Portal feature, accounting document, submitted-document amendment, or GL backfill was created.

## 2026-05-10 Workspace And Form UX Completion

- Created branch feature/workspace-form-ux-completion from feature/presentation-ux-dashboard-polish.
- Audited product-facing workspaces and reordered/polished JSON grouping for:
  - Executive Presentation Center,
  - Construction Control,
  - Procurement & Site Warehouses,
  - Measurement & IPC,
  - Contractor Management,
  - Real Estate Inventory,
  - Reports & Analytics.
- Kept Sales & Rental as a reservation-ready placeholder; no Sales Contract, Lease Contract, Installment Plan, Rent Schedule, collections, CRM matching, or portal feature was added.
- Reviewed and polished 32 completed custom DocTypes with:
  - business-oriented Section Breaks,
  - concise descriptions/help text for user-facing fields,
  - clearer grouping for calculated fields and status/workflow fields,
  - improved List View fields for important operational records.
- Reviewed report workspace access and kept report logic unchanged because this phase is UX/readiness only.
- Updated Arabic translations for workspace sections, form sections, and key field descriptions.
- Created Arabic UX review document:
  - .ai/FORM_AND_WORKSPACE_UX_REVIEW.md
- Updated Arabic client walkthrough and readiness checklist for the form/workspace UX completion phase.
- Validation completed:
  - JSON metadata and Arabic CSV parse successfully.
  - python3 compileall passed.
  - Migration, clear-cache, and clear-website-cache completed successfully.
  - All 32 reviewed DocTypes load with sections and descriptions.
  - All product workspace links resolve.
  - Key presentation reports load without errors.
  - Key List View queries load without errors.
  - No visible GCS workspace label appears in primary navigation.
  - Sales Contract, Lease Contract, Installment Plan, Rent Schedule, and CRM Matching DocTypes do not exist.
- No fieldnames were changed, no existing fieldtypes were changed, no optional fields were made required, no submitted documents were amended, no accounting documents were created, and no GL backfill was run.

## 2026-05-10 Final Readiness Gate Before Sales Foundation

- Ran final readiness gate on construction.yemenfrappe.com from branch feature/workspace-form-ux-completion.
- Created final gate document:
  - .ai/FINAL_REVIEW_GATE.md
- Validation completed:
  - bench migrate passed.
  - bench clear-cache passed.
  - bench clear-website-cache passed.
  - 9 product workspaces loaded, including Executive Presentation Center and Sales & Rental.
  - Main validation records exist across BOQ, Work Item, procurement, stock, measurement, IPC, contractor ledger, retention, real estate inventory, unit costing, and reservation.
  - 14 key reports loaded without errors.
  - 13 key forms/list views loaded with Section Breaks and field descriptions.
  - Arabic translation CSV parsed successfully with 402 rows and required labels present.
  - Sales & Rental remains reservation-focused and does not expose deferred contract/installment/rent features.
  - No visible GCS workspace label and no visible El Salvador workspace terminology were found.
  - Sales Contract, Lease Contract, Installment Plan, Rent Schedule, and CRM Matching DocTypes remain absent.
- No new business features were implemented, no accounting documents were created, no submitted records were amended, and no GL backfill was run.
- Final decision: safe to start Sales Contract and Installment Plan foundation.

## 2026-05-10 Deep Form Workspace UX Hardening

- Created branch feature/final-form-workspace-ux-hardening from feature/workspace-form-ux-completion after confirming it contains Unit Reservation, presentation UX, form UX, final readiness gate, financial dimensions, unit costing, EVM, cash flow, IPC, and contractor ledger commits.
- Inspected Universal Standard:
  - App exists at /home/frappe/frappe-bench/apps/universal_standard.
  - App is not installed on construction.yemenfrappe.com.
  - Used as read-only reference for Arabic translation file, RTL/font/language-toggle UX pattern, and non-business UI hardening approach.
- Hardened layouts for 32 completed custom DocTypes:
  - Added Tab Breaks to large forms.
  - Added/normalized Section Breaks and Column Breaks.
  - Preserved all business fieldnames, fieldtypes, required flags, and controller logic.
  - Preserved 100 percent English field description coverage.
- Hardened workspace presentation:
  - Executive Presentation Center now follows Executive Overview -> End-to-End Flow -> Construction -> Procurement -> Measurement/IPC -> Contractor -> CFO -> Real Estate -> Profitability -> Reservation -> Financial Traceability.
  - Added deterministic Number Cards to major operational workspaces where reliable app-level methods exist.
  - Sales & Rental remains reservation-only and explicitly leaves contracts, installments, rent schedules, collections, CRM matching, and portal scope deferred.
- Added deterministic KPI helper methods for Work Items Count, Certified Amount, Invoiced Amount, Consumed Amount, Measured Amount, IPC Count, and Advance Balance.
- Expanded construct_erpnext/translations/ar.csv to 1645 rows and hardened Arabic translations for reviewed DocType labels, field labels, descriptions, sections/tabs, workspaces, reports, and Number Cards.
- Created translation and UX gate documents:
  - .ai/TRANSLATION_COVERAGE_AUDIT.md
  - .ai/UX_HARDENING_GATE.md
- Static translation audit results:
  - 32 DocTypes reviewed.
  - 616 user-facing fields reviewed.
  - 100 percent field description coverage.
  - 100 percent Arabic label/description/workspace/report/card coverage for reviewed scope.
- Validation completed:
  - JSON metadata and Arabic CSV parse successfully.
  - python3 compileall passed.
  - bench migrate passed on construction.yemenfrappe.com.
  - clear-cache and clear-website-cache passed.
  - Reviewed forms load with 98 Tab Breaks, 161 Section Breaks, and 78 Column Breaks across reviewed DocTypes.
  - Single settings DocTypes load correctly through get_single.
  - 9 product workspaces load with valid links.
  - 25 deterministic Number Cards exist and returned values.
  - 20 key reports loaded without errors.
  - Sales Contract, Lease Contract, Installment Plan, Rent Schedule, and CRM Matching DocTypes remain absent.
  - No visible GCS workspace label and no visible El Salvador workspace terminology were found.
- No Sales Contract, Lease Contract, Installment Plan, Rent Schedule, CRM Matching, Portal, accounting document, submitted-document amendment, or GL backfill was introduced.

## 2026-05-10 Sales Contract and Installment Plan Foundation

- Created branch feature/sales-contract-installment-foundation from feature/final-form-workspace-ux-hardening.
- Added internal Estate Sales module at construct_erpnext/estate_sales.
- Created DocTypes:
  - Sales Contract Settings: Single DocType for contract_number_prefix, default_contract_validity_days, default_down_payment_percent, allow_duplicate_contract_for_unit, require_customer, require_installment_schedule, installment_amount_tolerance_percent, mark_unit_sold_on_approval, enable_sales_invoice_generation, default_currency_from_company.
  - Sales Installment Schedule: Child DocType for installment rows with sequence, installment_number, label, installment_type (Booking/Down Payment/Contract/Construction Milestone/Handover/Post Handover/Other), due_date, percentage, amount, installment_status (Pending/Due/Partial/Paid/Overdue/Waived/Cancelled), sales_invoice, payment_entry, payment_reference, payment_method, notes.
  - Sales Contract: Submittable DocType with 9 tabs: Contract Information, Unit Details, Buyer Details, Commercial Terms, Installment Plan, Future Accounting References, Status & Control, Remarks. Fields include: contract_number, unit_reservation, real_estate_project, unit, sale_price, discount_percent, discount_amount, net_price, currency, payment_terms_type, installments (Table child), total_installment_amount, outstanding_installment_amount, installment_count, previous_unit_status, previous_marketing_status, cancellation_reason, accounting_dimensions section.
- Implemented sales_contract_utils with service functions: get_sales_contract_settings, generate_contract_number, get_active_sales_contract_for_unit, has_active_sales_contract, fetch_unit_metadata, calculate_contract_amounts, calculate_installment_totals, validate_installment_schedule_totals, generate_default_installments, mark_unit_sold, restore_unit_if_safe, convert_reservation_to_contract, release_unit_from_contract, create_sales_contract_from_reservation.
- Implemented Sales Contract controller with: autoname, before_validate, validate (6 sub-validations), before_submit, on_submit, before_cancel, on_cancel, whitelisted create_sales_contract_from_reservation.
- Sales Contract settings defaults: mark_unit_sold_on_approval enabled, enable_sales_invoice_generation disabled, allow_duplicate_contract_for_unit disabled, require_customer enabled, require_installment_schedule enabled, installment_amount_tolerance_percent 5.
- Added Sales Contract Approval Workflow through idempotent after_migrate setup: states Draft, Under Review, Approved, Active, Cancelled, Closed with docstatus-aware transitions.
- Added 5 Script Reports: Sales Contract Register, Sales Value Summary, Unit Sales Pipeline, Active Sales Contracts, Sold Units.
- Updated workspaces:
  - Sales & Rental: Added Sales Contract section, Sales Reports card, Active Sales Contracts number card.
  - Real Estate Inventory: Added Sales card with Unit Sales Pipeline, Sales Value Summary, Reserved to Sold Conversion Report.
  - Executive Control Center: Added Sales Visibility section, Active Sales Contracts and Sold Units number cards.
  - Executive Presentation Center: Added Sales Contract section, Active Sales Contracts and Sold Units number cards.
  - Reports & Analytics: Added Sales card with all 5 sales reports.
- Extended ar.csv to 1790 rows with ~145 new translation rows for DocTypes, fields, sections, tabs, workflow states, installment statuses, reports, and validation messages.
- Updated DECISIONS.md with ADR-024 through ADR-027: Sales Contract as Primary Operational Sales Transaction, Sales Installment Schedule as Child Table, Unit Becomes Sold on Approval, No Accounting Documents Until Invoice Design.
- Arabic validation scenario completed on construction.yemenfrappe.com:
  - Created Sales Contract from reservation RES-2026-00001.
  - Generated 5 installments: Booking 20%, Down Payment 30%, Construction Milestone 25%, Handover 20%, Post Handover 5%.
  - Total installment amount matched net_price.
  - Submitted Sales Contract; Unit A-101 status and marketing_status changed to Sold.
  - Reservation RES-2026-00001 status changed to Converted.
  - Duplicate contract for same unit was blocked by settings.
  - Installment schedule total mismatch validation triggered when totals did not match net_price.
  - All 5 sales reports loaded without errors.
- No Sales Invoice, Payment Entry, Lease Contract, Rent Schedule, Commission, CRM Matching, Portal, WhatsApp/Meta Integration, accounting documents, or ERPNext core modifications were introduced.

## 2026-05-10 Sales Contract Recovery and Completion

- Recovered the Sales Contract + Installment Plan foundation after a previous workflow attempt stopped.
- Confirmed raw SQL workflow creation was not continued.
- Sales Contract Approval Workflow is now created idempotently through Frappe ORM in `construct_erpnext.estate_sales.setup.after_migrate`.
- Added `Estate Sales` to `construct_erpnext/modules.txt` so Frappe does not treat Sales Contract DocTypes as orphaned during migration.
- Added missing controller modules for Sales Contract Settings and Sales Installment Schedule.
- Corrected Sales Installment Schedule metadata to `istable=1` and added an idempotent child-table schema guard for legacy partial metadata attempts.
- Corrected Sales Contract workflow update behavior by allowing workflow/status fields to update after submission and syncing `contract_status` from `workflow_state`.
- Corrected report filter SQL fragments so filters append with `AND` safely.
- Final sales reports validated: Sales Contract Register, Installment Schedule Report, Unit Sales Pipeline, Sales Value Summary, Reserved to Sold Conversion Report.
- Arabic validation scenario completed:
  - Sales Contract SC-2026-00001 created from reservation RES-2026-00001.
  - Four Arabic installments were validated: دفعة مقدمة، الدفعة الثانية، دفعة الاستلام، الدفعة النهائية.
  - Net price and total installments both equal 1,200,000.
  - Workflow reached Active.
  - Unit A-101 status and marketing_status are Sold.
  - Reservation RES-2026-00001 is Converted and linked to SC-2026-00001.
  - Duplicate Sales Contract for the same Unit is blocked.
  - Installment mismatch validation is blocked.
- Validation passed:
  - bench migrate, clear-cache, and clear-website-cache completed.
  - Sales Contract Settings, Sales Contract, and Sales Installment Schedule exist.
  - Sales Contract Approval Workflow exists with 6 states and 9 transitions.
  - All 5 sales reports load.
  - Key existing BOQ/procurement/measurement/IPC/contractor/CFO/unit reservation reports still exist.
  - Arabic translation CSV parses with 1792 rows.
  - No Sales Invoice, Payment Entry, Journal Entry, Lease Contract, Rent Schedule, Installment Plan, CRM Matching, Portal, or ERPNext core modification was introduced.

## 2026-05-10 Sales Contract Readiness Review

- Created branch feature/sales-contract-readiness-review from feature/sales-contract-installment-foundation.
- Review-only validation completed without creating Sales Invoice, Payment Entry, Journal Entry, Lease Contract, Rent Schedule, Commission, CRM Matching, Portal, or accounting documents.
- Confirmed Sales Contract Settings, Sales Contract, and Sales Installment Schedule exist.
- Confirmed Sales Contract Approval Workflow exists, is active, and has 6 states and 9 transitions.
- Confirmed Sales Contract SC-2026-00001 is Active, docstatus 1, linked to Unit A-101 and Reservation RES-2026-00001.
- Confirmed Unit A-101 status and marketing_status are Sold.
- Confirmed Reservation RES-2026-00001 status and workflow_state are Converted and linked to SC-2026-00001.
- Confirmed installment schedule has 4 rows and totals 1,200,000, matching net_price.
- Confirmed duplicate sales contract creation for the converted reservation/unit is blocked.
- Confirmed installment total mismatch validation blocks a draft contract when installment total differs from net_price beyond tolerance.
- Confirmed no Sales Invoice, Payment Entry, or GL Entry exists for SC-2026-00001.
- Confirmed Unit Accounting Dimension exists and unit fields are available on Sales Invoice Item and GL Entry for the next phase.
- Confirmed required sales reports and key existing unit/CFO/traceability reports load.
- Confirmed Sales & Rental, Executive Presentation Center, Executive Control Center, Real Estate Inventory, and Reports & Analytics workspaces load.
- Confirmed ar.csv parses successfully; noted minor missing Arabic translations for two generic Sales Contract layout labels to carry into UX cleanup.
- Added .ai/SALES_CONTRACT_READINESS_REVIEW.md.

## 2026-05-10 Sales Invoice and Collections Foundation

- Created branch feature/sales-invoice-collections-foundation from feature/sales-contract-readiness-review.
- Added Sales Invoice Collection Settings as a Single DocType controlling invoice generation, grouped installment invoices, Unit dimension requirements, partial collections, overdue grace days, duplicate invoice blocking, and company-currency defaults.
- Extended Sales Installment Schedule with invoice_status, invoice_amount, paid_amount, outstanding_amount, invoiced_on, paid_on, and overdue_days while preserving existing sales_invoice and payment_entry links.
- Extended Sales Contract with total_invoiced_amount, total_collected_amount, total_outstanding_amount, collection_status, first_sales_invoice, and latest_payment_entry.
- Added sales_invoice_utils service:
  - Creates draft ERPNext Sales Invoice from one or more Sales Contract installment rows.
  - Uses a non-stock service item `خدمة بيع وحدة عقارية`.
  - Uses a selling price list `قائمة أسعار بيع الوحدات العقارية` in company currency when no selling price list is configured.
  - Copies Unit, Project, Cost Center, Sales Contract, Sales Installment reference, Real Estate Project, and Unit Reservation to Sales Invoice Item where fields exist.
  - Blocks duplicate active invoices for the same installment.
  - Releases installment rows safely when a linked Sales Invoice is cancelled.
- Added collections_utils service:
  - Recalculates Sales Contract and installment collection status from Sales Invoice and Payment Entry references.
  - Provides an overdue installment marker and collection/unit revenue summaries.
- Added safe doc_events:
  - Sales Invoice validate/on_submit/on_cancel for dimension sync and installment status updates.
  - Payment Entry on_submit/on_cancel for collection status recalculation from invoice references.
  - Daily scheduler for overdue installment marking.
- Added Sales Contract client buttons for Create Sales Invoice and Refresh Collection Status.
- Added reports:
  - Sales Invoice from Installments Report
  - Sales Collection Report
  - Overdue Sales Installments
  - Unit Revenue Report
  - Sales Contract Collection Summary
- Added deterministic KPI Number Cards:
  - Total Invoiced Sales
  - Total Collected Sales
  - Outstanding Sales Amount
  - Overdue Installments Count
  - Overdue Installments Amount
- Updated Sales & Rental, Executive Control Center, Executive Presentation Center, and Reports & Analytics workspaces with collection links and cards.
- Extended ar.csv to 1847 rows with Sales Invoice and Collections labels, reports, statuses, buttons, and KPI translations.
- Arabic validation scenario completed:
  - Generated draft Sales Invoice ACC-SINV-2026-00001 from the first installment of SC-2026-00001.
  - Sales Invoice Item carries unit A-101, project PROJ-0001, cost center Main - YCRE, sales contract SC-2026-00001, installment reference erdmjjidfa, real estate project REP-2026-00001, and reservation RES-2026-00001.
  - Sales Contract totals updated: invoiced 300,000, collected 0, outstanding 300,000, status Partially Invoiced.
  - Duplicate invoice creation for the same installment is blocked.
  - Sales Invoice remains Draft because auto_submit_sales_invoice is disabled by default.
  - No GL Entry, Payment Entry, Journal Entry, Lease Contract, Rent Schedule, Commission, CRM Matching, Portal, or GL backfill was created.
- Validation passed:
  - bench migrate, clear-cache, and clear-website-cache completed.
  - New reports and key existing Unit/CFO/traceability reports load.
  - Sales collection KPI methods resolve.
  - Target workspaces exist and load.
  - ar.csv parses successfully.

## 2026-05-10 CMD-24 Sales Invoice and Collections Readiness Review

- Created branch feature/sales-invoice-collections-readiness-review from feature/sales-invoice-collections-foundation.
- Started review-only validation for Sales Invoice and Collections before Lease Contract and Rent Schedule foundation.
- Confirmed static/code readiness:
  - Python modules under estate_sales, cfo_analytics, and setup compile successfully.
  - Sales Invoice Collection Settings metadata exists.
  - Sales Contract and Sales Installment Schedule metadata include CMD-23 collection fields.
  - ar.csv parses successfully with 1847 rows.
  - Sales invoice/collection report links, workspace links, and KPI labels are present in JSON/translation files.
- Live site validation was blocked because MariaDB on construction.yemenfrappe.com refused connections.
- `systemctl status mariadb` showed `mariadb.service` failed with `Result: oom-kill`.
- Attempted service start was blocked by interactive sudo requirement in the current shell.
- No Sales Invoice, Payment Entry, Journal Entry, Lease Contract, Rent Schedule, Commission, CRM Matching, Portal, GL backfill, or submitted accounting amendment was created during this review.
- Added .ai/SALES_INVOICE_COLLECTIONS_READINESS_REVIEW.md with the blocked readiness decision.
- NEXT_ACTION set to restore MariaDB service and rerun the Sales Invoice and Collections readiness validation before Lease Contract foundation.

## 2026-05-10 CMD-24A Restore MariaDB and Rerun Sales Invoice Collections Readiness Validation

- Diagnosed server memory and MariaDB state after CMD-24 was blocked.
- Current memory snapshot: 11GiB RAM, 7.2GiB used, 3.8GiB free, 4.2GiB available; swap 4GiB with 1.7GiB used.
- Disk space is not the blocker: root filesystem is about 56% used.
- Highest memory users included code-server extension hosts, MariaDB, and several development assistant processes.
- MariaDB was running again at validation time: `mariadb.service` active since 2026-05-10 20:47:40 CEST.
- Prior OOM remains confirmed from service status; journal/dmesg details were limited by OS permissions.
- `sudo -n systemctl start mariadb` still fails because sudo requires a password; future service restarts require the server owner to run `sudo systemctl start mariadb`.
- DB connection validated:
  - `bench --site construction.yemenfrappe.com mariadb -e "select 1"` passed.
  - `bench --site construction.yemenfrappe.com list-apps` passed.
- Live Sales Invoice/Collections readiness validation passed:
  - Sales Invoice Collection Settings exists and auto-submit is disabled.
  - Sales Contract SC-2026-00001 is Active.
  - Draft Sales Invoice ACC-SINV-2026-00001 exists with docstatus 0.
  - Invoice item carries unit A-101, project PROJ-0001, cost center Main - YCRE, sales_contract SC-2026-00001, installment reference erdmjjidfa, real estate project REP-2026-00001, and reservation RES-2026-00001.
  - First installment is linked to ACC-SINV-2026-00001.
  - Contract totals remain: invoiced 300,000; collected 0; outstanding 300,000; status Partially Invoiced.
  - Unit dimension exists on Sales Invoice Item and GL Entry.
  - No GL Entry, Payment Entry, or Journal Entry exists for the draft invoice.
- Reports validated: all Sales Invoice/Collections reports plus key Sales Contract, Unit, GL, CFO, Cash Flow, and EVM reports loaded.
- Workspaces and sales collection KPI cards validated.
- Deferred scope confirmed: no Lease Contract, Rent Schedule, Commission, CRM Matching, Portal, new Sales Invoice, Sales Invoice submission, Payment Entry, Journal Entry, GL backfill, or submitted accounting amendment.
- Updated SALES_INVOICE_COLLECTIONS_READINESS_REVIEW.md with final passed CMD-24A decision.
- NEXT_ACTION set to Start Lease Contract and Rent Schedule foundation.
