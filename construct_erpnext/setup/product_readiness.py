import json

import frappe


PRODUCT_WORKSPACE_PATHS = {
	"Executive Presentation Center": "gcs_finance/workspace/executive_presentation_center/executive_presentation_center.json",
	"Executive Control Center": "gcs_finance/workspace/executive_control_center/executive_control_center.json",
	"Sales & Rental": "gcs_finance/workspace/sales_rental/sales_rental.json",
	"Construction Control": "gcs_projects/workspace/construction_control/construction_control.json",
	"Procurement & Site Warehouses": "gcs_projects/workspace/procurement_site_warehouses/procurement_site_warehouses.json",
	"Measurement & IPC": "gcs_projects/workspace/measurement_ipc/measurement_ipc.json",
	"Contractor Management": "gcs_projects/workspace/contractor_management/contractor_management.json",
	"Real Estate Inventory": "gcs_projects/workspace/real_estate_inventory/real_estate_inventory.json",
	"Reports & Analytics": "gcs_projects/workspace/reports_analytics/reports_analytics.json",
}

DEPRECATED_PROJECT_NUMBER_CARDS = {
	"PROJ-0002 BOQ Total",
	"PROJ-0002 Actual Amount",
	"PROJ-0002 Remaining Amount",
	"PROJ-0002 Overrun Items",
	"PROJ-0002 Certified Amount",
	"PROJ-0002 Unit Profitability",
}

PRESENTATION_NUMBER_CARDS = [
	{"label": "BOQ Total", "method": "construct_erpnext.cfo_analytics.presentation.boq_total", "document_type": "Project Financial Snapshot", "color": "#2563eb"},
	{"label": "Committed Amount", "method": "construct_erpnext.cfo_analytics.presentation.committed_amount", "document_type": "Construction Work Item", "color": "#7c3aed"},
	{"label": "Certified Gross Amount", "method": "construct_erpnext.cfo_analytics.presentation.certified_gross_amount", "document_type": "Interim Payment Certificate", "color": "#059669"},
	{"label": "Certified Amount", "method": "construct_erpnext.cfo_analytics.presentation.certified_amount", "document_type": "Interim Payment Certificate", "color": "#059669"},
	{"label": "Net Payable", "method": "construct_erpnext.cfo_analytics.presentation.net_payable", "document_type": "Interim Payment Certificate", "color": "#0891b2"},
	{"label": "Retention Held", "method": "construct_erpnext.cfo_analytics.presentation.retention_held", "document_type": "Retention Register", "color": "#b45309"},
	{"label": "Contractor Outstanding", "method": "construct_erpnext.cfo_analytics.presentation.contractor_outstanding", "document_type": "Contractor Account", "color": "#dc2626"},
	{"label": "Cash Flow Risk", "method": "construct_erpnext.cfo_analytics.presentation.cash_flow_risk", "document_type": "Project Cash Flow Forecast", "color": "#ea580c"},
	{"label": "EVM CPI", "method": "construct_erpnext.cfo_analytics.presentation.evm_cpi", "document_type": "Project EVM Metrics", "color": "#4f46e5"},
	{"label": "EVM SPI", "method": "construct_erpnext.cfo_analytics.presentation.evm_spi", "document_type": "Project EVM Metrics", "color": "#4f46e5"},
	{"label": "EVM Overall Status", "method": "construct_erpnext.cfo_analytics.presentation.evm_overall_status", "document_type": "Project EVM Metrics", "color": "#0f766e"},
	{"label": "Work Items Count", "method": "construct_erpnext.cfo_analytics.presentation.work_items_count", "document_type": "Construction Work Item", "color": "#2563eb"},
	{"label": "Invoiced Amount", "method": "construct_erpnext.cfo_analytics.presentation.invoiced_amount", "document_type": "Construction Work Item", "color": "#0891b2"},
	{"label": "Consumed Amount", "method": "construct_erpnext.cfo_analytics.presentation.consumed_amount", "document_type": "Construction Work Item", "color": "#b45309"},
	{"label": "Measured Amount", "method": "construct_erpnext.cfo_analytics.presentation.measured_amount", "document_type": "Measurement Entry", "color": "#0f766e"},
	{"label": "IPC Count", "method": "construct_erpnext.cfo_analytics.presentation.ipc_count", "document_type": "Interim Payment Certificate", "color": "#059669"},
	{"label": "Advance Balance", "method": "construct_erpnext.cfo_analytics.presentation.advance_balance", "document_type": "Advance Register", "color": "#b45309"},
	{"label": "Total Units", "method": "construct_erpnext.cfo_analytics.presentation.total_units", "document_type": "Unit", "color": "#2563eb"},
	{"label": "Available Units", "method": "construct_erpnext.cfo_analytics.presentation.available_units", "document_type": "Unit", "color": "#059669"},
	{"label": "Reserved Units", "method": "construct_erpnext.cfo_analytics.presentation.reserved_units", "document_type": "Unit", "color": "#b45309"},
	{"label": "Rented Units", "method": "construct_erpnext.cfo_analytics.presentation.rented_units", "document_type": "Unit", "color": "#0891b2"},
	{"label": "Expected Gross Margin", "method": "construct_erpnext.cfo_analytics.presentation.expected_gross_margin", "document_type": "Unit", "color": "#16a34a"},
	{"label": "Expected Margin %", "method": "construct_erpnext.cfo_analytics.presentation.expected_margin_percent", "document_type": "Unit", "color": "#16a34a"},
	{"label": "Active Reservations", "method": "construct_erpnext.cfo_analytics.presentation.active_reservations", "document_type": "Unit Reservation", "color": "#7c3aed"},
	{"label": "Expiring Reservations", "method": "construct_erpnext.cfo_analytics.presentation.expiring_reservations", "document_type": "Unit Reservation", "color": "#dc2626"},
	{"label": "Total Invoiced Sales", "method": "construct_erpnext.cfo_analytics.presentation.total_invoiced_sales", "document_type": "Sales Contract", "color": "#2563eb"},
	{"label": "Total Collected Sales", "method": "construct_erpnext.cfo_analytics.presentation.total_collected_sales", "document_type": "Sales Contract", "color": "#059669"},
	{"label": "Outstanding Sales Amount", "method": "construct_erpnext.cfo_analytics.presentation.outstanding_sales_amount", "document_type": "Sales Contract", "color": "#dc2626"},
	{"label": "Overdue Installments Count", "method": "construct_erpnext.cfo_analytics.presentation.overdue_installments_count", "document_type": "Sales Contract", "color": "#ea580c"},
	{"label": "Overdue Installments Amount", "method": "construct_erpnext.cfo_analytics.presentation.overdue_installments_amount", "document_type": "Sales Contract", "color": "#b45309"},
	{"label": "Sales Contracts", "method": "construct_erpnext.cfo_analytics.presentation.sales_contracts", "document_type": "Sales Contract", "color": "#2563eb"},
	{"label": "Draft Sales Invoices", "method": "construct_erpnext.cfo_analytics.presentation.draft_sales_invoices", "document_type": "Sales Invoice", "color": "#64748b"},
	{"label": "Active Lease Contracts", "method": "construct_erpnext.cfo_analytics.presentation.active_lease_contracts", "document_type": "Lease Contract", "color": "#2563eb"},
	{"label": "Scheduled Rental Value", "method": "construct_erpnext.cfo_analytics.presentation.scheduled_rental_value", "document_type": "Lease Contract", "color": "#059669"},
	{"label": "Expiring Leases", "method": "construct_erpnext.cfo_analytics.presentation.expiring_leases", "document_type": "Lease Contract", "color": "#ea580c"},
]


