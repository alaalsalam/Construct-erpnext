frappe.query_reports["Overdue Sales Installments"] = {
	filters: [
		{fieldname: "real_estate_project", label: __("Real Estate Project"), fieldtype: "Link", options: "Real Estate Project"},
		{fieldname: "customer", label: __("Customer"), fieldtype: "Link", options: "Customer"},
		{fieldname: "overdue_days_min", label: __("Minimum Overdue Days"), fieldtype: "Int"},
	]
};
