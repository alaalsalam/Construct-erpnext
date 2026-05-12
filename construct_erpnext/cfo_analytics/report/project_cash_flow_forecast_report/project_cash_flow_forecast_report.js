function construct_erpnext_report_badge(value) {
	if (window.construct_erpnext_report_badge) {
		return window.construct_erpnext_report_badge(value);
	}
	return value || "";
}

frappe.query_reports["Project Cash Flow Forecast Report"] = {
	filters: [
		{fieldname: "project", label: __("Project"), fieldtype: "Link", options: "Project"},
		{fieldname: "forecast", label: __("Forecast"), fieldtype: "Link", options: "Project Cash Flow Forecast"},
		{fieldname: "start_date", label: __("Start Date"), fieldtype: "Date"},
		{fieldname: "end_date", label: __("End Date"), fieldtype: "Date"},
		{fieldname: "period_type", label: __("Period Type"), fieldtype: "Select", options: "\nWeekly\nMonthly\nQuarterly"}
	],
	formatter(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (!data) {
			return value;
		}
		if (column.fieldname === "risk") {
			return construct_erpnext_report_badge(data.risk);
		}
		if (column.fieldname === "net_cash_flow" && data.net_cash_flow < 0) {
			return `<span class="text-danger font-weight-bold">${value}</span>`;
		}
		return value;
	},
};
