import frappe
from frappe import _
from construct_erpnext.reporting.report_utils import normalize_common_filters


def execute(filters=None):
	filters = normalize_common_filters(filters)
	return get_columns(), get_data(filters)


def get_columns():
	return [
		{"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 150},
		{"label": _("BOQ"), "fieldname": "construction_boq", "fieldtype": "Link", "options": "Construction BOQ", "width": 160},
		{"label": _("Work Item"), "fieldname": "name", "fieldtype": "Link", "options": "Construction Work Item", "width": 170},
		{"label": _("Planned Qty"), "fieldname": "planned_quantity", "fieldtype": "Float", "width": 110},
		{"label": _("Requested Qty"), "fieldname": "requested_qty", "fieldtype": "Float", "width": 110},
		{"label": _("Ordered Qty"), "fieldname": "ordered_qty", "fieldtype": "Float", "width": 110},
		{"label": _("Received Qty"), "fieldname": "received_qty", "fieldtype": "Float", "width": 110},
		{"label": _("Invoiced Qty"), "fieldname": "invoiced_qty", "fieldtype": "Float", "width": 110},
		{"label": _("Pipeline Gap"), "fieldname": "pipeline_gap", "fieldtype": "Float", "width": 110},
		{"label": _("Status"), "fieldname": "procurement_status", "fieldtype": "Data", "width": 150},
	]


def get_data(filters):
	conditions = ["wi.disabled = 0"]
	values = {}
	for fieldname in ("project", "construction_boq", "item_category"):
		if filters.get(fieldname):
			conditions.append(f"wi.{fieldname} = %({fieldname})s")
			values[fieldname] = filters.get(fieldname)
	if filters.get("supplier"):
		conditions.append(
			"""EXISTS (
				SELECT 1
				FROM `tabPurchase Order Item` poi
				INNER JOIN `tabPurchase Order` po ON po.name = poi.parent
				WHERE poi.construction_work_item = wi.name
					AND po.docstatus = 1
					AND po.supplier = %(supplier)s
			)"""
		)
		values["supplier"] = filters.get("supplier")

	return frappe.db.sql(
		"""
		SELECT
			wi.project, wi.construction_boq, wi.name, wi.planned_quantity,
			wi.requested_qty, wi.ordered_qty, wi.received_qty, wi.invoiced_qty,
			(wi.planned_quantity - wi.received_qty) AS pipeline_gap,
			wi.procurement_status
		FROM `tabConstruction Work Item` wi
		WHERE {conditions}
		ORDER BY wi.project, wi.construction_boq, wi.name
		""".format(conditions=" AND ".join(conditions)),
		values,
		as_dict=True,
	)
