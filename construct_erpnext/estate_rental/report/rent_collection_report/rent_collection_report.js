frappe.query_reports["Rent Collection Report"] = {
	filters: [
		{ fieldname: "company", label: __("Company"), fieldtype: "Link", options: "Company" },
		{ fieldname: "real_estate_project", label: __("Real Estate Project"), fieldtype: "Link", options: "Real Estate Project" },
		{ fieldname: "customer", label: __("Customer"), fieldtype: "Link", options: "Customer" },
		{ fieldname: "rent_collection_status", label: __("Rent Collection Status"), fieldtype: "Select", options: "\nNot Invoiced\nPartially Invoiced\nFully Invoiced\nPartially Collected\nFully Collected\nOverdue" },
		{ fieldname: "from_date", label: __("From Date"), fieldtype: "Date" },
		{ fieldname: "to_date", label: __("To Date"), fieldtype: "Date" },
	],
};
