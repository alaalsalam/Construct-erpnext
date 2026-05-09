frappe.query_reports["Unit Inventory Report"] = {
	filters: [
		{fieldname: "real_estate_project", label: __("Real Estate Project"), fieldtype: "Link", options: "Real Estate Project"},
		{fieldname: "building", label: __("Building"), fieldtype: "Link", options: "Building"},
		{fieldname: "floor", label: __("Floor"), fieldtype: "Link", options: "Floor"},
		{fieldname: "status", label: __("Status"), fieldtype: "Select", options: "\nAvailable\nReserved\nSold\nRented\nBlocked\nUnder Maintenance\nUnder Construction"},
		{fieldname: "unit_type", label: __("Unit Type"), fieldtype: "Link", options: "Unit Type"},
		{fieldname: "usage_purpose", label: __("Usage Purpose"), fieldtype: "Select", options: "\nSale\nLong Term Rent\nShort Term Rent\nInvestment\nDevelopment\nMixed"},
		{fieldname: "property_nature", label: __("Property Nature"), fieldtype: "Select", options: "\nResidential\nCommercial\nIndustrial\nLand\nHospitality\nSpecial"}
	]
};
