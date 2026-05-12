frappe.query_reports["Project EVM Metrics Report"] = {
	filters: [
		{fieldname: "project", label: __("Project"), fieldtype: "Link", options: "Project"},
		{fieldname: "calculation_date", label: __("Calculation Date"), fieldtype: "Date"},
		{fieldname: "status", label: __("Status"), fieldtype: "Select", options: "\nDraft\nCalculated\nReviewed\nArchived"}
	],
	formatter(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (["cost_status", "schedule_status", "overall_evm_status"].includes(column.fieldname)) {
			return window.construct_erpnext_report_badge(data[column.fieldname]);
		}
		if (["cost_performance_index", "schedule_performance_index"].includes(column.fieldname) && data[column.fieldname] < 1) {
			return `<span class="text-danger font-weight-bold">${value}</span>`;
		}
		return value;
	},
};
