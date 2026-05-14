frappe.query_reports["Follow Up Report"] = {
	filters: [
		{fieldname: "channel", label: __("Channel"), fieldtype: "Select", options: "\nCall\nEmail\nVisit\nMessage\nOther"},
		{fieldname: "result", label: __("Result"), fieldtype: "Select", options: "\nInterested\nNeeds More Options\nScheduled Viewing\nReserved\nNot Interested\nNo Response"},
		{fieldname: "from_date", label: __("From Date"), fieldtype: "Date"},
		{fieldname: "to_date", label: __("To Date"), fieldtype: "Date"}
	]
};
