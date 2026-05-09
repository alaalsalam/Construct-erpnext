frappe.query_reports["Unit Availability Report"] = {
	filters: [
		{fieldname: "real_estate_project", label: __("Real Estate Project"), fieldtype: "Link", options: "Real Estate Project"},
		{fieldname: "building", label: __("Building"), fieldtype: "Link", options: "Building"},
		{fieldname: "status", label: __("Status"), fieldtype: "Select", options: "\nAvailable\nReserved\nSold\nRented\nBlocked"},
		{fieldname: "usage_purpose", label: __("Usage Purpose"), fieldtype: "Select", options: "\nSale\nLong Term Rent\nShort Term Rent\nInvestment\nDevelopment\nMixed"}
	]
};
