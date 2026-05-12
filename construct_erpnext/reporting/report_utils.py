import frappe
from frappe import _
from frappe.utils import flt


def resolve_project_filter(value):
	if not value:
		return value

	if frappe.db.exists("Project", value):
		return value

	project = frappe.db.get_value("Project", {"project_name": value}, "name")
	return project or value


def normalize_common_filters(filters):
	filters = frappe._dict(filters or {})
	if filters.get("project"):
		filters.project = resolve_project_filter(filters.project)
	return filters


def sum_field(rows, fieldname):
	return sum(flt(row.get(fieldname)) for row in rows or [])


def count_where(rows, fieldname, values):
	if isinstance(values, str):
		values = {values}
	else:
		values = set(values or [])
	return sum(1 for row in rows or [] if row.get(fieldname) in values)


def summary_value(label, value, datatype="Currency", indicator="Blue"):
	return {
		"label": _(label),
		"value": flt(value) if datatype in ("Currency", "Float", "Percent") else value,
		"datatype": datatype,
		"indicator": indicator,
	}
