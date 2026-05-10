# Product Readiness Checklist

## 2026-05-10

## 1. Technical Readiness

- Passed: No ERPNext core files modified.
- Passed: construct_erpnext package name remains unchanged.
- Passed: No utility-billing installation.
- Passed: Unit Reservation foundation is implemented as the first commercial operation.
- Passed: No Sales Contract, Lease Contract, CRM Matching, or Portal features created.
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
- Passed: Executive Presentation Center adds deterministic KPI Number Cards for the client-facing overview.
- Deferred: Dashboard Charts are not created yet because chart definitions and threshold wording still need finance leadership sign-off.

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
- Unit Reservation does not create accounting documents; reservation amount remains commercial tracking only.
- Draft reservations are not cancelled through Workflow because Frappe v15 cannot cancel before submit.
- Active validation reservation RES-2026-00001 keeps A-101 reserved for walkthrough.

## 10. Unit Reservation Readiness

- Passed: Unit Reservation Settings ready.
- Passed: Unit Reservation DocType ready.
- Passed: Unit Reservation Workflow ready for Draft -> Reserved and submitted cancellation/expiry/conversion states.
- Passed: Reservation controller updates Unit status and marketing_status.
- Passed: Duplicate active reservation is blocked by default.
- Passed: Cancellation and expiry release the Unit safely.
- Passed: Reservation reports ready.
- Passed: Workspace links ready.
- Passed: Arabic translations added.
- Passed: No accounting side effects.
- Deferred: Sales Contract conversion target remains a future phase.
- Deferred: Lease Contract conversion target remains a future phase.

## 11. Decision

Safe to review Unit Reservation with stakeholders before Sales Contract foundation.

## 12. Presentation UX Readiness

- Passed: Executive Presentation Center workspace added for client presentation.
- Passed: CFO reports grouped in a single presentation path.
- Passed: Construction flow grouped from BOQ to Work Item and variance reports.
- Passed: Procurement and site consumption reports grouped.
- Passed: Measurement, IPC, and traceability reports grouped.
- Passed: Contractor financial control reports grouped.
- Passed: Real estate inventory, unit costing, profitability, and reservation links grouped.
- Passed: Deep financial traceability reports grouped.
- Passed: Arabic translations updated for presentation workspace sections and KPI labels.
- Passed: Number Cards created with deterministic app-level methods.
- Deferred: Dashboard Charts are deferred until finance leadership approves chart definitions and threshold wording.
- Passed: Client walkthrough updated with Presentation UX and Dashboard Flow.
- Passed: No new business features added.
- Passed: No accounting documents created.
- Passed: No submitted documents amended.
- Passed: No GL backfill performed.

## 13. Presentation Decision

Safe for a professional client presentation after a final browser click-through of Executive Presentation Center and core linked reports.

## 14. Form and Workspace UX Completion

- Passed: Workspaces ordered by process.
- Passed: Executive Presentation Center follows the full presentation storyline.
- Passed: Construction, Procurement, Measurement, Contractor, Real Estate, Reservation, and Reports workspaces are grouped by operating flow.
- Passed: Key DocTypes have business-oriented sections.
- Passed: Key user-facing fields have concise descriptions.
- Passed: Calculated fields are grouped clearly in totals, risk, profitability, or status sections.
- Passed: Status and workflow fields remain visible.
- Passed: Important List View columns were improved without adding heavy calculated fields.
- Passed: Reports remain accessible from the relevant workspaces.
- Passed: Arabic translations updated for new section labels and important descriptions.
- Passed: No new business features introduced.
- Passed: No accounting documents created.
- Passed: No submitted documents amended.
- Passed: No GL backfill performed.

## 15. UX Completion Decision

Safe to proceed to a final review of completed phases before Sales Contract and Installment Plan foundation.

## 16. Final Readiness Gate

- Passed: bench migrate completed successfully.
- Passed: clear-cache and clear-website-cache completed successfully.
- Passed: Product workspaces load.
- Passed: Main completed business flows have validation records.
- Passed: Key presentation reports load.
- Passed: Key forms have sections and descriptions.
- Passed: List views load.
- Passed: Arabic translation CSV parses and required labels are present.
- Passed: Sales & Rental remains placeholder/reservation-focused.
- Passed: No Sales Contract, Lease Contract, Installment Plan, Rent Schedule, or CRM Matching DocType exists.
- Passed: No accounting documents created during the gate.
- Passed: No submitted records amended.
- Passed: No GL backfill performed.
- Passed: No visible GCS workspace or El Salvador workspace terminology.

## 17. Final Gate Decision

Safe to start Sales Contract and Installment Plan foundation.

## 18. Deep UX Hardening Gate

