frappe.query_reports["Viewing Schedule Report"] = {
	filters: [
		{fieldname: "status", label: __("Status"), fieldtype: "Select", options: "\nScheduled\nCompleted\nCancelled\nNo Show"},
		{fieldname: "from_date", label: __("From Date"), fieldtype: "Date"},
		{fieldname: "to_date", label: __("To Date"), fieldtype: "Date"}
	]
};
