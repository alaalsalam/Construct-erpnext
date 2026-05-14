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

## ADR-013: Cash Flow Forecast As Transaction-Based Projection

- Cash Flow Forecast foundation uses deterministic transaction-based projections and does not replace ERPNext accounting or bank/cash reports.
- Submitted Purchase Invoice outstanding is preferred over IPC payable when both represent the same contractor obligation.
- IPC net payable is counted when no linked submitted Purchase Invoice exists.
- Purchase Orders are counted only for their uninvoiced submitted amount.
- Retention release is forecast from Retention Register release_due_date and remaining_retention_amount.
- The forecast does not create Journal Entries, Payment Entries, Purchase Invoices, background jobs, or scheduled EVM automation.

## ADR-014: EVM Snapshot Calculations

- EVM foundation uses deterministic snapshot calculations from BOQ, IPC certification, actual cost, and planned progress percent.
- BAC is based on Construction Work Item planned amounts, EV on certified amounts, AC on invoiced actuals, and PV on BAC multiplied by planned progress percent.
- Automated schedule-derived PV and scheduled recalculation are deferred until the scheduling model is stabilized.
- Project EVM Metrics does not create or submit accounting documents and does not replace ERPNext accounting reports.

## ADR-015: Unit As Stable Asset, Tenant Deferred

- Unit is a standalone stable real estate asset/entity.
- Owner is modeled as Property Owner, and ownership is modeled separately through Property Ownership with percentage support.
- Property Ownership uses fieldname property_owner because owner is a reserved Frappe document metadata field.
- Tenant is intentionally excluded from Unit and will be linked later through Lease Contract.
- Sales Contract, Lease Contract, Reservation, Smart Matching, and Unit Cost Allocation are deferred to later phases.

## ADR-016: Unit Cost Allocation As Management Layer

- Unit Cost Allocation is a management/control layer that allocates project costs to real estate units without creating accounting entries.
- ERPNext accounting remains the source of truth for GL, invoices, payments, and official financial postings.
- Allocation documents preserve the allocation basis, source amount, unit lines, calculated percentages, and profitability status for review.
- Applying an allocation updates Unit allocated_cost, latest allocation, margin, and profitability status for operational reporting.
- Reversing or changing allocation policy must be handled as a controlled management update and must not erase accounting history.

## ADR-017: Dual Tracking With Accounting Dimensions

- The system uses a dual tracking model:
  1. Operational Tracking for BOQ, Measurement Book, IPC, Contractor Ledger, and Unit Cost Allocation.
  2. Accounting Dimensions for financial reporting and GL-level drilldown.
- Initial Accounting Dimensions are Construction Work Item, Cost Code, and Unit.
- Building, Floor, WBS Element, and Contractor are not Accounting Dimensions initially.
- Building and Floor can be derived from Unit.
- WBS Element can be derived from Construction Work Item.
- Contractor is already represented as Supplier/Party in ERPNext transactions.
- Accounting Dimensions complement existing operational links and do not replace them.
- No broad GL backfill is performed; dimensions apply prospectively and to draft-only sync.

## ADR-018: Historical GL Dimension Backfill Deferred

- Historical submitted GL rows created before Accounting Dimensions were enabled are not amended, reposted, or broadly backfilled.
- Draft documents may be synchronized through controlled draft-only methods before normal submission.
- Future submitted transactions should carry Accounting Dimensions prospectively through ERPNext Accounting Dimension fields and app-level validate hooks.
- Unit-level GL validation is deferred until a legitimate unit-specific accounting flow exists, such as Sales/Rental or an approved unit-specific cost posting flow.

## ADR-019: Product Readiness Before Reservation

- Product readiness, bilingual UX, workspace grouping, report i18n review, and client presentation QA are completed before Unit Reservation, Sales, and Rental development.
- English remains the source text for technical labels and report definitions.
- Arabic user experience is provided through translation files rather than replacing technical labels with Arabic.
- Product-facing workspaces are process-oriented and synchronized through an app-level after_migrate helper.
- Executive Number Cards and Dashboard Charts are deferred until finance leadership signs off on final KPI definitions; existing reports are used for presentation readiness.

