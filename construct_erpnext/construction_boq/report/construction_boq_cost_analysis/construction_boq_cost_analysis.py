import frappe
from frappe import _
from construct_erpnext.reporting.report_utils import normalize_common_filters


def execute(filters=None):
	filters = normalize_common_filters(filters)
	return get_columns(), get_data(filters)


def get_columns():
	return [
		{"label": _("BOQ"), "fieldname": "construction_boq", "fieldtype": "Link", "options": "Construction BOQ", "width": 160},
		{"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 160},
		{"label": _("WBS Code"), "fieldname": "wbs_code", "fieldtype": "Data", "width": 120},
		{"label": _("Cost Code"), "fieldname": "cost_code", "fieldtype": "Link", "options": "Cost Code", "width": 140},
		{"label": _("Description"), "fieldname": "description", "fieldtype": "Data", "width": 260},
		{"label": _("Category"), "fieldname": "item_category", "fieldtype": "Data", "width": 120},
		{"label": _("Quantity"), "fieldname": "quantity", "fieldtype": "Float", "width": 100},
		{"label": _("UOM"), "fieldname": "uom", "fieldtype": "Link", "options": "UOM", "width": 90},
		{"label": _("Unit Rate"), "fieldname": "unit_rate", "fieldtype": "Currency", "width": 120},
		{"label": _("Amount"), "fieldname": "amount", "fieldtype": "Currency", "width": 120},
		{"label": _("Final Amount"), "fieldname": "final_amount", "fieldtype": "Currency", "width": 130},
	]


def get_data(filters):
	conditions = ["boq.docstatus < 2"]
	values = {}

	if filters.get("project"):
		conditions.append("boq.project = %(project)s")
		values["project"] = filters.get("project")
	if filters.get("construction_boq"):
		conditions.append("boq.name = %(construction_boq)s")
		values["construction_boq"] = filters.get("construction_boq")
	if filters.get("item_category"):
		conditions.append("item.item_category = %(item_category)s")
		values["item_category"] = filters.get("item_category")
	if filters.get("cost_code"):
		conditions.append("item.cost_code = %(cost_code)s")
		values["cost_code"] = filters.get("cost_code")

	return frappe.db.sql(
		"""
		SELECT
			boq.name AS construction_boq,
			boq.project,
			item.wbs_code,
			item.cost_code,
			item.description,
			item.item_category,
			item.quantity,
			item.uom,
			item.unit_rate,
			item.amount,
			item.final_amount
		FROM `tabConstruction BOQ Item` item
		INNER JOIN `tabConstruction BOQ` boq ON boq.name = item.parent
		WHERE {conditions}
		ORDER BY boq.project, boq.name, item.idx
		""".format(conditions=" AND ".join(conditions)),
		values,
		as_dict=True,
	)
