import frappe
from frappe import _
from frappe.utils import flt


UNIT_STATUSES = ("Available", "Reserved", "Sold", "Rented", "Blocked")


def recalculate_project_unit_counts(real_estate_project):
	if not real_estate_project:
		return
	counts = _get_unit_counts({"real_estate_project": real_estate_project})
	frappe.db.set_value(
		"Real Estate Project",
		real_estate_project,
		{
			"total_units": counts.get("total_units"),
			"available_units": counts.get("available_units"),
			"reserved_units": counts.get("reserved_units"),
			"sold_units": counts.get("sold_units"),
			"rented_units": counts.get("rented_units"),
			"blocked_units": counts.get("blocked_units"),
		},
		update_modified=False,
	)


def recalculate_building_unit_counts(building):
	if not building:
		return
	counts = _get_unit_counts({"building": building})
	frappe.db.set_value(
		"Building",
		building,
		{"total_units": counts.get("total_units")},
		update_modified=False,
	)


def recalculate_floor_unit_counts(floor):
	if not floor:
		return
	counts = _get_unit_counts({"floor": floor})
	frappe.db.set_value(
		"Floor",
		floor,
		{"total_units": counts.get("total_units")},
		update_modified=False,
	)


def sync_unit_status(unit):
	if unit.status in UNIT_STATUSES:
		unit.marketing_status = unit.status
	elif unit.marketing_status in UNIT_STATUSES and unit.status in (
		None,
		"",
		"Under Construction",
		"Under Maintenance",
	):
		unit.status = unit.marketing_status
	elif not unit.marketing_status:
		unit.marketing_status = "Available"


def validate_ownership_percentages(unit, current_doc=None):
	if not unit:
		return
	total = frappe.db.sql(
		"""
		SELECT COALESCE(SUM(ownership_percentage), 0)
		FROM `tabProperty Ownership`
		WHERE unit = %(unit)s
			AND status = 'Active'
			AND name != %(name)s
		""",
		{"unit": unit, "name": current_doc.name if current_doc else ""},
	)[0][0]
	total = flt(total) + (
		flt(current_doc.ownership_percentage)
		if current_doc and current_doc.status == "Active"
		else 0
	)
	if total > 100:
		frappe.throw(_("Total active ownership percentage for this Unit cannot exceed 100%."))
	if total < 100:
		frappe.msgprint(
			_("Active ownership percentage for this Unit is {0}%.").format(total),
			alert=True,
		)


def update_related_counts(real_estate_project=None, building=None, floor=None):
	recalculate_project_unit_counts(real_estate_project)
	recalculate_building_unit_counts(building)
	recalculate_floor_unit_counts(floor)


def create_default_inventory_for_project(project):
	# Optional helper for guided implementation setup. It is never called automatically.
	return frappe.get_doc("Project", project).name


def _get_unit_counts(filters):
	conditions = []
	values = {}
	for field, value in filters.items():
		if value:
			conditions.append(f"{field} = %({field})s")
			values[field] = value
	where_clause = " AND ".join(conditions) if conditions else "1=1"
	row = frappe.db.sql(
		f"""
		SELECT
			COUNT(*) AS total_units,
			SUM(CASE WHEN status = 'Available' THEN 1 ELSE 0 END) AS available_units,
			SUM(CASE WHEN status = 'Reserved' THEN 1 ELSE 0 END) AS reserved_units,
			SUM(CASE WHEN status = 'Sold' THEN 1 ELSE 0 END) AS sold_units,
			SUM(CASE WHEN status = 'Rented' THEN 1 ELSE 0 END) AS rented_units,
			SUM(CASE WHEN status = 'Blocked' THEN 1 ELSE 0 END) AS blocked_units
		FROM `tabUnit`
		WHERE {where_clause}
		""",
		values,
		as_dict=True,
	)[0]
	return {key: flt(value) for key, value in row.items()}
