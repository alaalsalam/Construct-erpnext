frappe.query_reports["Construction BOQ Variance"] = {
	filters: [
		{
			fieldname: "project",
			label: __("Project"),
			fieldtype: "Link",
			options: "Project",
		},
		{
			fieldname: "status",
			label: __("Status"),
			fieldtype: "Select",
			options: "\nDraft\nUnder Review\nApproved\nLocked\nCancelled",
		},
	],
};
