frappe.query_reports["BOQ Procurement Pipeline"] = {
	filters: [
		{ fieldname: "project", label: __("Project"), fieldtype: "Link", options: "Project" },
		{ fieldname: "construction_boq", label: __("Construction BOQ"), fieldtype: "Link", options: "Construction BOQ" },
		{ fieldname: "item_category", label: __("Item Category"), fieldtype: "Select", options: "\nMaterial\nLabor\nEquipment\nSubcontract\nOverhead\nContingency\nOther" },
		{ fieldname: "supplier", label: __("Supplier"), fieldtype: "Link", options: "Supplier" },
	],
};
