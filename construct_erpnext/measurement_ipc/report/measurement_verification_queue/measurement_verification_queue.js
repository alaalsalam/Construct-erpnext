frappe.query_reports["Measurement Verification Queue"] = {
	filters: [
		{ fieldname: "project", label: __("Project"), fieldtype: "Link", options: "Project" },
		{ fieldname: "contractor", label: __("Contractor"), fieldtype: "Link", options: "Supplier" },
		{ fieldname: "status", label: __("Status"), fieldtype: "Select", options: "\nDraft\nSubmitted\nVerified\nRejected\nLocked\nCancelled" },
		{ fieldname: "measured_by", label: __("Measured By"), fieldtype: "Link", options: "User" },
	],
};
