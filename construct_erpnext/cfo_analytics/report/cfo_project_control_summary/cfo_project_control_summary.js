frappe.query_reports["CFO Project Control Summary"] = {
	filters: [
		{fieldname: "project", label: __("Project"), fieldtype: "Link", options: "Project"},
		{fieldname: "risk_status", label: __("Risk Status"), fieldtype: "Select", options: "\nGreen\nYellow\nRed"}
	]
};