## ADR-020: Unit Reservation As Temporary Commercial Hold

- Unit Reservation is a temporary commercial hold layer before Sales Contract or Lease Contract.
- Active reservations set the Unit to Reserved and prevent duplicate active reservations unless an administrator changes settings deliberately.
- Reservation may represent sale or rent intent, but it does not create accounting documents, invoices, payments, installments, commissions, or contracts.
- Tenant remains intentionally excluded from Unit; future tenant/customer occupancy will be modeled through Lease Contract or Sales/Rental documents.
- Cancelled or expired reservations release the Unit only when no other active reservation exists and the Unit is not Sold, Rented, Blocked, or Under Maintenance.

## ADR-021: Presentation Workspace Uses Deterministic KPIs

- Executive Presentation Center is a presentation/readiness workspace and does not add a new business process.
- KPI Number Cards use deterministic app-level whitelisted methods over existing DocTypes and reports.
- Number Cards are acceptable for presentation because they are read-only summaries and do not create or amend business records.
- Dashboard Charts are deferred until finance leadership approves chart definitions, KPI thresholds, and narrative wording.
- Existing operational reports remain the source of detail behind each KPI card.

## ADR-022: UX Readiness Changes Are Metadata Only

- Workspace and form UX completion changes are limited to layout, descriptions, list view visibility, translations, and readiness documentation.
- The phase does not change business logic, fieldnames, existing fieldtypes, required-field policy, accounting behavior, or submitted records.
- Section Breaks and Column Breaks are allowed as layout metadata to make completed custom DocTypes easier to explain and use.
- Sales Contract, Lease Contract, Installment Plan, Rent Schedule, CRM Matching, Portal, and accounting features remain deferred.

## ADR-023: Deep UX Hardening Before Sales Foundation

- The previous technical readiness gate is corrected by a deeper UX hardening phase before Sales Contract and Installment Plan work.
- Large completed DocTypes may use Tab Breaks, Section Breaks, and Column Breaks as layout metadata only.
- Fieldnames, fieldtypes, required flags, business logic, accounting behavior, and submitted records remain unchanged.
- English remains the source language for labels and descriptions.
- Arabic UX is hardened through `construct_erpnext/translations/ar.csv`, following the same source-text translation approach used by Universal Standard.
- Universal Standard is used as a read-only reference because it exists in bench apps but is not installed on `construction.yemenfrappe.com`.
- Sales Contract, Lease Contract, Installment Plan, Rent Schedule, CRM Matching, Portal, and accounting automation remain deferred until this UX layer passes validation.

## ADR-024: Sales Contract as Primary Operational Sales Transaction

- Sales Contract is the first actual sale transaction after Unit Reservation.
- Sales Contract is submittable and uses the Sales Contract Approval Workflow.
- Unit becomes Sold on approved/submitted Sales Contract (controlled by `mark_unit_sold_on_approval` in settings).
- Unit Reservation converts to status `Converted` on Sales Contract submission.
- Sales Contract does not create Sales Invoices, Payment Entries, or GL entries in this phase.
- Sales Order creation is deferred to a later phase.

## ADR-025: Sales Installment Schedule as Child Table Inside Sales Contract

- Sales Installment Schedule is a Child DocType linked to Sales Contract.
- Each row represents a scheduled payment with due date, percentage, amount, and status.
- Child table design prevents orphaned installment records and keeps contract and schedule lifecycle coupled.
- No Sales Invoice or Payment Entry is generated from installments in this phase.
- Future phases will add invoice/payment generation and status tracking.

## ADR-026: Unit Becomes Sold on Sales Contract Approval

- Unit.status and Unit.marketing_status are updated to `Sold` when a Sales Contract is submitted (if settings allow).
- Previous unit status is stored on the Sales Contract for safe rollback on cancellation.
- Cancellation restores unit status only if no other active sales contract or reservation exists.
- Sold in this system means "contracted for sale" and does not imply handover or title registration yet.

