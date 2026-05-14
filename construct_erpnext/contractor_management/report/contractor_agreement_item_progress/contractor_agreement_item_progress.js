frappe.query_reports["Contractor Agreement Item Progress"] = {
	filters: [
		{ fieldname: "project", label: __("Project"), fieldtype: "Link", options: "Project" },
		{ fieldname: "contractor", label: __("Contractor"), fieldtype: "Link", options: "Supplier" },
		{ fieldname: "contractor_agreement", label: __("Contractor Agreement"), fieldtype: "Link", options: "Subcontract" },
		{ fieldname: "cost_code", label: __("Cost Code"), fieldtype: "Link", options: "Cost Code" },
		{ fieldname: "wbs_element", label: __("WBS Element"), fieldtype: "Link", options: "WBS Element" },
		{ fieldname: "item_status", label: __("Status"), fieldtype: "Select", options: "\nPlanned\nIn Progress\nPartially Measured\nPartially Certified\nFully Certified\nOverrun\nClosed" },
	],
};
