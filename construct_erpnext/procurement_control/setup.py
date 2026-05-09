import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


LINKED_CHILD_TABLES = (
	"Material Request Item",
	"Purchase Order Item",
	"Purchase Receipt Item",
	"Purchase Invoice Item",
	"Stock Entry Detail",
)


def after_migrate():
	create_procurement_custom_fields()


def create_procurement_custom_fields():
	custom_fields = {}
	for doctype in LINKED_CHILD_TABLES:
		insert_after = get_insert_after(doctype)
		custom_fields[doctype] = [
			link_field(
				"construction_work_item",
				"Construction Work Item",
				"Construction Work Item",
				insert_after,
			),
			link_field("construction_boq", "Construction BOQ", "Construction BOQ"),
			link_field("wbs_element", "WBS Element", "WBS Element"),
			link_field("cost_code", "Cost Code", "Cost Code"),
			link_field("site_warehouse", "Site Warehouse", "Warehouse"),
		]

	custom_fields["Warehouse"] = [
		{
			"fieldname": "is_site_warehouse",
			"label": "Is Site Warehouse",
			"fieldtype": "Check",
			"insert_after": "company",
		},
		link_field("construction_project", "Construction Project", "Project"),
		{
			"fieldname": "site_code",
			"label": "Site Code",
			"fieldtype": "Data",
		},
		link_field("site_manager", "Site Manager", "User"),
	]

	create_custom_fields(custom_fields, ignore_validate=True)


def get_insert_after(doctype):
	for fieldname in ("project", "cost_center", "warehouse", "item_code"):
		if frappe.get_meta(doctype).has_field(fieldname):
			return fieldname
	return None


def link_field(fieldname, label, options, insert_after=None):
	field = {
		"fieldname": fieldname,
		"label": label,
		"fieldtype": "Link",
		"options": options,
	}
	if insert_after:
		field["insert_after"] = insert_after
	return field
