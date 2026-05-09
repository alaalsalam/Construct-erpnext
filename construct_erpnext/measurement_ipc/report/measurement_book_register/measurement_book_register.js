frappe.query_reports["Measurement Book Register"] = {
	filters: [
		{ fieldname: "project", label: __("Project"), fieldtype: "Link", options: "Project" },
		{ fieldname: "contractor", label: __("Contractor"), fieldtype: "Link", options: "Supplier" },
		{ fieldname: "status", label: __("Status"), fieldtype: "Select", options: "\nDraft\nSubmitted\nUnder Verification\nVerified\nLocked\nCancelled" },
		{ fieldname: "from_date", label: __("From Date"), fieldtype: "Date" },
		{ fieldname: "to_date", label: __("To Date"), fieldtype: "Date" },
	],
};
