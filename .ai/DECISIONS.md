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

## ADR-003: Canonical App Repository Path

- Canonical app repository path normalized to /home/frappe/frappe-bench/apps/construct_erpnext to avoid confusion between app package name and repository folder.
- Old path /home/frappe/frappe-bench/apps/Construct-erpnext was removed by renaming the real repository folder.
- Do not use /home/frappe/frappe-bench/apps/Construct-erpnext as a working root anymore.
- Keep the internal Python package folder /home/frappe/frappe-bench/apps/construct_erpnext/construct_erpnext.

## ADR-004: Disable Automatic Country Localization

- Make the product generic by default.
- Keep legacy El Salvador setup helpers in setup/legacy_el_salvador.py for reference and compatibility.
- Do not execute El Salvador tax setup, payroll setup, or sv_* custom-field creation during after_install.
- Do not run El Salvador withholding logic from Purchase Invoice validate.
- Implement taxes, payroll, and fiscal localization separately per deployment.

## ADR-005: BOQ Rows Become Operational Work Items

- BOQ items are edited inside Construction BOQ as child rows.
- Approved Construction BOQs generate standalone Construction Work Items.
- Construction Work Item is the future operational link point for procurement, site warehouses, progress, Measurement Book, IPC, actual costing, and forecasting.
- Construction BOQ Workflow is created through an after_migrate setup hook for Frappe v15 compatibility.

## ADR-006: Construction Work Item Links BOQ To Procurement

- Construction Work Item is the operational link between BOQ and ERPNext procurement/stock transactions.
- Procurement child rows store references to Construction Work Item, Construction BOQ, WBS Element, Cost Code, and Site Warehouse through app-managed Custom Fields.
- Procurement totals are recalculated from submitted ERPNext documents and exclude draft/cancelled documents.
- Committed, invoiced, and consumed amounts are tracked separately from the existing actual_cost field to avoid accidental double counting.
- Procurement budget blocking is disabled by default and controlled through Procurement Control Settings.

## ADR-007: Operational Baseline Records

- Operational baseline records are allowed on construction.yemenfrappe.com only when they are realistic, reusable, and documented.
- The Al Nakheel baseline is kept for continued implementation validation instead of being removed.
- Baseline records must not use disposable naming and must remain suitable for future BOQ, procurement, stock, and Measurement Book validation.

## ADR-008: Arabic Operational Baseline, English Technical Model

- Technical DocType names, Python modules, and internal APIs remain English for Frappe maintainability.
- Operational records, titles, descriptions, item names, warehouse names, cost centers, project names, BOQ labels, and explanatory data should use clear Arabic names.
- Operational baseline records must remain non-country-specific unless a deployment-specific localization plan is approved.
- Submitted or linked ERPNext records are not force-renamed when doing so could disturb accounting, stock, or workflow history; visible Arabic fields are updated instead.

## ADR-009: Measurement Entry Feeds Future IPC

- Measurement Entry is a standalone operational record linked to Measurement Book and Construction Work Item.
- Verified/Locked Measurement Entries update Work Item measurement progress.
- Measurement Book does not certify payment quantities and does not update certified_qty.
- Future IPC generation must be based on verified Measurement Entries rather than manual IPC line entry.

## ADR-010: IPC From Verified Measurement Entries

- Interim Payment Certificates are generated from Verified or Locked Measurement Entries through a verified Measurement Book.
- IPC updates Construction Work Item certified_qty and certification progress separately from measured_qty and measurement progress.
- A Measurement Entry linked to a submitted/non-cancelled IPC cannot be reused in another IPC.
- Existing Subcontract is sufficient as the optional contractor contract reference for this phase because it contains project, contractor, company, contract title, status, amount, activities, and dates.
- Do not create Contractor Contract or Contractor Ledger until a separate contractor accounting phase is approved.
- Purchase Invoice generation from IPC creates a draft ERPNext Purchase Invoice and does not submit it automatically.

## ADR-011: Contractor Ledger As Operational Subledger

- Contractor Ledger is an operational subledger that references ERPNext Purchase Invoice and Payment Entry but does not replace GL accounting.
- ERPNext Purchase Invoice and Payment Entry remain the accounting source of truth for payables and payments.
- Contractor Ledger Entry records contractor control events for certified amount, retention, advance recovery, purchase invoice creation, payment allocation, and payment difference.
- Retention Register, Advance Register, and Guarantee Register are control registers only; they do not create Journal Entries automatically.
- Existing IPC records can be synchronized through an explicit app-level helper rather than destructive resubmission.

## ADR-012: Project Financial Snapshot As CFO Aggregation Layer

- Project Financial Snapshot is the first CFO aggregation layer and does not replace ERPNext accounting reports or GL.
- The snapshot is point-in-time and deterministic; it reads from Construction Work Item, Interim Payment Certificate, Contractor Account, and Retention Register.
- The snapshot does not submit accounting records, create Journal Entries, run Cash Flow Forecast automation, or create scheduled EVM calculations.
- Risk statuses are intentionally simple and explainable until a separate forecasting and executive analytics phase is approved.
