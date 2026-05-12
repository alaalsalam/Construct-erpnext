frappe.query_reports["Project Financial Snapshot Report"] = {
	filters: [
		{fieldname: "project", label: __("Project"), fieldtype: "Link", options: "Project"},
		{fieldname: "snapshot_date", label: __("Snapshot Date"), fieldtype: "Date"}
	],
	formatter(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (["cost_risk_status", "overall_status"].includes(column.fieldname)) {
			return window.construct_erpnext_report_badge(data[column.fieldname]);
		}
		return value;
	},
};