- Passed: Universal Standard inspected and used as read-only UX/translation reference.
- Passed: universal_standard is not installed on the site; no dependency was introduced.
- Passed: 32 completed custom DocTypes reviewed again.
- Passed: Large forms now use Tab Breaks where useful.
- Passed: Sections and columns were strengthened to reduce long stacked forms.
- Passed: Field description coverage is 100 percent for reviewed custom fields.
- Passed: Arabic label coverage is 100 percent for reviewed DocTypes, fields, sections, workspaces, reports, and cards.
- Passed: Arabic description coverage is 100 percent for reviewed custom field descriptions.
- Passed: Major workspaces have process cards and deterministic Number Cards where reliable.
- Passed: Sales & Rental remains reservation-only.
- Passed: Dashboard Charts are explicitly deferred.
- Passed: No Sales Contract, Lease Contract, Installment Plan, Rent Schedule, CRM Matching, Portal, accounting document, submitted amendment, or GL backfill introduced.

## 19. Deep UX Decision

Previous completed phases are now ready for a professional client presentation from the form/workspace/translation perspective, subject to one final browser click-through in the client user context.

## 20. Sales Contract and Installment Plan Readiness

- Passed: Sales Contract Settings ready.
- Passed: Sales Contract DocType ready with 9 tabs and all required fields.
- Passed: Sales Installment Schedule Child DocType ready.
- Passed: Sales Contract controller implements all 6 sub-validations, submit/cancel hooks, and whitelisted creation method.
- Passed: Sales Contract Approval Workflow created through after_migrate setup.
- Passed: Contract number, unit metadata, party, discount, installment schedule, and tolerance validations are working.
- Passed: Unit becomes Sold on Sales Contract submission (when settings allow).
- Passed: Reservation converts to Converted status on Sales Contract submission.
- Passed: Active duplicate contract blocking works.
- Passed: 5 sales reports load without errors.
- Passed: Workspaces updated with Sales Contract section, reports, and number cards.
- Passed: Arabic translations extended to 1790 rows covering new DocTypes, fields, sections, tabs, workflow, installment types/statuses, and reports.
- Passed: No Sales Invoice, Payment Entry, Lease Contract, Rent Schedule, Commission, CRM Matching, Portal, accounting documents, or ERPNext core modifications introduced.
- Passed: Sales Invoice generation explicitly disabled in settings.

## 21. Sales Contract Decision

Safe to review Sales Contract readiness before Sales Invoice and Collections foundation.

## 22. Sales Contract Recovery Gate

- Passed: Raw SQL workflow creation was stopped.
- Passed: Workflow creation uses Frappe ORM and idempotent after_migrate setup.
- Passed: Sales Installment Schedule is a valid child table with parent linkage columns.
- Passed: Sales Contract SC-2026-00001 reached Active through workflow.
- Passed: Unit A-101 became Sold.
- Passed: Reservation RES-2026-00001 became Converted.
- Passed: Four-installment Arabic validation schedule totals match net price.
- Passed: Duplicate contract validation is blocked.
- Passed: Installment mismatch validation is blocked.
- Passed: All five required sales reports load.
- Passed: No Sales Invoice, Payment Entry, Journal Entry, Lease Contract, Rent Schedule, Portal, or CRM Matching feature was created.

## 23. Sales Contract Readiness Review

- Passed: Sales Contract Settings, Sales Contract, and Sales Installment Schedule exist.
- Passed: Sales Contract Approval Workflow exists and loads.
- Passed: SC-2026-00001 is Active and submitted.
- Passed: A-101 is Sold.
- Passed: RES-2026-00001 is Converted and linked to SC-2026-00001.
- Passed: Four installments total 1,200,000 and match net price.
- Passed: Duplicate contract validation is blocked.
- Passed: Draft installment mismatch validation is blocked.
- Passed: No Sales Invoice, Payment Entry, Journal Entry, or GL Entry was created by the contract.
- Passed: Unit Accounting Dimension is ready for future Sales Invoice Item and GL traceability.
- Passed: Sales reports and key existing reports load.
- Passed: Sales and executive workspaces load.
- Passed: ar.csv parses successfully.
- Deferred: Minor Arabic translations for generic Sales Contract layout labels should be cleaned up in the next UX pass.

## 24. Sales Contract Readiness Decision

Safe to start Sales Invoice and Collections foundation.

## 25. Sales Invoice and Collections Foundation

- Passed: Sales Invoice Collection Settings exists and default generation controls are enabled while auto-submit remains disabled.
- Passed: Sales Installment Schedule tracks invoice status, invoice amount, paid amount, outstanding amount, invoice date, payment date, and overdue days.
- Passed: Sales Contract tracks total invoiced, collected, outstanding, and collection status.
- Passed: Draft Sales Invoice generation from Sales Contract installments works.
- Passed: Sales Invoice Item carries Unit dimension and operational references for SC-2026-00001.
- Passed: Duplicate active invoice generation for the same installment is blocked.
- Passed: Payment Entry integration is hook-based and does not override ERPNext accounting.
- Passed: Sales collection reports load without errors.
- Passed: Sales collection KPI Number Cards resolve deterministic values.
- Passed: Workspaces include sales collection reports and cards.
- Passed: Arabic translations extended and ar.csv parses.
- Passed: No Sales Invoice submission, Payment Entry, Journal Entry, Lease Contract, Rent Schedule, Commission, CRM Matching, Portal, or GL backfill was created.
- Deferred: GL Unit revenue validation requires submitting a Sales Invoice through normal ERPNext controls.
- Deferred: Payment Entry collection validation requires a submitted Sales Invoice.

