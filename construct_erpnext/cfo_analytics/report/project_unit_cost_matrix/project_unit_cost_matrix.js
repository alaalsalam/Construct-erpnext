frappe.query_reports["Project Unit Cost Matrix"] = {
	filters: [
		{fieldname: "project", label: __("Project"), fieldtype: "Link", options: "Project"},
		{fieldname: "real_estate_project", label: __("Real Estate Project"), fieldtype: "Link", options: "Real Estate Project"},
		{fieldname: "cost_code", label: __("Cost Code"), fieldtype: "Link", options: "Cost Code"}
	]
};
