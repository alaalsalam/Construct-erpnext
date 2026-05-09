# Decisions

## ADR-001: Base Product And Initial Technical Direction

- Build on alaalsalam/Construct-erpnext as base product.
- Keep construct_erpnext package name for now.
- Develop modules inside the same app.
- Do not install utility-billing as dependency now.
- Remove/neutralize El Salvador localization.
- Do not modify ERPNext core.

## ADR-002: ERPNext v15 Deployment Target

- Current deployment target is ERPNext v15 because construction.yemenfrappe.com is running:
  - Frappe 15.107.2
  - ERPNext 15.107.0
  - HRMS 15.58.2
- Do not upgrade to v16 now.
- All development must remain compatible with ERPNext v15 unless a separate migration plan is approved.

## ADR-003: Disable Automatic Country Localization

- Make the product generic by default.
- Keep legacy El Salvador setup helpers in setup/legacy_el_salvador.py for reference and compatibility.
- Do not execute El Salvador tax setup, payroll setup, or sv_* custom-field creation during after_install.
- Do not run El Salvador withholding logic from Purchase Invoice validate.
- Implement taxes, payroll, and fiscal localization separately per deployment.
