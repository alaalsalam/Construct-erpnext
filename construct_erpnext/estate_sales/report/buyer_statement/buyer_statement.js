frappe.query_reports["Buyer Statement"] = {
	filters: [
		{ fieldname: "customer", label: __("Customer"), fieldtype: "Link", options: "Customer" },
		{ fieldname: "sales_contract", label: __("Sales Contract"), fieldtype: "Link", options: "Sales Contract" },
		{ fieldname: "real_estate_project", label: __("Real Estate Project"), fieldtype: "Link", options: "Real Estate Project" },
		{ fieldname: "unit", label: __("Unit"), fieldtype: "Link", options: "Unit" },
		{ fieldname: "from_date", label: __("From Date"), fieldtype: "Date" },
		{ fieldname: "to_date", label: __("To Date"), fieldtype: "Date" },
	],
};
