frappe.query_reports["Ownership Summary Report"] = {
	filters: [
		{fieldname: "real_estate_project", label: __("Real Estate Project"), fieldtype: "Link", options: "Real Estate Project"},
		{fieldname: "property_owner", label: __("Owner"), fieldtype: "Link", options: "Property Owner"},
		{fieldname: "unit", label: __("Unit"), fieldtype: "Link", options: "Unit"},
		{fieldname: "status", label: __("Status"), fieldtype: "Select", options: "\nActive\nTransferred\nEnded\nCancelled"}
	]
};
