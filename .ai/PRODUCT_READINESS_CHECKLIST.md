# Product Readiness Checklist

## 2026-05-10

## 1. Technical Readiness

- Passed: No ERPNext core files modified.
- Passed: construct_erpnext package name remains unchanged.
- Passed: No utility-billing installation.
- Passed: No Reservation, Sales Contract, Lease Contract, CRM Matching, or Portal features created.
- Passed: No accounting documents created.
- Passed: No GL backfill run.
- Passed: No submitted documents amended.
- Passed: No Server Scripts introduced.
- Passed: Product readiness workspace sync is app-level and idempotent.

## 2. Data Readiness

- Passed: Arabic operational baseline records remain readable and reusable.
- Passed: BOQ, Work Item, procurement, stock, measurement, IPC, contractor, CFO, EVM, inventory, unit costing, and financial dimension validation records remain intact.
- Deferred: Purchase Invoice ACC-PINV-2026-00002 remains Draft until normal Invoice Authorization is completed.
- Deferred: Unit dimension GL validation waits for legitimate unit-specific accounting transactions.

## 3. Bilingual UX Readiness

- Passed: English remains the source language for DocType labels, report names, workspace names, and technical metadata.
- Passed: Arabic translation file created at construct_erpnext/translations/ar.csv.
- Passed: Arabic translations cover core DocTypes, workspaces, reports, workflow states, common report columns, and key descriptions.
- Passed: Translation CSV validates as parseable CSV.
- Deferred: Full browser-level Arabic UI review should be done with an Arabic-language user session before client delivery.

## 4. Workspace Readiness

- Passed: Product-facing workspaces are grouped by process flow:
  - Executive Control Center.
  - Construction Control.
  - Procurement & Site Warehouses.
  - Measurement & IPC.
  - Contractor Management.
  - Real Estate Inventory.
  - Sales & Rental.
  - Reports & Analytics.
- Passed: Sales & Rental remains a placeholder with a clear future-phase note.
- Passed: No GCS workspace is promoted as primary product navigation.
- Passed: Workspace ordering is synchronized through a readiness after_migrate helper.

## 5. Reports Readiness

- Passed: Custom Script Report column labels use Frappe translation wrappers.
- Passed: Reports are grouped in Reports & Analytics by Construction, Procurement, Measurement & IPC, Contractor, CFO, Real Estate Inventory, Unit Profitability, and Financial Dimensions.
- Passed: Existing traceability validation confirmed critical reports load and degrade gracefully for historical GL rows with blank new dimensions.

## 6. Dashboard Readiness

- Passed: Executive Control Center links the core CFO reports needed for client presentation:
  - Project Financial Snapshot Report.
  - Project Cash Flow Forecast Report.
  - Project EVM Metrics Report.
  - Contractor Exposure Summary.
  - Unit Profitability Report.
  - Project Performance Dashboard Report.
- Deferred: Number Cards and Dashboard Charts were not created in this phase because reliable production metrics should be signed off with finance leadership before being promoted as cards.

## 7. Traceability Readiness

- Passed: .ai/TRACEABILITY_VALIDATION.md confirms BOQ -> Work Item -> Procurement / Stock / Measurement -> IPC -> Contractor Ledger -> Unit Costing -> Accounting Dimensions / Reports.
- Passed: Historical GL limitations are documented.
- Passed: No broad GL backfill decision is documented.

## 8. Client Presentation Readiness

- Passed: Arabic walkthrough created at .ai/CLIENT_PRESENTATION_WALKTHROUGH.md.
- Passed: Walkthrough includes presentation storyline, screens to open, what each screen proves, ready scope, deferred scope, honest positioning, and known limits.

## 9. Known Limitations

- Historical submitted GL rows before Accounting Dimensions do not have new dimension values.
- Unit dimension in GL needs future unit-specific transactions from Sales/Rental or approved unit-specific costing.
- IPC Purchase Invoice submission and payment validation depend on normal Invoice Authorization.
- CFO/EVM risk thresholds are deterministic readiness rules and should be reviewed with finance leadership before final KPI sign-off.
- Full Arabic browser review should be done in the client user context before presentation.

## 10. Decision

Safe to proceed to Unit Reservation foundation after this readiness pass.