def sync_product_workspace_readiness():
	"""Keep installed product workspace records aligned with curated readiness JSON."""
	ensure_presentation_number_cards()
	app_path = frappe.get_app_path("construct_erpnext")

	for workspace_name, relative_path in PRODUCT_WORKSPACE_PATHS.items():
		with open(f"{app_path}/{relative_path}", encoding="utf-8") as workspace_file:
			source = json.load(workspace_file)

		if frappe.db.exists("Workspace", workspace_name):
			workspace = frappe.get_doc("Workspace", workspace_name)
		else:
			workspace = frappe.new_doc("Workspace")
			workspace.name = workspace_name

		workspace.label = source.get("label") or workspace.label
		workspace.title = source.get("title") or workspace.title
		workspace.module = source.get("module") or workspace.module
		workspace.icon = source.get("icon") or workspace.icon
		workspace.sequence_id = source.get("sequence_id") or workspace.sequence_id
		workspace.content = source.get("content") or workspace.content
		workspace.is_hidden = source.get("is_hidden", 0)
		workspace.public = source.get("public", 1)

		workspace.set("charts", [])
		for chart in source.get("charts", []):
			workspace.append("charts", {
				"chart_name": chart.get("chart_name"),
				"label": chart.get("label"),
			})

		workspace.set("number_cards", [])
		for card in source.get("number_cards", []):
			workspace.append("number_cards", {
				"number_card_name": card.get("number_card_name"),
				"label": card.get("label"),
			})

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


def ensure_presentation_number_cards():
	remove_deprecated_project_number_cards()

	for card in PRESENTATION_NUMBER_CARDS:
		if not frappe.db.exists("DocType", card["document_type"]):
			continue

		existing = frappe.db.exists("Number Card", card["label"])
		doc = frappe.get_doc("Number Card", existing) if existing else frappe.new_doc("Number Card")
		doc.update({
			"label": card["label"],
			"type": "Custom",
			"method": card["method"],
			"document_type": card["document_type"],
			"module": "GCS Finance",
			"is_public": 1,
			"show_full_number": 1,
			"color": card.get("color"),
		})
		doc.save(ignore_permissions=True)


def remove_deprecated_project_number_cards():
	for card_name in DEPRECATED_PROJECT_NUMBER_CARDS:
		if frappe.db.exists("Number Card", card_name):
			frappe.delete_doc("Number Card", card_name, ignore_permissions=True)
