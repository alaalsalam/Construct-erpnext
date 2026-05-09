# Risks

Initial risks:

- Existing app contains El Salvador tax and payroll setup.
- hooks.py contains overrides and document events on core ERPNext DocTypes.
- Purchase Invoice and Salary Slip events may contain country-specific logic.
- App package rename is risky and postponed.
- BOQ, Measurement Book, IPC, and Forecasting must be built from scratch.

Updated risks:

- Legacy El Salvador modules still exist in setup/tax_setup.py, setup/payroll_setup.py, setup/custom_fields.json, and gcs_admin/tax_withholding.py, but are no longer called automatically.
- Overtime Administration and Vacation Policy still contain El Salvador-specific behavior and should be reviewed before production use.
- Existing sites may already have sv_* custom fields, IVA/ISR accounts, or ISSS/AFP/Aguinaldo salary components from previous installs.
- Fixture export rules could capture existing country-specific Custom Fields if they exist in a configured site and are exported later.
- Purchase Invoice authorization remains active and must be validated independently from the disabled withholding logic.
- construction.yemenfrappe.com now has HRMS installed because construct_erpnext requires it; HRMS workflows and permissions should be reviewed for this product.
- The installed construct_erpnext code comes from the local feature/product-delocalization working tree with uncommitted cleanup and .ai memory changes; commit and push before treating the deployment as reproducible.
- Previous path apps/Construct-erpnext was renamed to apps/construct_erpnext; older editor windows, shell sessions, or documentation may still point to the removed path.
- Original upstream README may target v16, but current deployment is v15.
- Need smoke test for all existing modules before adding BOQ/IPC.
- Site-level smoke testing currently depends on MariaDB availability; latest check failed with connection refused on 127.0.0.1.
- Plain system python3 does not import bench editable apps; use the bench virtualenv Python for import smoke checks unless system Python is explicitly configured.
- Legacy GCS module names remain in metadata even though user-facing workspaces are product-oriented; full module renaming remains postponed.
- Workspace visibility for existing GCS records required a database patch because JSON sync alone did not update existing records.
- Construction BOQ workflow must be kept in sync through after_migrate setup because Workflow records are not part of Frappe v15 model sync.
- construction.yemenfrappe.com currently lacks normal baseline Company/Project data for full end-user BOQ entry validation; rollback-only validation used lightweight records and did not leave seed data.
- Construction Work Item currently tracks planned and certified quantities only; procurement, stock, actual cost, Measurement Book, and IPC links still need implementation.
- construction.yemenfrappe.com initially lacked baseline ERPNext Company, Item Group, UOM, Item, Supplier, Project, and Warehouse records; reusable operational baseline records were created on 2026-05-09.
- Procurement Custom Fields are created through an idempotent after_migrate setup hook and must remain compatible with ERPNext v15 child table schemas.
- Procurement totals currently assume standard ERPNext docstatus semantics: only submitted documents are counted, and cancelled/draft documents are excluded.
- Stock consumption totals currently use submitted Stock Entry Detail rows with a source warehouse; transfer and manufacture semantics may need refinement once site warehouse operating procedures are finalized.
- Work Item actual_cost is intentionally not updated by procurement sync yet; dashboards must use committed_amount, invoiced_amount, and consumed_amount until the actual-cost policy is finalized.
- Site language and timezone were unset and blocked ERPNext amount-in-words generation; System Settings now use language en and time zone Asia/Aden.
- Submitted procurement validation records are intentionally retained; future validation must account for existing submitted MR, PO, PR, PI, Stock Entry, and stock ledger impact.
- Baseline operational names were normalized to Arabic and System Settings language is now ar; future validation should watch for ERPNext translation, PDF, and amount-in-words behavior in Arabic.
- ERPNext Company country is mandatory; the existing Country value was retained because no generic Country master exists and no country-specific tax setup was added.
- Submitted and linked document names such as ANK-BOQ-FOUNDATION-001 were not force-renamed; Arabic meaning is stored in visible title/description fields where safe.
- Measurement Book updates Work Item measured progress but intentionally does not update certified_qty; IPC must be the certification layer.
- Measurement Book workflow is created through after_migrate setup and depends on Workflow State and Workflow Action Master records being present or created idempotently.
- construction.yemenfrappe.com had construct_erpnext installed but missing from sites/apps.txt; the app was added back to apps.txt so Frappe can build the module map and load Measurement IPC controllers.
- IPC Purchase Invoice creation currently creates a draft invoice only; submitted Purchase Invoice authorization and payment application remain under ERPNext finance controls.
- IPC retention, advance recovery, penalties, withholding, and other deductions are represented on the IPC but do not yet create ledger entries; this must be handled by the Contractor Ledger and Retention Register phase.
- Partial payment validation was not executed because the IPC Purchase Invoice remains a draft; Payment Entry validation requires the standard ERPNext invoice submission/authorization path first.
