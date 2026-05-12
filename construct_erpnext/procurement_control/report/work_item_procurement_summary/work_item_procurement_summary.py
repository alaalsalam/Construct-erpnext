import frappe
from frappe import _
from construct_erpnext.reporting.report_utils import sum_field, summary_value, normalize_common_filters


def execute(filters=None):
	filters = normalize_common_filters(filters)
	data = get_data(filters)
	return get_columns(), data, None, None, None, False


def get_columns():
	return [
		{"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 140},
		{"label": _("BOQ"), "fieldname": "construction_boq", "fieldtype": "Link", "options": "Construction BOQ", "width": 150},
		{"label": _("Work Item"), "fieldname": "name", "fieldtype": "Link", "options": "Construction Work Item", "width": 160},
		{"label": _("WBS"), "fieldname": "wbs_element", "fieldtype": "Link", "options": "WBS Element", "width": 140},
		{"label": _("Cost Code"), "fieldname": "cost_code", "fieldtype": "Link", "options": "Cost Code", "width": 120},
		{"label": _("Item"), "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 120},
		{"label": _("Description"), "fieldname": "description", "fieldtype": "Data", "width": 220},
		{"label": _("Planned Qty"), "fieldname": "planned_quantity", "fieldtype": "Float", "width": 110},
		{"label": _("Requested Qty"), "fieldname": "requested_qty", "fieldtype": "Float", "width": 110},
		{"label": _("Ordered Qty"), "fieldname": "ordered_qty", "fieldtype": "Float", "width": 110},
		{"label": _("Received Qty"), "fieldname": "received_qty", "fieldtype": "Float", "width": 110},
		{"label": _("Invoiced Qty"), "fieldname": "invoiced_qty", "fieldtype": "Float", "width": 110},
		{"label": _("Consumed Qty"), "fieldname": "consumed_qty", "fieldtype": "Float", "width": 110},
		{"label": _("Remaining Qty"), "fieldname": "remaining_qty", "fieldtype": "Float", "width": 110},
		{"label": _("Planned Amount"), "fieldname": "planned_amount", "fieldtype": "Currency", "width": 130},
		{"label": _("Committed Amount"), "fieldname": "committed_amount", "fieldtype": "Currency", "width": 140},
		{"label": _("Invoiced Amount"), "fieldname": "invoiced_amount", "fieldtype": "Currency", "width": 130},
		{"label": _("Consumed Amount"), "fieldname": "consumed_amount", "fieldtype": "Currency", "width": 140},
		{"label": _("Procurement Status"), "fieldname": "procurement_status", "fieldtype": "Data", "width": 150},
	]


def get_data(filters):
	conditions = ["disabled = 0"]
	values = {}
	for fieldname in ("project", "construction_boq", "item_category", "procurement_status"):
		if filters.get(fieldname):
			conditions.append(f"{fieldname} = %({fieldname})s")
			values[fieldname] = filters.get(fieldname)
	if filters.get("construction_work_item"):
		conditions.append("name = %(construction_work_item)s")
		values["construction_work_item"] = filters.get("construction_work_item")

	return frappe.db.sql(
		"""
		SELECT
			project, construction_boq, name, wbs_element, cost_code, item_code, description,
			planned_quantity, requested_qty, ordered_qty, received_qty, invoiced_qty,
			consumed_qty, remaining_qty, planned_amount, committed_amount, invoiced_amount,
			consumed_amount, procurement_status
		FROM `tabConstruction Work Item`
		WHERE {conditions}
		ORDER BY project, construction_boq, name
		""".format(conditions=" AND ".join(conditions)),
		values,
		as_dict=True,
	)


def get_report_summary(data):
	return [
		summary_value("Requested Qty", sum_field(data, "requested_qty"), "Float", "Blue"),
		summary_value("Ordered Qty", sum_field(data, "ordered_qty"), "Float", "Blue"),
		summary_value("Received Qty", sum_field(data, "received_qty"), "Float", "Green"),
		summary_value("Invoiced Qty", sum_field(data, "invoiced_qty"), "Float", "Orange"),
		summary_value("Consumed Qty", sum_field(data, "consumed_qty"), "Float", "Blue"),
		summary_value("Remaining Qty", sum_field(data, "remaining_qty"), "Float", "Grey"),
	]
