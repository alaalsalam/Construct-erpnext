frappe.query_reports["Advance Recovery Report"] = {
	filters: [
		{fieldname: "project", label: __("Project"), fieldtype: "Link", options: "Project"},
		{fieldname: "contractor", label: __("Contractor"), fieldtype: "Link", options: "Supplier"},
		{fieldname: "status", label: __("Status"), fieldtype: "Select", options: "\nActive\nFully Recovered\nCancelled"}
	]
};
