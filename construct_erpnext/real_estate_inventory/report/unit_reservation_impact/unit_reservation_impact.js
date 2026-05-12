frappe.query_reports["Unit Reservation Impact"] = {
	filters: [
		{fieldname: "real_estate_project", label: __("Real Estate Project"), fieldtype: "Link", options: "Real Estate Project"},
		{fieldname: "building", label: __("Building"), fieldtype: "Link", options: "Building"}
	]
};
