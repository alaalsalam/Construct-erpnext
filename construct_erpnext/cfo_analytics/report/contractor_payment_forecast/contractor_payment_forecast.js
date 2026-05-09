frappe.query_reports["Contractor Payment Forecast"] = {
	filters: [
		{fieldname: "project", label: __("Project"), fieldtype: "Link", options: "Project"},
		{fieldname: "contractor", label: __("Contractor"), fieldtype: "Link", options: "Supplier"},
		{fieldname: "from_date", label: __("From Date"), fieldtype: "Date"},
		{fieldname: "to_date", label: __("To Date"), fieldtype: "Date"}
	]
};
