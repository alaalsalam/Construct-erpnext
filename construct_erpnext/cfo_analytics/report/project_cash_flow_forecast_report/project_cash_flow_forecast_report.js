frappe.query_reports["Project Cash Flow Forecast Report"] = {
	filters: [
		{fieldname: "project", label: __("Project"), fieldtype: "Link", options: "Project"},
		{fieldname: "forecast", label: __("Forecast"), fieldtype: "Link", options: "Project Cash Flow Forecast"},
		{fieldname: "start_date", label: __("Start Date"), fieldtype: "Date"},
		{fieldname: "end_date", label: __("End Date"), fieldtype: "Date"},
		{fieldname: "period_type", label: __("Period Type"), fieldtype: "Select", options: "\nWeekly\nMonthly\nQuarterly"}
	]
};
