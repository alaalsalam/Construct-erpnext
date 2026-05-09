frappe.query_reports["Real Estate Project Summary"] = {
	filters: [
		{fieldname: "real_estate_project", label: __("Real Estate Project"), fieldtype: "Link", options: "Real Estate Project"},
		{fieldname: "status", label: __("Status"), fieldtype: "Select", options: "\nPlanning\nUnder Construction\nReady for Sale\nReady for Rent\nOperating\nClosed"}
	]
};