## 26. Sales Invoice and Collections Decision

Safe to review Sales Invoice and Collections readiness before Lease Contract foundation.

## 27. CMD-24 Sales Invoice and Collections Readiness Review

- Passed: Static code compile for Sales Invoice and Collections modules.
- Passed: Sales Invoice Collection Settings metadata exists.
- Passed: Sales Contract and Sales Installment Schedule metadata include collection fields.
- Passed: ar.csv parses successfully with Sales Invoice and Collections translations.
- Passed: Workspace/report/KPI links are present in JSON and translation files.
- Blocked: Live site validation could not run because MariaDB is down with `Result: oom-kill`.
- Blocked: Draft Sales Invoice ACC-SINV-2026-00001 could not be revalidated live.
- Blocked: Report loading, workspace loading, and Number Card loading could not be revalidated live.
- Deferred: Sales Invoice remains Draft.
- Deferred: GL Entry validation requires normal Sales Invoice submission.
- Deferred: Payment Entry validation requires a submitted Sales Invoice.

## 28. CMD-24 Decision

Not safe to proceed to Lease Contract until MariaDB is restored and Sales Invoice and Collections readiness validation passes live on construction.yemenfrappe.com.

## 29. Lease Contract and Rent Schedule Foundation

- Passed: Lease Contract Settings exists.
- Passed: Lease Contract DocType exists and is submittable.
- Passed: Rent Schedule child table exists.
- Passed: Lease Contract Approval Workflow exists and loads.
- Passed: Rent reservation RES-2026-00005 converted into Lease Contract LC-2026-00001.
- Passed: Unit A-G01 changed to Rented only after lease approval/activation.
- Passed: Reservation RES-2026-00005 changed to Converted.
- Passed: Rent Schedule generated 12 monthly rows totaling 4,200,000.
- Passed: Duplicate active Lease Contract for the same Unit is blocked.
- Passed: Lease reports load without errors.
- Passed: Workspace links and lease KPI Number Cards exist.
- Passed: Arabic translations were extended for lease fields, reports, workflow states, and actions.
- Passed: No Rent Invoice, Sales Invoice, Payment Entry, Journal Entry, Commission, CRM Matching, Portal, or GL backfill was created.
- Deferred: Rent Invoice and rental collections are the next finance phase.

## 30. Lease Foundation Decision

Safe to review Lease Contract readiness before Rent Invoice and Collections foundation.

## 31. Lease Contract Readiness Review

- Passed: Lease Contract Settings, Lease Contract, and Rent Schedule exist.
- Passed: Lease Contract Approval Workflow exists and loads.
- Passed: LC-2026-00001 is Active and submitted.
- Passed: A-G01 is Rented.
- Passed: RES-2026-00005 is Converted and linked to LC-2026-00001.
- Passed: Rent Schedule has 12 monthly rows totaling 4,200,000.
- Passed: Total scheduled rent matches total contract rent.
- Passed: Duplicate active lease validation is blocked.
- Passed: Unit Accounting Dimension is ready for future rent invoice item and GL traceability.
- Passed: Lease reports and key existing Sales, Unit, GL, CFO, Cash Flow, and EVM reports load.
- Passed: Sales & Rental, Executive Presentation Center, Executive Control Center, Real Estate Inventory, and Reports & Analytics workspaces load with lease/rental links.
- Passed: ar.csv parses successfully with lease translations present.
- Passed: No Rent Invoice, Sales Invoice, Payment Entry, Journal Entry, Commission, CRM Matching, Portal, GL Entry, or GL backfill was created from the lease.
- Deferred: Rent Invoice, rental collections, rental receivables aging, and GL validation are the next phase.

## 32. Lease Readiness Decision

Safe to start Rent Invoice and Collections foundation.

## 33. Phase 1 Client Presentation Closure

- Passed: Phase 1 scope validated from Construction BOQ to draft Sales Invoice.
- Passed: Key forms open for construction, procurement, measurement, IPC, contractor, CFO, inventory, unit costing, reservation, sales contract, and draft sales invoice.
- Passed: 32 key reports loaded across Phase 1 scope.
- Passed: Product workspaces load.
- Passed: Executive Presentation Center loads.
- Passed: KPI cards for Phase 1 presentation are available.
- Passed: Lease/Rent links are marked as Phase 2 / Upcoming where they remain visible.
- Passed: Lease-specific KPI cards are not visible in primary workspace card lists.
- Passed: ar.csv parses and Phase 2 labels are translated.
- Passed: Draft Sales Invoice ACC-SINV-2026-00001 remains Draft.
- Passed: No Payment Entry, Journal Entry, GL Entry from draft invoice, Rent Invoice DocType, Commission, CRM Matching, Portal, or GL backfill was created.
- Deferred: Full collections, Rent/Lease full cycle, Commission, CRM, Smart Matching, Backlog Matching, Portals, WhatsApp/Meta, and production accounting automation.
- Needs Attention: Monitor MariaDB memory because of previous OOM.

## 34. Phase 1 Closure Decision

Ready to present Phase 1 to the client and collect feedback before Phase 2 planning.
