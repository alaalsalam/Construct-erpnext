frappe.query_reports["Sales Collection Report"] = {
	filters: [
		{fieldname: "company", label: __("Company"), fieldtype: "Link", options: "Company"},
		{fieldname: "real_estate_project", label: __("Real Estate Project"), fieldtype: "Link", options: "Real Estate Project"},
		{fieldname: "customer", label: __("Customer"), fieldtype: "Link", options: "Customer"},
		{fieldname: "collection_status", label: __("Collection Status"), fieldtype: "Select", options: "\nNot Invoiced\nPartially Invoiced\nFully Invoiced\nPartially Collected\nFully Collected\nOverdue"},
		{fieldname: "from_date", label: __("From Date"), fieldtype: "Date"},
		{fieldname: "to_date", label: __("To Date"), fieldtype: "Date"},
	],
	formatter(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (column.fieldname === "collection_status") {
			return window.construct_erpnext_report_badge(data.collection_status);
		}
		if (column.fieldname === "total_outstanding_amount" && data.total_outstanding_amount > 0) {
			return `<span class="text-danger font-weight-bold">${value}</span>`;
		}
		return value;
	},
};
