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
