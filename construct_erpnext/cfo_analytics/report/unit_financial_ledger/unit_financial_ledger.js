frappe.query_reports["Unit Financial Ledger"] = {
	filters: [
		{fieldname: "unit", label: __("Unit"), fieldtype: "Link", options: "Unit"},
		{fieldname: "project", label: __("Project"), fieldtype: "Link", options: "Project"},
		{fieldname: "from_date", label: __("From Date"), fieldtype: "Date"},
		{fieldname: "to_date", label: __("To Date"), fieldtype: "Date"}
	]
};
