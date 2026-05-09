import frappe


WORKSPACE_LINKS = {
	"Real Estate Inventory": [
		{"type": "Card Break", "label": "Unit Costing"},
		{"type": "Link", "label": "Unit Cost Allocation", "link_type": "DocType", "link_to": "Unit Cost Allocation"},
		{"type": "Card Break", "label": "Unit Costing Reports"},
		{"type": "Link", "label": "Unit Cost Allocation Report", "link_type": "Report", "link_to": "Unit Cost Allocation Report", "is_query_report": 1},
		{"type": "Link", "label": "Unit Profitability Report", "link_type": "Report", "link_to": "Unit Profitability Report", "is_query_report": 1},
		{"type": "Link", "label": "Real Estate Project Profitability Summary", "link_type": "Report", "link_to": "Real Estate Project Profitability Summary", "is_query_report": 1},
		{"type": "Link", "label": "Building Profitability Summary", "link_type": "Report", "link_to": "Building Profitability Summary", "is_query_report": 1},
	],
	"Executive Control Center": [
		{"type": "Card Break", "label": "Unit Profitability"},
		{"type": "Link", "label": "Unit Profitability Report", "link_type": "Report", "link_to": "Unit Profitability Report", "is_query_report": 1},
		{"type": "Link", "label": "Real Estate Project Profitability Summary", "link_type": "Report", "link_to": "Real Estate Project Profitability Summary", "is_query_report": 1},
		{"type": "Link", "label": "Building Profitability Summary", "link_type": "Report", "link_to": "Building Profitability Summary", "is_query_report": 1},
	],
	"Reports & Analytics": [
		{"type": "Card Break", "label": "Unit Costing Reports"},
		{"type": "Link", "label": "Unit Cost Allocation Report", "link_type": "Report", "link_to": "Unit Cost Allocation Report", "is_query_report": 1},
		{"type": "Link", "label": "Unit Profitability Report", "link_type": "Report", "link_to": "Unit Profitability Report", "is_query_report": 1},
		{"type": "Link", "label": "Real Estate Project Profitability Summary", "link_type": "Report", "link_to": "Real Estate Project Profitability Summary", "is_query_report": 1},
		{"type": "Link", "label": "Building Profitability Summary", "link_type": "Report", "link_to": "Building Profitability Summary", "is_query_report": 1},
	],
}


def after_migrate():
	ensure_unit_costing_workspace_links()


def ensure_unit_costing_workspace_links():
	for workspace_name, links in WORKSPACE_LINKS.items():
		if not frappe.db.exists("Workspace", workspace_name):
			continue

		workspace = frappe.get_doc("Workspace", workspace_name)
		existing = {
			(link.type, link.label, link.get("link_type"), link.get("link_to"))
			for link in workspace.links
		}

		changed = False
		for link in links:
			key = (link.get("type"), link.get("label"), link.get("link_type"), link.get("link_to"))
			if key in existing:
				continue

			workspace.append("links", {
				"type": link.get("type"),
				"label": link.get("label"),
				"link_type": link.get("link_type"),
				"link_to": link.get("link_to"),
				"is_query_report": link.get("is_query_report", 0),
				"hidden": 0,
				"onboard": 0,
				"link_count": 0,
			})
			changed = True

		if changed:
			workspace.save(ignore_permissions=True)
