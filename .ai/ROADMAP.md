# Roadmap

- Phase 0: Project memory
- Phase 1: De-localization / remove El Salvador dependency
- Phase 2: Product stabilization and Workspace/UX cleanup
- Phase 3: Construction BOQ
- Phase 4: Procurement and site warehouses
- Phase 5: Measurement Book
- Phase 6: IPC and contractor billing
- Phase 7: CFO analytics and forecasting
- Phase 8: Real estate inventory
- Phase 9: Sales and rental
- Phase 10: CRM, matching, and backlog

Phase 2 deliverables:

- Replace GCS-facing navigation with product workspaces. Completed.
- Hide manufacturing, maintenance, payroll, and security implementation workspaces from primary users. Completed through reversible patch.
- Keep useful construction finance/project DocTypes available under role-oriented workspaces. Completed for existing DocTypes/reports.
- Do not create BOQ, IPC, or real estate DocTypes during Phase 2.
- Keep construct_erpnext package name and existing construction modules working.

Phase 3 deliverables:

- Create Construction BOQ foundation. Completed.
- Create Cost Code and WBS Element masters. Completed.
- Create Construction BOQ and Construction BOQ Item planning structure. Completed.
- Generate standalone Construction Work Items from approved BOQ rows. Completed.
- Add BOQ cost analysis and variance reports. Completed.
- Add BOQ links to Construction Control and Reports & Analytics workspaces. Completed.
- Next Phase 3/4 bridge: link BOQ Work Items to procurement and site warehouse flows.

Phase 4 deliverables:

- Link Construction Work Items to Material Request, Purchase Order, Purchase Receipt, Purchase Invoice, and Stock Entry rows. Completed.
- Add site warehouse metadata to Warehouse. Completed.
- Add Procurement Control Settings. Completed.
- Add Work Item procurement recalculation from submitted procurement and stock documents. Completed.
- Add draft Material Request generation from material Work Items. Completed as a whitelisted method.
- Add procurement control reports and workspace links. Completed.
- Next Phase 5: design and implement Measurement Book foundation.

Phase 5 deliverables:

- Normalize reusable operational baseline records to clear Arabic, non-country-specific names. Completed.
- Create Measurement Book and Measurement Entry foundation. Completed.
- Add Work Item measurement progress fields without changing certified_qty. Completed.
- Add Measurement Book Verification Workflow. Completed.
- Add measurement register, progress, and verification queue reports. Completed.
- Add Measurement & IPC and Reports & Analytics workspace links for measurement. Completed.
- Next Phase 6: design and implement Interim Payment Certificate foundation.

Phase 6 deliverables:

- Inspect existing Subcontract/Subcontract Activity and decide contractor contract reference. Completed.
- Create Interim Payment Certificate, Interim Payment Certificate Line, and IPC Deduction foundation. Completed.
- Generate IPC from verified Measurement Entries through Measurement Book. Completed.
- Update Work Item certified quantity and certification progress separately from measured quantity. Completed.
- Add draft Purchase Invoice creation from approved IPC. Completed.
- Add IPC approval workflow and IPC reports. Completed.
- Add IPC workspace links across Measurement & IPC, Contractor Management, Executive Control Center, and Reports & Analytics. Completed.
- Create Contractor Account, Contractor Ledger Entry, Retention Register, Advance Register, and Guarantee Register foundation. Completed in code.
- Integrate IPC, draft Purchase Invoice, and Payment Entry events with operational contractor ledger. Completed in code.
- Add contractor account, retention, advance recovery, exposure, and guarantee reports. Completed in code.
- Add contractor financial control links to Contractor Management, Executive Control Center, and Reports & Analytics workspaces. Completed in code.
- Site migration, cache clear, existing IPC sync, contractor account totals, retention register, reports, and workspace checks completed after MariaDB service recovery.
- Next Phase 7: design and implement Project Financial Snapshot and CFO Analytics foundation.

Phase 7 deliverables:

- Create Project Financial Snapshot DocType. Completed.
- Add deterministic CFO aggregation service for BOQ, procurement, measurement, IPC, retention, and contractor exposure. Completed.
- Add whitelisted snapshot data and snapshot creation methods. Completed.
- Add CFO reports: Project Financial Snapshot Report, CFO Project Control Summary, Work Item Financial Traceability, Contractor Financial Exposure. Completed.
- Add CFO links to Executive Control Center and Reports & Analytics. Completed.
- Create retained Arabic validation snapshot for مشروع البرج السكني المتكامل. Completed.
- Cash Flow Forecast full engine and scheduled EVM automation remain deferred.
- Next Phase 7 extension: design and implement Cash Flow Forecast foundation.
- Create Project Cash Flow Forecast and Project Cash Flow Forecast Period DocTypes. Completed.
- Add deterministic cash flow forecast service based on Purchase Orders, Purchase Invoices, IPC payables, and Retention Register due dates. Completed.
- Add whitelisted forecast data and forecast creation methods. Completed.
- Add cash flow reports: Project Cash Flow Forecast Report, Project Cash Requirement Summary, Contractor Payment Forecast, Retention Release Forecast. Completed.
- Add cash flow links to Executive Control Center and Reports & Analytics. Completed.
- Create retained Arabic validation forecast for مشروع البرج السكني المتكامل. Completed.
- Sales inflows, rental income, customer installments, full bank/cash integration, and scheduled EVM automation remain deferred.
- Next Phase 7 extension: design and implement EVM Metrics foundation.
- Create Project EVM Metrics DocType. Completed.
- Add deterministic EVM service for BAC, EV, AC, PV, CV, SV, CPI, SPI, EAC, ETC, VAC, and TCPI. Completed.
- Add whitelisted EVM data and snapshot creation methods. Completed.
- Add EVM reports: Project EVM Metrics Report, EVM Forecast Summary, Project Performance Dashboard Report. Completed.
- Add EVM links to Executive Control Center and Reports & Analytics. Completed.
- Create retained Arabic validation EVM snapshot for مشروع البرج السكني المتكامل. Completed.
- Automated schedule-derived PV, scheduled recalculation, AI forecasting, and Real Estate Inventory remain deferred.
- Next Phase 8: design and implement Real Estate Inventory foundation.

