import frappe
from frappe import _
from construct_erpnext.reporting.report_utils import count_where, sum_field, summary_value


def execute(filters=None):
	filters = filters or {}
	columns = [
		{"label": _("Unit"), "fieldname": "unit", "fieldtype": "Link", "options": "Unit", "width": 120},
		{"label": _("Project"), "fieldname": "real_estate_project", "fieldtype": "Link", "options": "Real Estate Project", "width": 170},
		{"label": _("Building"), "fieldname": "building", "fieldtype": "Link", "options": "Building", "width": 120},
		{"label": _("Floor"), "fieldname": "floor", "fieldtype": "Link", "options": "Floor", "width": 120},
		{"label": _("Unit Type"), "fieldname": "unit_type", "fieldtype": "Link", "options": "Unit Type", "width": 120},
		{"label": _("Area"), "fieldname": "area", "fieldtype": "Float", "width": 80},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
		{"label": _("Allocated Cost"), "fieldname": "allocated_cost", "fieldtype": "Currency", "width": 130},
		{"label": _("Expected Sale Price"), "fieldname": "expected_sale_price", "fieldtype": "Currency", "width": 150},
		{"label": _("Expected Monthly Rent"), "fieldname": "expected_monthly_rent", "fieldtype": "Currency", "width": 150},
		{"label": _("Expected Margin"), "fieldname": "expected_margin", "fieldtype": "Currency", "width": 130},
		{"label": _("Margin %"), "fieldname": "expected_margin_percent", "fieldtype": "Percent", "width": 100},
		{"label": _("Profitability Status"), "fieldname": "profitability_status", "fieldtype": "Data", "width": 140},
	]
	conditions = ["1=1"]
	values = {}
	for field in ("real_estate_project", "building", "floor", "unit_type", "profitability_status"):
		if filters.get(field):
			conditions.append(f"{field} = %({field})s")
			values[field] = filters[field]
	if filters.get("unit_status"):
		conditions.append("status = %(unit_status)s")
		values["unit_status"] = filters["unit_status"]
	data = frappe.db.sql(
		f"""
		SELECT name AS unit, real_estate_project, building, floor, unit_type, area,
			status, allocated_cost, expected_sale_price, expected_monthly_rent,
			expected_margin, expected_margin_percent, profitability_status
		FROM `tabUnit`
		WHERE {" AND ".join(conditions)}
		ORDER BY building, floor, unit_code
		""",
		values,
		as_dict=True,
	)
	return columns, data, None, None, get_report_summary(data), False


def get_report_summary(data):
	return [
		summary_value("Total Units", len(data or []), "Int", "Blue"),
		summary_value("Expected Sales Value", sum_field(data, "expected_sale_price"), "Currency", "Green"),
		summary_value("Allocated Cost", sum_field(data, "allocated_cost"), "Currency", "Orange"),
		summary_value("Expected Gross Margin", sum_field(data, "expected_margin"), "Currency", "Green"),
		summary_value("Profitable Units", count_where(data, "profitability_status", "Profitable"), "Int", "Green"),
		summary_value("Watch Units", count_where(data, "profitability_status", "Watch"), "Int", "Orange"),
		summary_value("Loss Risk Units", count_where(data, "profitability_status", "Loss Risk"), "Int", "Red"),
	]