## ADR-027: No Accounting Documents Until Invoice Design

- Sales Invoice generation is explicitly disabled in Sales Contract Settings (`enable_sales_invoice_generation` default 0).
- Payment Entry creation is not implemented in this phase.
- GL entries are not created from Sales Contract.
- ERPNext accounting remains the source of truth; future phases will design the invoice/collection/accounting flow.
- Accounting Dimension `unit` is prepared on Sales Contract for future propagation to Sales Invoice, but no posting occurs now.

## ADR-028: Workflow Setup Must Use Frappe ORM

- Sales Contract Approval Workflow is created and repaired through Frappe ORM in an idempotent after_migrate setup.
- Direct MariaDB SQL is not used for Workflow, Workflow State, Workflow Action Master, or Workflow transition creation.
- Frappe v15 docstatus rules are respected: pre-submit cancellation is not forced through workflow SQL.
- Draft or Under Review contracts can return to Draft; cancellation is handled only through valid docstatus-aware workflow states.

## ADR-029: Sales Invoice and Collections From Installments

- Sales Invoice is generated from Sales Installment Schedule rows, not directly from Unit.
- Each installment row can be linked to only one active Sales Invoice; cancelled invoices release installment rows safely for re-invoicing.
- Unit is copied to Sales Invoice Item as the key revenue-side Accounting Dimension for future GL-level unit traceability.
- Project and cost center are copied where available; Construction Work Item and Cost Code remain cost-side dimensions and are not used for real estate sales revenue by default.
- Payment Entry remains ERPNext's source of truth for collections; the app reads linked Sales Invoice references to update Sales Contract and installment collection status.
- Sales Invoice submission and Payment Entry creation are not forced by default; draft invoice creation is the safe operational baseline.

## ADR-030: Lease Contract and Rent Schedule Foundation

- Lease Contract is the operational rental agreement before rent invoicing.
- Tenant/customer belongs to Lease Contract, not Unit.
- Rent Schedule is a child table inside Lease Contract and remains operational only in this phase.
- Unit becomes Rented only through an approved/submitted Lease Contract, with previous Unit state stored for safe release.
- A Rent Unit Reservation may convert into a Lease Contract; the reservation becomes Converted after lease approval.
- Rent Invoice and Payment Entry generation are deferred to the next rental finance phase.
- No Sales Invoice, Payment Entry, Journal Entry, GL Entry, commission, CRM matching, portal, or GL backfill is created by Lease Contract.

## ADR-031: Phase 1 Closure Before Phase 2

- Feature development pauses after Phase 1 readiness closure.
- Phase 1 is presented as an operational and executive foundation from construction control to draft sales invoice generation.
- Lease/Rent foundation records may exist, but full Lease/Rent cycle is treated as Phase 2 and is marked as Upcoming in primary presentation workspaces.
- Draft Sales Invoice from installment demonstrates traceability only; it is not submitted and does not create GL or Payment Entry.
- Phase 2 will be planned after client feedback and will cover collections, rent invoicing, commission, CRM, matching, portals, WhatsApp/Meta, and production accounting automation.

## ADR-032: Contractor Agreement Layer Uses Existing Subcontract

- The existing `Subcontract` DocType is enhanced and presented as `Contractor Agreement / اتفاقية مقاول` instead of creating a competing contractor contract structure.
- `Subcontract Activity` is enhanced as the agreement item table and links each row to Construction Work Item, BOQ, WBS, Cost Code, Item, UOM, measured quantities, certified quantities, and remaining values.
- Construction Work Item remains the operational bridge between BOQ, procurement, measurement, IPC, contractor ledger, and retention.
- Contractor Agreement activation links Work Items to the contractor/agreement and creates or reuses the operational Contractor Account.
- Measurement Entry and IPC now carry the Contractor Agreement where available so reports can trace BOQ -> Work Item -> Agreement -> Measurement -> IPC.
- Contractor Agreements do not create Purchase Invoices, Payment Entries, Journal Entries, or GL Entries.

