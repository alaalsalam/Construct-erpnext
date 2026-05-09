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
