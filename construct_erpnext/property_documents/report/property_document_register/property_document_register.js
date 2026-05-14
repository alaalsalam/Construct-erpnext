frappe.query_reports["Property Document Register"] = {
	filters: [
		{fieldname: "real_estate_project", label: __("Real Estate Project"), fieldtype: "Link", options: "Real Estate Project"},
		{fieldname: "document_type", label: __("Document Type"), fieldtype: "Select", options: "\nTitle Deed\nContract\nID\nDrawing\nLicense\nOther"}
	]
};
