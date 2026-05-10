# Traceability Validation

## 2026-05-10 09:32:24 CEST

## Executive Summary

End-to-end traceability validation was completed on construction.yemenfrappe.com before starting Reservation, Sales, or Rental foundations.

The operational chain is working:

BOQ -> Construction Work Item -> Procurement / Stock / Measurement -> IPC -> Contractor Ledger -> Unit Costing -> Accounting Dimensions / Reports.

It is safe to proceed to Unit Reservation foundation with one important boundary: Accounting Dimensions are prospective. Historical submitted GL rows created before the Accounting Dimensions were enabled were not amended, reposted, or backfilled.

## What Passed

- Accounting Dimensions exist and are enabled:
  - Construction Work Item / construction_work_item
  - Cost Code / cost_code
  - Unit / unit
- Financial Dimension Settings exists with warning/non-blocking defaults:
  - enable_financial_dimension_sync = 1
  - enable_dimension_warnings = 1
  - enable_dimension_blocking = 0
  - allow_blank_unit_for_project_level_cost = 1
  - default_dimension_mode = Warning
- Dimension fields exist on expected accounting/transaction rows:
  - Purchase Invoice Item
  - Stock Entry Detail
  - Journal Entry Account
  - GL Entry
  - Sales Invoice Item
- Draft Purchase Invoice ACC-PINV-2026-00002 remains Draft and is linked to IPC-2026-00001.
- Draft-only dimension backfill was run on ACC-PINV-2026-00002.
- ACC-PINV-2026-00002 item row contains:
  - construction_work_item = CWI-2026-00001
  - cost_code = CC-CONC
  - unit = blank, allowed for project-level contractor cost
  - project = PROJ-0001
  - construction_boq = ANK-BOQ-FOUNDATION-001
  - wbs_element = PROJ-0001-01.01
- Purchase Invoice submission was not attempted because Invoice Authorization is active and no Authorized Invoice Authorization exists for ACC-PINV-2026-00002.
- Existing Stock Entry MAT-STE-2026-00001 is linked at row level to CWI-2026-00001 and CC-CONC.
- Measurement Book MB-2026-00001 is Verified.
- Measurement Entry ME-2026-00001 is Verified and linked to IPC-2026-00001.
- IPC-2026-00001 is submitted with status Invoice Created.
- Construction Work Item CWI-2026-00001 shows:
  - measured_qty = 25
  - measurement_progress_percent = 25
  - certified_qty = 25
  - certification_status = Partially Certified
- Contractor Account CA-2026-00001 totals remain consistent:
  - total_certified_amount = 875000
  - total_retention_held = 87500
  - total_invoiced_amount = 875000
  - total_paid_amount = 0
  - outstanding_balance = 787500
- Retention Register RET-2026-00001 remains Held with release_due_date 2027-05-09.
- Unit Cost Allocation UCA-2026-00001 remains Applied:
  - source amount = 3500000
  - total allocated amount = 3500000
  - unallocated amount = 0

## Report Validation

The following reports loaded without errors:

- GL Dimension Traceability
- Unit Financial Ledger
- Work Item Financial Ledger
- Cost Code Financial Analysis
- Project Unit Cost Matrix
- Work Item Procurement Summary
- Construction BOQ Variance
- Measurement to IPC Traceability
- Contractor Account Statement
- Project Financial Snapshot Report
- Project Cash Flow Forecast Report
- Project EVM Metrics Report
- Unit Profitability Report

Reports degrade gracefully when historical GL rows do not yet contain the new dimensions.

## End-To-End Checklist

A. BOQ to Work Item: Passed.

- Construction BOQ ANK-BOQ-FOUNDATION-001 exists, is submitted, and has status Approved.
- Construction Work Item CWI-2026-00001 was generated.

B. Work Item to Procurement: Passed.

- Material Request MAT-MR-2026-00001 is linked to CWI-2026-00001 and CC-CONC.
- Purchase Order PUR-ORD-2026-00003 is linked to CWI-2026-00001 and CC-CONC.
- Purchase Receipt MAT-PRE-2026-00001 is linked to CWI-2026-00001 and CC-CONC.
- Purchase Invoice ACC-PINV-2026-00001 is submitted and linked to CWI-2026-00001 and CC-CONC.
- Purchase Invoice ACC-PINV-2026-00002 is draft, linked to IPC-2026-00001, and dimension-synced.

C. Work Item to Stock: Passed with historical GL limitation.

- Stock Entry MAT-STE-2026-00001 is submitted and row-linked to CWI-2026-00001 and CC-CONC.
- GL rows for MAT-STE-2026-00001 have blank new dimension fields because the stock entry was submitted before Accounting Dimensions were enabled.
- No repost or broad GL backfill was performed.

D. Work Item to Measurement: Passed.

- Measurement Entry ME-2026-00001 is linked to CWI-2026-00001.
- Work Item measured quantity and progress are updated.

E. Measurement to IPC: Passed.

- IPC-2026-00001 was generated from verified measurement.
- Work Item certified quantity is updated separately from measured quantity.

F. IPC to Contractor Ledger: Passed.

- Contractor Account CA-2026-00001 is updated.
- Retention Register RET-2026-00001 is updated.

G. Financial Dimensions: Passed prospectively.

- Accounting Dimensions exist.
- Draft PI rows are synced.
- Submitted historical GL dimension fields are blank where the source transaction predates the dimension activation.
- No submitted documents were amended.
- No broad GL backfill was run.

H. Unit Costing: Passed.

- Unit Cost Allocation UCA-2026-00001 is applied.
- Unit profitability reporting works.
- Unit GL validation is pending until future unit-specific accounting transactions exist, such as Sales/Rental or controlled unit-specific cost postings.

## What Is Pending

- Submit ACC-PINV-2026-00002 only after a normal Invoice Authorization record is Authorized.
- Validate future submitted GL rows carrying construction_work_item, cost_code, and unit after normal business transactions are posted under the new dimension setup.
- Validate Unit dimension on GL after Sales/Rental or another approved unit-specific accounting flow exists.
- Payment Entry validation remains pending until the IPC Purchase Invoice is submitted through normal ERPNext controls.

## Known Limitation

Historical submitted GL rows before Accounting Dimensions do not have dimension values.

## Decision

No broad GL backfill is performed now. Submitted accounting history remains unchanged.

## Recommendation

Future transactions should carry dimensions prospectively through draft sync and validate hooks. Unit Reservation foundation can proceed next.
