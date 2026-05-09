# Architecture

Internal modules planned inside construct_erpnext:

- construction_boq
- procurement_control
- measurement_ipc
- contractor_management
- real_estate_inventory
- estate_sales
- estate_rental
- unit_costing
- cfo_analytics
- forecasting
- crm_real_estate

## Product Workspace Structure

Final user-facing workspace structure for the generic product base:

- Executive Control Center: implemented as a product-facing Workspace.
- Construction Control: implemented as a product-facing Workspace.
- Procurement & Site Warehouses: implemented as a product-facing Workspace.
- Measurement & IPC: implemented as a product-facing placeholder Workspace.
- Contractor Management: implemented as a product-facing Workspace.
- Real Estate Inventory: implemented as a product-facing placeholder Workspace.
- Sales & Rental: implemented as a product-facing placeholder Workspace.
- Reports & Analytics: implemented as a product-facing Workspace.

## Construction BOQ Foundation

Implemented internal module: construction_boq / Construction BOQ.

New planning and control DocTypes:

- Cost Code: construction cost classification master.
- WBS Element: project-level work breakdown master with project-scoped WBS code validation.
- Construction BOQ: submittable BOQ header with editable child rows and calculated category totals.
- Construction BOQ Item: child table for BOQ line items, quantities, rates, wastage, markup, and final amount.
- Construction Work Item: operational work item generated from approved BOQ rows for future procurement, measurement, IPC, progress, and forecasting links.

BOQ reports:

- Construction BOQ Cost Analysis
- Construction BOQ Variance

Workflow:

- Construction BOQ Approval Workflow is created idempotently after migration.
- States: Draft, Under Review, Approved, Locked, Cancelled.
- Approval transition to Approved submits the BOQ and generates Construction Work Items.

Existing GCS workspaces are implementation-era navigation and are hidden from user-facing navigation through workspace JSON and a reversible patch. Keep the underlying construct_erpnext package and existing internal module folders for now; do not rename the Python package.

## Procurement Control Foundation

Implemented internal module: procurement_control / Procurement Control.

Procurement linkage design:

- Construction Work Item is the operational link between BOQ planning and ERPNext procurement/stock transactions.
- ERPNext procurement child rows are extended through app-level Custom Fields, not ERPNext core DocType edits.
- Material Request Item, Purchase Order Item, Purchase Receipt Item, Purchase Invoice Item, and Stock Entry Detail can link to Construction Work Item, Construction BOQ, WBS Element, Cost Code, and Site Warehouse.
- Warehouse can be marked as a site warehouse and linked to a construction project, site code, and site manager.
- Procurement totals on Construction Work Item are recalculated from submitted ERPNext documents only.
- Actual cost is not overwritten blindly; committed, invoiced, and consumed amounts are tracked separately for procurement control.

New settings:

- Procurement Control Settings: enables/disables Work Item sync, budget warnings, budget blocking, tolerance percentage, default site warehouse, and optional Work Item requirement for project purchases.

Procurement reports:

- Work Item Procurement Summary
- BOQ Procurement Pipeline
- Site Warehouse Consumption
- Procurement Budget Control

## Measurement Book Foundation

Implemented internal module: measurement_ipc / Measurement IPC.

Measurement design:

- Measurement Book groups field measurement activity by company, project, contractor, BOQ, and period.
- Measurement Entry is a standalone operational record linked to Measurement Book and Construction Work Item.
- Measurement Entries carry site/QS comments, location notes, image/file attachments, and optional GPS fields.
- Quantities support Direct Quantity, Length, Area, Volume, Count, and Manual methods.
- Verified/Locked Measurement Entries update Work Item measured quantity, measured amount, measurement progress, and measurement status.
- Certified quantity is not updated in this phase; certification remains reserved for the future IPC foundation.
- Future IPC generation must consume verified Measurement Entries rather than manually entered IPC lines.

Measurement reports:

- Measurement Book Register
- Work Item Measurement Progress
- Measurement Verification Queue

## Interim Payment Certificate Foundation

Implemented inside internal module: measurement_ipc / Measurement IPC.

IPC design:

- IPC is generated from Verified or Locked Measurement Entries through a verified Measurement Book.
- IPC is not entered manually from scratch for measured quantities.
- Existing Subcontract is used as the optional contractor contract reference; no Contractor Contract DocType was created in this phase.
- Interim Payment Certificate is submittable and uses Frappe Workflow for review, certification, and approval.
- Interim Payment Certificate Line stores Measurement Entry traceability, Construction Work Item, WBS, Cost Code, BOQ quantity, previous/current/total certified quantities, retention, and net line amount.
- IPC Deduction explains retention, advance recovery, penalty, withholding, and other deductions without forcing ledger/account treatment yet.
- Approved/submitted IPCs update Construction Work Item certification fields separately from Measurement Book measured fields.
- Purchase Invoice generation creates a draft ERPNext Purchase Invoice from an approved IPC and preserves the existing Purchase Invoice authorization process.
- Payment status reads ERPNext Purchase Invoice state; full contractor ledger and retention register are deferred.

