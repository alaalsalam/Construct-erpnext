frappe.query_reports["Sales Pipeline by Requirement"] = {
	filters: [
		{fieldname: "preferred_project", label: __("Preferred Project"), fieldtype: "Link", options: "Real Estate Project"},
		{fieldname: "requirement_type", label: __("Requirement Type"), fieldtype: "Select", options: "\nBuy\nRent\nInvestment"}
	]
};
