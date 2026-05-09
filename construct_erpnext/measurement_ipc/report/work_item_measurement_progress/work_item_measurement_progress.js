frappe.query_reports["Work Item Measurement Progress"] = {
	filters: [
		{ fieldname: "project", label: __("Project"), fieldtype: "Link", options: "Project" },
		{ fieldname: "construction_boq", label: __("Construction BOQ"), fieldtype: "Link", options: "Construction BOQ" },
		{ fieldname: "construction_work_item", label: __("Construction Work Item"), fieldtype: "Link", options: "Construction Work Item" },
		{ fieldname: "measurement_status", label: __("Measurement Status"), fieldtype: "Select", options: "\nNot Measured\nPartially Measured\nFully Measured\nOver Measured" },
		{ fieldname: "cost_code", label: __("Cost Code"), fieldtype: "Link", options: "Cost Code" },
		{ fieldname: "wbs_element", label: __("WBS Element"), fieldtype: "Link", options: "WBS Element" },
	],
};