Phase 8 deliverables:

- Create Real Estate Project, Building, Floor, Unit Type, Unit, Property Owner, and Property Ownership DocTypes. Completed.
- Implement inventory services and controllers for unit counts, status alignment, margin calculation, and ownership percentage validation. Completed.
- Add inventory reports: Unit Inventory Report, Unit Availability Report, Ownership Summary Report, Real Estate Project Summary. Completed.
- Add Real Estate Inventory workspace links and executive/reporting links. Completed.
- Create retained Arabic validation inventory for مشروع البرج السكني المتكامل. Completed.
- Create Unit Cost Allocation and Unit Cost Allocation Line DocTypes. Completed.
- Implement deterministic unit cost allocation by area, equal share, manual percentage, and manual amount. Completed.
- Apply allocation to Unit allocated cost, margin, and profitability fields without accounting entries. Completed.
- Add unit costing reports: Unit Cost Allocation Report, Unit Profitability Report, Real Estate Project Profitability Summary, Building Profitability Summary. Completed.
- Add Unit Costing links to Real Estate Inventory, Executive Control Center, and Reports & Analytics workspaces. Completed.
- Add ERPNext Accounting Dimensions for Construction Work Item, Cost Code, and Unit. Completed.
- Add Financial Dimension Settings and draft-only dimension sync. Completed.
- Add GL/unit/work item/cost code/project-unit financial traceability reports. Completed.
- Add financial traceability links to Executive Control Center, Reports & Analytics, Real Estate Inventory, and Construction Control. Completed.
- Tenant, Lease Contract, Sales Contract, Reservation, and Smart Matching remain deferred.
- Run end-to-end traceability validation before Reservation and Sales/Rental foundation. Completed.
- Complete Product Readiness, Bilingual UX, Client Presentation QA, workspace polish, report i18n review, and readiness documentation before Unit Reservation. Completed.
- Phase 9 entry: Unit Reservation foundation. Completed.
- Unit Reservation Settings created for reservation validity, duplicate rules, party requirement, and expiry warnings.
- Unit Reservation created as a submittable transaction before future Sales Contract or Lease Contract.
- Active reservations set Unit status and marketing_status to Reserved.
- Duplicate active reservations are blocked by default.
- Cancelled and expired reservations release the Unit to Available only when safe.
- Reservation reports and workspace links added to Sales & Rental, Real Estate Inventory, Executive Control Center, and Reports & Analytics.
- Daily expiry utility is enabled through scheduler and can also be called explicitly.
- No Sales Contract, Lease Contract, installments, collections, invoices, payments, CRM matching, portal features, or accounting documents were created.
- Presentation UX and Executive Dashboard Polish completed:
  - Executive Presentation Center workspace added for the client-facing product storyline.
  - KPI Number Cards added for core construction, CFO, inventory, and reservation indicators using deterministic app methods.
  - Existing product workspaces remain grouped by operational process.
  - Dashboard Charts are deferred until finance KPI/chart sign-off.
- Workspace and Form UX Completion completed:
  - Product workspaces reordered by process.
  - Completed custom DocTypes polished with business sections, concise field descriptions, and improved list views.
  - Arabic translations extended for section labels and important descriptions.
  - No new business/accounting features were introduced.
- Final Readiness Gate completed, then corrected by user feedback requiring deeper UX hardening before Sales Contract.
- Deep Form/Workspace UX Hardening completed:
  - Universal Standard inspected and used as a read-only translation/RTL UX reference.
  - Large completed DocTypes hardened with Tab Breaks, Section Breaks, and Column Breaks.
  - 32 custom DocTypes reviewed with 100 percent field description coverage.
  - Arabic translation coverage hardened for DocTypes, fields, descriptions, workspaces, reports, and KPI cards.
  - Major workspaces received deterministic KPI Number Cards or process cards.
  - Dashboard Charts remain deferred until finance KPI/chart sign-off.
  - No Sales Contract, Lease Contract, Installment Plan, Rent Schedule, CRM Matching, Portal, accounting document, submitted amendment, or GL backfill was introduced.
- Next Phase 9 task: Start Sales Contract and Installment Plan foundation.

Phase 9 Sales Contract and Installment Plan deliverables:

- Create Sales Contract Settings, Sales Contract, and Sales Installment Schedule DocTypes. Completed.
- Implement contract number generation, unit metadata fetch, party validation, installment schedule calculation and validation, Unit Sold status on approval, and reservation conversion. Completed.
- Add Sales Contract Approval Workflow through idempotent after_migrate setup. Completed.
- Add 5 Script Reports for Sales Contract Register, Installment Schedule Report, Unit Sales Pipeline, Sales Value Summary, and Reserved to Sold Conversion Report. Completed.
- Update Sales & Rental, Real Estate Inventory, Executive Control Center, Executive Presentation Center, and Reports & Analytics workspaces with sales links. Completed.
- Extend Arabic translations for new DocTypes, fields, sections, tabs, workflow states, installment types, statuses, and reports. Completed.
- Arabic validation completed on construction.yemenfrappe.com. Completed.
- No Sales Invoice, Payment Entry, Lease Contract, Rent Schedule, Commission, CRM Matching, Portal, accounting documents, or ERPNext core modifications were created.
- Next Phase 9 extension: Review Sales Contract readiness before Sales Invoice and Collections foundation.
