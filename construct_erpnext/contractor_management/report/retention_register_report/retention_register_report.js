frappe.query_reports["Retention Register Report"] = {
	filters: [
		{fieldname: "project", label: __("Project"), fieldtype: "Link", options: "Project"},
		{fieldname: "contractor", label: __("Contractor"), fieldtype: "Link", options: "Supplier"},
		{fieldname: "status", label: __("Status"), fieldtype: "Select", options: "\nHeld\nEligible for Release\nPartially Released\nReleased\nCancelled"},
		{fieldname: "from_date", label: __("From Date"), fieldtype: "Date"},
		{fieldname: "to_date", label: __("To Date"), fieldtype: "Date"}
	]
};
