frappe.query_reports["EVM Forecast Summary"] = {
	filters: [
		{fieldname: "project", label: __("Project"), fieldtype: "Link", options: "Project"},
		{fieldname: "from_date", label: __("From Date"), fieldtype: "Date"},
		{fieldname: "to_date", label: __("To Date"), fieldtype: "Date"},
		{fieldname: "overall_status", label: __("Overall Status"), fieldtype: "Select", options: "\nOn Track\nWatch\nAt Risk"}
	]
};
