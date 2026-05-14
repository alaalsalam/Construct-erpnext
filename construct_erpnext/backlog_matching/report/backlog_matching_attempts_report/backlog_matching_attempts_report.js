frappe.query_reports["Backlog Matching Attempts Report"] = {
	filters: [
		{fieldname: "backlog_request", label: __("Backlog Request"), fieldtype: "Link", options: "Backlog Request"},
		{fieldname: "result", label: __("Result"), fieldtype: "Select", options: "\nNo Match\nMatched\nBelow Threshold"}
	]
};
