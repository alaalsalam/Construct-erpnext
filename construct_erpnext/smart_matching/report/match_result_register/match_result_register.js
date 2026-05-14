frappe.query_reports["Match Result Register"] = {
	filters: [
		{fieldname: "customer_requirement", label: __("Customer Requirement"), fieldtype: "Link", options: "Customer Requirement"},
		{fieldname: "status", label: __("Status"), fieldtype: "Select", options: "\nOpen\nReviewed\nConverted\nNo Suitable Match\nClosed"}
	]
};
