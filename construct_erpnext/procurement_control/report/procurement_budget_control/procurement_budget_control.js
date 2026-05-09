frappe.query_reports["Procurement Budget Control"] = {
	filters: [
		{ fieldname: "project", label: __("Project"), fieldtype: "Link", options: "Project" },
		{ fieldname: "construction_boq", label: __("Construction BOQ"), fieldtype: "Link", options: "Construction BOQ" },
		{ fieldname: "overrun_only", label: __("Overrun Only"), fieldtype: "Check" },
	],
};
