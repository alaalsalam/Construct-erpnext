frappe.query_reports["Backlog Request Register"] = {
	filters: [
		{fieldname: "status", label: __("Status"), fieldtype: "Select", options: "\nActive\nMatched\nClosed\nCancelled"},
		{fieldname: "reason", label: __("Reason"), fieldtype: "Select", options: "\nNo Match\nBudget Gap\nArea Gap\nType Gap"}
	]
};
