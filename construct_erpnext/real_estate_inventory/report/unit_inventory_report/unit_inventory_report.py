import frappe
from frappe import _


def execute(filters=None):
	filters = filters or {}
	columns = [
		{"label": _("Unit"), "fieldname": "unit", "fieldtype": "Link", "options": "Unit", "width": 120},
		{"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Real Estate Project", "width": 170},
		{"label": _("Building"), "fieldname": "building", "fieldtype": "Link", "options": "Building", "width": 130},
		{"label": _("Floor"), "fieldname": "floor", "fieldtype": "Link", "options": "Floor", "width": 130},
		{"label": _("Unit Type"), "fieldname": "unit_type", "fieldtype": "Link", "options": "Unit Type", "width": 120},
		{"label": _("Area"), "fieldname": "area", "fieldtype": "Float", "width": 90},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 110},
		{"label": _("Usage Purpose"), "fieldname": "usage_purpose", "fieldtype": "Data", "width": 130},
		{"label": _("Expected Sale Price"), "fieldname": "expected_sale_price", "fieldtype": "Currency", "width": 150},
		{"label": _("Expected Rent"), "fieldname": "expected_monthly_rent", "fieldtype": "Currency", "width": 130},
		{"label": _("Allocated Cost"), "fieldname": "allocated_cost", "fieldtype": "Currency", "width": 130},
		{"label": _("Expected Margin %"), "fieldname": "expected_margin_percent", "fieldtype": "Percent", "width": 140},
	]
	conditions, values = _get_conditions(filters, ["real_estate_project", "building", "floor", "status", "unit_type", "usage_purpose", "property_nature"])
	data = frappe.db.sql(
		f"""
		SELECT name AS unit, real_estate_project AS project, building, floor, unit_type,
			area, status, usage_purpose, expected_sale_price, expected_monthly_rent,
			allocated_cost, expected_margin_percent
		FROM `tabUnit`
		WHERE {conditions}
		ORDER BY real_estate_project, building, floor, unit_code
		""",
		values,
		as_dict=True,
	)
	return columns, data


def _get_conditions(filters, fields):
	conditions = ["1=1"]
	values = {}
	for field in fields:
		if filters.get(field):
			conditions.append(f"{field} = %({field})s")
			values[field] = filters[field]
	return " AND ".join(conditions), values
