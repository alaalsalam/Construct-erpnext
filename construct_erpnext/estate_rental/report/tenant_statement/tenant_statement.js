frappe.query_reports["Tenant Statement"] = {
	filters: [
		{ fieldname: "customer", label: __("Customer"), fieldtype: "Link", options: "Customer" },
		{ fieldname: "lease_contract", label: __("Lease Contract"), fieldtype: "Link", options: "Lease Contract" },
		{ fieldname: "real_estate_project", label: __("Real Estate Project"), fieldtype: "Link", options: "Real Estate Project" },
		{ fieldname: "unit", label: __("Unit"), fieldtype: "Link", options: "Unit" },
		{ fieldname: "from_date", label: __("From Date"), fieldtype: "Date" },
		{ fieldname: "to_date", label: __("To Date"), fieldtype: "Date" },
	],
};
