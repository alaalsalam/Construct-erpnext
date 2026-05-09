frappe.query_reports["Construction BOQ Cost Analysis"] = {
	filters: [
		{
			fieldname: "project",
			label: __("Project"),
			fieldtype: "Link",
			options: "Project",
		},
		{
			fieldname: "construction_boq",
			label: __("Construction BOQ"),
			fieldtype: "Link",
			options: "Construction BOQ",
		},
		{
			fieldname: "item_category",
			label: __("Item Category"),
			fieldtype: "Select",
			options: "\nMaterial\nLabor\nEquipment\nSubcontract\nOverhead\nContingency\nOther",
		},
		{
			fieldname: "cost_code",
			label: __("Cost Code"),
			fieldtype: "Link",
			options: "Cost Code",
		},
	],
};
