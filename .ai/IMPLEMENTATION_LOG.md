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
