import frappe


def execute(filters=None):
	filters = filters or {}
	parent_filters = {}
	if filters.get("customer_requirement"):
		parent_filters["customer_requirement"] = filters.get("customer_requirement")
	parents = frappe.get_all("Match Result", filters=parent_filters, pluck="name")
	data = []
	if parents:
		item_filters = {"parent": ["in", parents]}
		if filters.get("unit"):
			item_filters["unit"] = filters.get("unit")
		items = frappe.get_all(
			"Match Result Item",
			filters=item_filters,
			fields=["parent as match_result", "unit", "score", "unit_status", "unit_type", "area", "price_or_rent", "matched_criteria", "missed_criteria"],
			order_by="score desc",
		)
		requirements = dict(frappe.get_all("Match Result", filters={"name": ["in", parents]}, fields=["name", "customer_requirement"], as_list=1))
		for row in items:
			row.customer_requirement = requirements.get(row.match_result)
			data.append(row)
	return [
		{"label": "Match Result", "fieldname": "match_result", "fieldtype": "Link", "options": "Match Result", "width": 150},
		{"label": "Customer Requirement", "fieldname": "customer_requirement", "fieldtype": "Link", "options": "Customer Requirement", "width": 170},
		{"label": "Unit", "fieldname": "unit", "fieldtype": "Link", "options": "Unit", "width": 130},
		{"label": "Score", "fieldname": "score", "fieldtype": "Float", "width": 100},
		{"label": "Unit Status", "fieldname": "unit_status", "fieldtype": "Data", "width": 110},
		{"label": "Unit Type", "fieldname": "unit_type", "fieldtype": "Link", "options": "Unit Type", "width": 120},
		{"label": "Area", "fieldname": "area", "fieldtype": "Float", "width": 100},
		{"label": "Price or Rent", "fieldname": "price_or_rent", "fieldtype": "Currency", "width": 130},
		{"label": "Matched Criteria", "fieldname": "matched_criteria", "fieldtype": "Data", "width": 220},
		{"label": "Missed Criteria", "fieldname": "missed_criteria", "fieldtype": "Data", "width": 220},
	], data
