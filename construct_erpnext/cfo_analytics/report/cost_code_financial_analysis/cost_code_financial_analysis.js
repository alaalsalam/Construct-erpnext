frappe.query_reports["Cost Code Financial Analysis"] = {
	filters: [
		{fieldname: "project", label: __("Project"), fieldtype: "Link", options: "Project"},
		{fieldname: "cost_code", label: __("Cost Code"), fieldtype: "Link", options: "Cost Code"},
		{fieldname: "unit", label: __("Unit"), fieldtype: "Link", options: "Unit"},
		{fieldname: "from_date", label: __("From Date"), fieldtype: "Date"},
		{fieldname: "to_date", label: __("To Date"), fieldtype: "Date"}
	]
};
