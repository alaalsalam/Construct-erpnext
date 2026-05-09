frappe.query_reports["Building Profitability Summary"] = {
	filters: [
		{fieldname: "real_estate_project", label: __("Real Estate Project"), fieldtype: "Link", options: "Real Estate Project"},
		{fieldname: "building", label: __("Building"), fieldtype: "Link", options: "Building"}
	]
};
