frappe.query_reports["Guarantee Register Report"] = {
	filters: [
		{fieldname: "project", label: __("Project"), fieldtype: "Link", options: "Project"},
		{fieldname: "contractor", label: __("Contractor"), fieldtype: "Link", options: "Supplier"},
		{fieldname: "status", label: __("Status"), fieldtype: "Select", options: "\nActive\nExpiring Soon\nExpired\nReleased\nEncashment Requested\nEncashment Completed\nCancelled"},
		{fieldname: "expiry_from", label: __("Expiry From"), fieldtype: "Date"},
		{fieldname: "expiry_to", label: __("Expiry To"), fieldtype: "Date"}
	]
};
