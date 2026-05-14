frappe.query_reports["Unit Rental Revenue Report"] = {
	filters: [
		{ fieldname: "real_estate_project", label: __("Real Estate Project"), fieldtype: "Link", options: "Real Estate Project" },
		{ fieldname: "unit", label: __("Unit"), fieldtype: "Link", options: "Unit" },
		{ fieldname: "customer", label: __("Customer"), fieldtype: "Link", options: "Customer" },
	],
};
