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

- Executive Control Center
- Construction Control
- Procurement & Site Warehouses
- Measurement & IPC
- Contractor Management
- Real Estate Inventory
- Sales & Rental
- Reports & Analytics

Existing GCS workspaces are implementation-era navigation and should be replaced or hidden from user-facing navigation. Keep the underlying construct_erpnext package and existing internal module folders for now; do not rename the Python package.

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