IPC reports:

- IPC Register
- IPC Line Details
- Measurement to IPC Traceability
- Contractor IPC Summary

## Contractor Ledger And Retention Foundation

Implemented internal module: contractor_management / Contractor Management.

Contractor financial control design:

- Contractor Ledger is an operational subledger for contractor control and does not replace ERPNext GL accounting.
- ERPNext Purchase Invoice and Payment Entry remain the accounting source of truth.
- Contractor Account groups contractor/project/subcontract financial exposure.
- Contractor Ledger Entry records auditable operational events such as IPC Certified, Retention Held, Advance Recovery, Purchase Invoice Created, Payment Made, and Payment Difference.
- Retention Register tracks retention held from IPCs and future release eligibility without creating Journal Entries automatically.
- Advance Register tracks contractor advances and recovery through IPCs without overriding ERPNext Payment Entry.
- Guarantee Register tracks performance, advance payment, and retention guarantees without external bank integration.
- IPC submission creates contractor ledger and retention records.
- IPC Purchase Invoice creation creates/updates operational ledger references only; it does not submit the invoice.
- Payment Entry hooks read ERPNext allocations to update contractor ledger and IPC payment status without changing standard payment behavior.

Contractor control reports:

- Contractor Account Statement
- Retention Register Report
- Advance Recovery Report
- Contractor Exposure Summary
- Guarantee Register Report

## Project Financial Snapshot And CFO Analytics Foundation

Implemented internal module: cfo_analytics / CFO Analytics.

CFO analytics design:

- Project Financial Snapshot is the first point-in-time CFO aggregation layer.
- It summarizes BOQ planned value, procurement commitments, invoiced and consumed amounts, measured progress, certified IPC amounts, retention, contractor paid amount, contractor outstanding exposure, variances, and simple risk indicators.
- The snapshot reads operational values from Construction Work Item, Interim Payment Certificate, Contractor Account, and Retention Register.
- It does not replace ERPNext accounting reports or GL.
- It does not create Journal Entries, Cash Flow Forecast documents, or scheduled EVM automation.
- Risk status is deterministic and explainable:
  - Cost risk is Red if committed amount exceeds BOQ total, Yellow if committed amount is at least 90 percent of BOQ total, otherwise Green.
  - Cash risk is Red if contractor outstanding is more than 75 percent of certified net amount, Yellow if more than 40 percent, otherwise Green.

CFO reports:

- Project Financial Snapshot Report
- CFO Project Control Summary
- Work Item Financial Traceability
- Contractor Financial Exposure

## Role-Oriented Navigation

- Executive / CFO: Executive Control Center, Reports & Analytics, selected Finance records.
- Project Manager: Construction Control, Contractor Management, Measurement & IPC, Reports & Analytics.
- Site Engineer: Construction Control, Procurement & Site Warehouses, Measurement & IPC.
- QS Engineer: Construction Control, Measurement & IPC, Contractor Management, Reports & Analytics.
- Procurement Officer: Procurement & Site Warehouses, Contractor Management.
- Finance Officer: Executive Control Center, Contractor Management, Sales & Rental, Reports & Analytics.
- Contractor Portal User: Contractor Management and portal-only project/IPC views.

## Existing DocTypes To Reuse

- Construction Budget
- Budget Level
- Budget Change Order
- Activity Schedule
- Physical Advancement
- Project Cost Entry
- Labor Hour Entry
- Equipment Usage Log
- Material Distribution
- Insumo
- Insumo Price Scenario
- Subcontract
- Subcontract Activity
- Project Invoice
- Project Revenue
- Invoice Authorization
- Check Request
- Collection Document
- Deposit Entry
- Financial Ratio
- Financial Ratio Result
- Client Portal Access
- Client Portal Project
- Audit Trail Config
- Audit Trail Entry

## Existing DocTypes To Hide From Primary Workspaces For Now

- Process Parameter
- Process Traceability Log
- SPC Control Chart
- SPC Data Point
- Traceability Batch Item
- Corrective Action Tracker
- Maintenance Routine
- Maintenance Contractor
- Asset Component
- Downtime Record
- Failure Analysis
- Failure Mode
- ISO Compliance Checklist
- Payroll Movement
- Payroll Cost Distribution
- Employee Loan
- Overtime Administration
- Vacation Policy
- Salary Adjustment Request
- Withholding Liquidation
- Advance Payment Tracker
- Alternative Payment Document
- Auto Journal Entry Rule
- Check Batch Print
- Access Scope
- Role Group
- Audit Trail Export
- Meta Audit Entry

## Labels To Clean Up

- Remove user-facing "GCS" workspace labels, titles, and module naming from navigation.
- Keep internal module paths and module names until a controlled migration/rename strategy exists.
- Keep El Salvador legacy helpers isolated and hidden from workspaces.
- Replace "Insumo" with user-facing "Cost Resource" or "Resource Item" in navigation later.
- Review README/translations for legacy El Salvador terms before public release.
