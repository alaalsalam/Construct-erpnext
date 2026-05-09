frappe.query_reports["Unit Cost Allocation Report"] = {
	filters: [
		{fieldname: "real_estate_project", label: __("Real Estate Project"), fieldtype: "Link", options: "Real Estate Project"},
		{fieldname: "allocation_status", label: __("Allocation Status"), fieldtype: "Select", options: "\nDraft\nCalculated\nReviewed\nApplied\nCancelled"},
		{fieldname: "allocation_basis", label: __("Allocation Basis"), fieldtype: "Select", options: "\nBy Area\nEqual Share\nManual Percentage\nManual Amount"},
		{fieldname: "cost_source", label: __("Cost Source"), fieldtype: "Select", options: "\nBOQ Total\nCommitted Cost\nInvoiced Cost\nConsumed Cost\nCertified Cost\nFinancial Snapshot\nManual Amount"}
	]
};
