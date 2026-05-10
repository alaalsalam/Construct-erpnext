import json

import frappe


PRODUCT_WORKSPACE_PATHS = {
	"Executive Control Center": "gcs_finance/workspace/executive_control_center/executive_control_center.json",
	"Sales & Rental": "gcs_finance/workspace/sales_rental/sales_rental.json",
	"Construction Control": "gcs_projects/workspace/construction_control/construction_control.json",
	"Procurement & Site Warehouses": "gcs_projects/workspace/procurement_site_warehouses/procurement_site_warehouses.json",
	"Measurement & IPC": "gcs_projects/workspace/measurement_ipc/measurement_ipc.json",
	"Contractor Management": "gcs_projects/workspace/contractor_management/contractor_management.json",
	"Real Estate Inventory": "gcs_projects/workspace/real_estate_inventory/real_estate_inventory.json",
	"Reports & Analytics": "gcs_projects/workspace/reports_analytics/reports_analytics.json",
}


def sync_product_workspace_readiness():
	"""Keep installed product workspace records aligned with curated readiness JSON."""
	app_path = frappe.get_app_path("construct_erpnext")

	for workspace_name, relative_path in PRODUCT_WORKSPACE_PATHS.items():
		if not frappe.db.exists("Workspace", workspace_name):
			continue

		with open(f"{app_path}/{relative_path}", encoding="utf-8") as workspace_file:
			source = json.load(workspace_file)

		workspace = frappe.get_doc("Workspace", workspace_name)
		workspace.label = source.get("label") or workspace.label
		workspace.title = source.get("title") or workspace.title
		workspace.content = source.get("content") or workspace.content
		workspace.is_hidden = source.get("is_hidden", 0)
		workspace.public = source.get("public", 1)

		workspace.set("links", [])
		for link in source.get("links", []):
			workspace.append("links", {
				"type": link.get("type"),
				"label": link.get("label"),
				"link_type": link.get("link_type"),
				"link_to": link.get("link_to"),
				"is_query_report": link.get("is_query_report", 0),
				"hidden": link.get("hidden", 0),
				"onboard": link.get("onboard", 0),
				"link_count": link.get("link_count", 0),
			})

		workspace.save(ignore_permissions=True)
