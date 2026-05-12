frappe.query_reports["Project Financial Snapshot Report"] = {
	filters: [
		{fieldname: "project", label: __("Project"), fieldtype: "Link", options: "Project"},
		{fieldname: "snapshot_date", label: __("Snapshot Date"), fieldtype: "Date"}
	]
};