## ADR-033: Sales Invoice Posting and Payment Entry Use ERPNext Standard Accounting

- Submitted Sales Invoices are created from Sales Installment Schedule rows and remain linked to Sales Contract, Unit, Real Estate Project, and Unit Reservation where available.
- Sales Invoice submission uses normal ERPNext `doc.submit()` validation; no accounting bypass or manual Journal Entry is allowed.
- Payment Entry is the official collection document and is created against submitted Sales Invoice references only.
- Unit dimension must remain present on Sales Invoice Item and resulting GL Entry so unit-level revenue traceability is preserved.
- Automatic bulk submission remains disabled; only controlled finance-approved invoices should be submitted.

## ADR-034: Rent Invoice and Rent Collections Use ERPNext Sales Invoice and Payment Entry

- Rent invoices are generated from Lease Contract Rent Schedule rows into standard ERPNext Sales Invoice.
- Rent Schedule remains the operational rental schedule source; each row can link to one active rent Sales Invoice.
- Unit is copied to Sales Invoice Item so rental revenue GL entries carry the Unit accounting dimension after normal Sales Invoice submission.
- Payment Entry remains ERPNext's official collection document for rent collections.
- Lease Contract totals and Rent Schedule statuses are synchronized from submitted Sales Invoices and Payment Entry references.
- Automatic bulk rent invoice submission remains disabled; controlled validation may submit one invoice/payment only through standard ERPNext validation.

## ADR-035: Brokerage Commission Is Operational Until Finance Payout Design

- Broker commission is tracked through `Broker`, `Commission Rule`, and `Commission Entry`.
- Commission can be calculated from Sales Contract, Lease Contract, or Sales Invoice source documents according to an active Commission Rule.
- Commission Entry does not create Payment Entry, Journal Entry, Purchase Invoice, or GL Entry.
- Broker payout accounting is deferred until finance approves accounts, taxes, payout workflow, and document controls.
- Duplicate commission entries are blocked for the same broker, rule, and source transaction unless a future split-commission design is approved.

## ADR-036: Real Estate CRM Captures Requirements Before Reservation

- Customer Requirement is the CRM source for buyer, renter, and investor needs before reservation or contract creation.
- Viewing Appointment and Real Estate Follow Up remain operational CRM records and do not change Unit status.
- CRM does not create Sales Contracts, Lease Contracts, Sales Invoices, Payment Entries, or Journal Entries.
- Matching and backlog automation are separate foundations and must consume Customer Requirement data without bypassing reservation rules.

## ADR-037: Smart Matching Is Advisory and Uses Available Units Only

- Smart Matching consumes Customer Requirement records and existing Unit inventory.
- Match Result records store ranked recommendations and explanation notes but do not create reservations or contracts.
- Reserved, Sold, Rented, Blocked, or otherwise unavailable Units are excluded from recommendations.
- Requirements with no result above the configured minimum score remain available for Backlog Matching.

## ADR-038: Backlog Matching Records Unmet Demand Without Automation Side Effects

- Backlog Request is created from Customer Requirements that do not receive a suitable Smart Matching result.
- Backlog Match Attempt records retry history and available units checked.
- Backlog Matching does not reserve units, create tasks, send external notifications, or create accounting documents.
- Notifications and automation are handled in a later readiness phase.

## ADR-039: Property Maintenance Is Operational Cost Tracking Only

- Property Maintenance Request and Property Maintenance Task track unit maintenance operations.
- Estimated and actual costs are management fields and do not post accounting.
- ERPNext Work Order, Purchase Invoice, Payment Entry, Journal Entry, and GL integration are deferred until a maintenance accounting design is approved.

## ADR-040: Property Document Management Is Metadata and Attachment Readiness

- Property Document stores document metadata and optional attachment links for projects, units, parties, and contracts.
- Contract Attachment Register stores contract-specific attachment references.
- No external storage, signing workflow, or portal document access is created in this phase.
- Access policy and retention controls are deferred to production hardening.
