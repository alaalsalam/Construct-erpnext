import frappe
from frappe import _
from construct_erpnext.reporting.report_utils import normalize_common_filters


def execute(filters=None):
	filters = normalize_common_filters(filters)
	return get_columns(), get_data(filters)


def get_columns():
	return [
		{"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 150},
		{"label": _("Site Warehouse"), "fieldname": "site_warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 170},
		{"label": _("Work Item"), "fieldname": "construction_work_item", "fieldtype": "Link", "options": "Construction Work Item", "width": 170},
		{"label": _("Item"), "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 130},
		{"label": _("Stock Entry"), "fieldname": "stock_entry", "fieldtype": "Link", "options": "Stock Entry", "width": 170},
		{"label": _("Posting Date"), "fieldname": "posting_date", "fieldtype": "Date", "width": 110},
		{"label": _("Qty"), "fieldname": "qty", "fieldtype": "Float", "width": 100},
		{"label": _("Amount"), "fieldname": "amount", "fieldtype": "Currency", "width": 120},
		{"label": _("Cost Code"), "fieldname": "cost_code", "fieldtype": "Link", "options": "Cost Code", "width": 130},
		{"label": _("WBS"), "fieldname": "wbs_element", "fieldtype": "Link", "options": "WBS Element", "width": 130},
	]


def get_data(filters):
	conditions = ["se.docstatus = 1", "IFNULL(sed.construction_work_item, '') != ''", "IFNULL(sed.s_warehouse, '') != ''"]
	values = {}
	if filters.get("project"):
		conditions.append("sed.project = %(project)s")
		values["project"] = filters.get("project")
	if filters.get("site_warehouse"):
		conditions.append("(sed.site_warehouse = %(site_warehouse)s OR sed.s_warehouse = %(site_warehouse)s)")
		values["site_warehouse"] = filters.get("site_warehouse")
	if filters.get("construction_work_item"):
		conditions.append("sed.construction_work_item = %(construction_work_item)s")
		values["construction_work_item"] = filters.get("construction_work_item")
	if filters.get("item_code"):
		conditions.append("sed.item_code = %(item_code)s")
		values["item_code"] = filters.get("item_code")
	if filters.get("from_date"):
		conditions.append("se.posting_date >= %(from_date)s")
		values["from_date"] = filters.get("from_date")
	if filters.get("to_date"):
		conditions.append("se.posting_date <= %(to_date)s")
		values["to_date"] = filters.get("to_date")

	return frappe.db.sql(
		"""
		SELECT
			sed.project,
			COALESCE(NULLIF(sed.site_warehouse, ''), sed.s_warehouse) AS site_warehouse,
			sed.construction_work_item,
			sed.item_code,
			se.name AS stock_entry,
			se.posting_date,
			sed.qty,
			sed.amount,
			sed.cost_code,
			sed.wbs_element
		FROM `tabStock Entry Detail` sed
		INNER JOIN `tabStock Entry` se ON se.name = sed.parent
		WHERE {conditions}
		ORDER BY se.posting_date DESC, se.name
		""".format(conditions=" AND ".join(conditions)),
		values,
		as_dict=True,
	)
