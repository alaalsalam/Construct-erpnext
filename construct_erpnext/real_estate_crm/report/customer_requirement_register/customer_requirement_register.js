frappe.query_reports["Customer Requirement Register"] = {
	filters: [
		{fieldname: "preferred_project", label: __("Preferred Project"), fieldtype: "Link", options: "Real Estate Project"},
		{fieldname: "requirement_type", label: __("Requirement Type"), fieldtype: "Select", options: "\nBuy\nRent\nInvestment"},
		{fieldname: "status", label: __("Status"), fieldtype: "Select", options: "\nNew\nQualified\nMatched\nReserved\nWon\nLost\nBacklog"},
		{fieldname: "priority", label: __("Priority"), fieldtype: "Select", options: "\nLow\nMedium\nHigh\nUrgent"}
	]
};
