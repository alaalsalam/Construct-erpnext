import json

import frappe
from frappe import _

from construct_erpnext.procurement_control.work_item_sync import get_work_item_material_request_qty


@frappe.whitelist()
def create_material_request_from_work_items(
	project, work_items, required_by, target_warehouse=None
):
	if isinstance(work_items, str):
		work_items = json.loads(work_items)

	if not work_items:
		frappe.throw(_("At least one Construction Work Item is required."))

	material_request = frappe.new_doc("Material Request")
	material_request.material_request_type = "Purchase"
	material_request.schedule_date = required_by
	material_request.company = frappe.db.get_value("Project", project, "company")
	if target_warehouse:
		material_request.set_warehouse = target_warehouse

	for work_item_name in work_items:
		work_item = frappe.get_doc("Construction Work Item", work_item_name)
		if work_item.project != project:
			frappe.throw(
				_("Construction Work Item {0} does not belong to Project {1}.").format(
					work_item.name, project
				)
			)
		if work_item.item_category != "Material" or not work_item.item_code:
			continue

		qty = get_work_item_material_request_qty(work_item)
		if qty <= 0:
			continue

		material_request.append(
			"items",
			{
				"item_code": work_item.item_code,
				"schedule_date": required_by,
				"qty": qty,
				"uom": work_item.uom,
				"warehouse": target_warehouse,
				"project": work_item.project,
				"cost_center": work_item.cost_center,
				"construction_work_item": work_item.name,
				"construction_boq": work_item.construction_boq,
				"wbs_element": work_item.wbs_element,
				"cost_code": work_item.cost_code,
				"site_warehouse": target_warehouse,
			},
		)

	if not material_request.items:
		frappe.throw(_("No requestable material Work Items were found."))

	material_request.insert()
	return material_request.name
