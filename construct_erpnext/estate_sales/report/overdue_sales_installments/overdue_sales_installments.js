function construct_erpnext_report_badge(value) {
	if (window.construct_erpnext_report_badge) {
		return window.construct_erpnext_report_badge(value);
	}
	return value || "";
}

frappe.query_reports["Overdue Sales Installments"] = {
	filters: [
		{fieldname: "real_estate_project", label: __("Real Estate Project"), fieldtype: "Link", options: "Real Estate Project"},
		{fieldname: "customer", label: __("Customer"), fieldtype: "Link", options: "Customer"},
		{fieldname: "overdue_days_min", label: __("Minimum Overdue Days"), fieldtype: "Int"},
	],
	formatter(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (!data) {
			return value;
		}
		if (column.fieldname === "invoice_status") {
			return construct_erpnext_report_badge(data.invoice_status);
		}
		if (column.fieldname === "overdue_days" && data.overdue_days > 0) {
			return `<span class="text-danger font-weight-bold">${value}</span>`;
		}
		return value;
	},
};
