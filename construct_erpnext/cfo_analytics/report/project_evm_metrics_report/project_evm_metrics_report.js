frappe.query_reports["Project EVM Metrics Report"] = {
	filters: [
		{fieldname: "project", label: __("Project"), fieldtype: "Link", options: "Project"},
		{fieldname: "calculation_date", label: __("Calculation Date"), fieldtype: "Date"},
		{fieldname: "status", label: __("Status"), fieldtype: "Select", options: "\nDraft\nCalculated\nReviewed\nArchived"}
	]
};
