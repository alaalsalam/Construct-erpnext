import frappe
from frappe import _


def execute(filters=None):
	filters = filters or {}
	columns = [
		{"label": _("Real Estate Project"), "fieldname": "real_estate_project", "fieldtype": "Link", "options": "Real Estate Project", "width": 180},
		{"label": _("ERPNext Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 150},
		{"label": _("Total Units"), "fieldname": "total_units", "fieldtype": "Int", "width": 100},
		{"label": _("Source Cost"), "fieldname": "source_cost", "fieldtype": "Currency", "width": 130},
		{"label": _("Total Allocated Cost"), "fieldname": "total_allocated_cost", "fieldtype": "Currency", "width": 160},
		{"label": _("Total Expected Sales Value"), "fieldname": "total_expected_sales_value", "fieldtype": "Currency", "width": 180},
		{"label": _("Expected Gross Margin"), "fieldname": "expected_gross_margin", "fieldtype": "Currency", "width": 160},
		{"label": _("Expected Margin %"), "fieldname": "expected_margin_percent", "fieldtype": "Percent", "width": 140},
		{"label": _("Profitable Units"), "fieldname": "profitable_units", "fieldtype": "Int", "width": 120},
		{"label": _("Watch Units"), "fieldname": "watch_units", "fieldtype": "Int", "width": 100},
		{"label": _("Loss Risk Units"), "fieldname": "loss_risk_units", "fieldtype": "Int", "width": 120},
		{"label": _("Not Priced Units"), "fieldname": "not_priced_units", "fieldtype": "Int", "width": 120},
	]
	condition = "WHERE rep.name = %(real_estate_project)s" if filters.get("real_estate_project") else ""
	data = frappe.db.sql(
		f"""
		SELECT rep.name AS real_estate_project, rep.project, COUNT(u.name) AS total_units,
			COALESCE(MAX(uca.source_amount), 0) AS source_cost,
			COALESCE(SUM(u.allocated_cost), 0) AS total_allocated_cost,
			COALESCE(SUM(u.expected_sale_price), 0) AS total_expected_sales_value,
			COALESCE(SUM(u.expected_margin), 0) AS expected_gross_margin,
			CASE WHEN COALESCE(SUM(u.expected_sale_price), 0) > 0
				THEN COALESCE(SUM(u.expected_margin), 0) / SUM(u.expected_sale_price) * 100
				ELSE 0 END AS expected_margin_percent,
			SUM(CASE WHEN u.profitability_status = 'Profitable' THEN 1 ELSE 0 END) AS profitable_units,
			SUM(CASE WHEN u.profitability_status = 'Watch' THEN 1 ELSE 0 END) AS watch_units,
			SUM(CASE WHEN u.profitability_status = 'Loss Risk' THEN 1 ELSE 0 END) AS loss_risk_units,
			SUM(CASE WHEN u.profitability_status = 'Not Priced' THEN 1 ELSE 0 END) AS not_priced_units
		FROM `tabReal Estate Project` rep
		LEFT JOIN `tabUnit` u ON u.real_estate_project = rep.name
		LEFT JOIN `tabUnit Cost Allocation` uca
			ON uca.name = u.latest_cost_allocation AND uca.allocation_status = 'Applied'
		{condition}
		GROUP BY rep.name
		ORDER BY rep.modified DESC
		""",
		{"real_estate_project": filters.get("real_estate_project")},
		as_dict=True,
	)
	return columns, data
