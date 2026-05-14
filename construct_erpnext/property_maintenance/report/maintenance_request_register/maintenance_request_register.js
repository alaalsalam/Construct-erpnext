frappe.query_reports["Maintenance Request Register"] = {
	filters: [
		{fieldname: "real_estate_project", label: __("Real Estate Project"), fieldtype: "Link", options: "Real Estate Project"},
		{fieldname: "status", label: __("Status"), fieldtype: "Select", options: "\nNew\nUnder Review\nApproved\nIn Progress\nCompleted\nCancelled"}
	]
};
