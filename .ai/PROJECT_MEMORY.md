# Project Memory

- Product name: Real Estate Development ERP
- Base app: construct_erpnext
- Repository: alaalsalam/Construct-erpnext
- Canonical repository path: /home/frappe/frappe-bench/apps/construct_erpnext
- Target site: construction.yemenfrappe.com
- Goal: Build a full Construction + Real Estate Development ERP system on ERPNext/Frappe.
- Business flow:
  Land acquisition
  -> construction and development
  -> BOQ and budgets
  -> project procurement and site warehouses
  -> site progress and measurement
  -> contractor IPC
  -> invoices and payments
  -> real estate units
  -> sale/rent
  -> collections
  -> CFO dashboards and forecasting.
- Current strategy:
  Build inside the same app using internal modules.
  Do not create multiple apps now.
  Do not install utility-billing now.
  Use utility-billing only as reference for real estate hierarchy and leasing patterns.
- First technical priority:
  Remove or neutralize El Salvador localization and make the product generic.
