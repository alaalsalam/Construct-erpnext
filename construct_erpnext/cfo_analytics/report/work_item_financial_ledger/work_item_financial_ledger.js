frappe.query_reports["Work Item Financial Ledger"] = {
	filters: [
		{fieldname: "construction_work_item", label: __("Construction Work Item"), fieldtype: "Link", options: "Construction Work Item"},
		{fieldname: "project", label: __("Project"), fieldtype: "Link", options: "Project"},
		{fieldname: "from_date", label: __("From Date"), fieldtype: "Date"},
		{fieldname: "to_date", label: __("To Date"), fieldtype: "Date"}
	]
};
