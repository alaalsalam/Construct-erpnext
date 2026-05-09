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
