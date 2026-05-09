import frappe
from frappe import _


def execute(filters=None):
	filters = filters or {}
	columns = [
		{"label": _("Building"), "fieldname": "building", "fieldtype": "Link", "options": "Building", "width": 140},
		{"label": _("Units"), "fieldname": "units", "fieldtype": "Int", "width": 90},
		{"label": _("Total Area"), "fieldname": "total_area", "fieldtype": "Float", "width": 110},
		{"label": _("Allocated Cost"), "fieldname": "allocated_cost", "fieldtype": "Currency", "width": 130},
		{"label": _("Expected Sales Value"), "fieldname": "expected_sales_value", "fieldtype": "Currency", "width": 160},
		{"label": _("Expected Margin"), "fieldname": "expected_margin", "fieldtype": "Currency", "width": 140},
		{"label": _("Margin %"), "fieldname": "margin_percent", "fieldtype": "Percent", "width": 100},
		{"label": _("Profitability Status"), "fieldname": "profitability_status", "fieldtype": "Data", "width": 140},
	]
	conditions = ["1=1"]
	values = {}
	for field in ("real_estate_project", "building"):
		if filters.get(field):
			conditions.append(f"{field} = %({field})s")
			values[field] = filters[field]
	data = frappe.db.sql(
		f"""
		SELECT building, COUNT(*) AS units, COALESCE(SUM(area), 0) AS total_area,
			COALESCE(SUM(allocated_cost), 0) AS allocated_cost,
			COALESCE(SUM(expected_sale_price), 0) AS expected_sales_value,
			COALESCE(SUM(expected_margin), 0) AS expected_margin,
			CASE WHEN COALESCE(SUM(expected_sale_price), 0) > 0
				THEN COALESCE(SUM(expected_margin), 0) / SUM(expected_sale_price) * 100
				ELSE 0 END AS margin_percent
		FROM `tabUnit`
		WHERE {" AND ".join(conditions)}
		GROUP BY building
		ORDER BY building
		""",
		values,
		as_dict=True,
	)
	for row in data:
		if row.margin_percent >= 20:
			row.profitability_status = "Profitable"
		elif row.margin_percent >= 0:
			row.profitability_status = "Watch"
		else:
			row.profitability_status = "Loss Risk"
	return columns, data
