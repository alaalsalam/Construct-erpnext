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
