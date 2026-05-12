function construct_erpnext_report_badge(value) {
	if (window.construct_erpnext_report_badge) {
		return window.construct_erpnext_report_badge(value);
	}
	return value || "";
}

frappe.query_reports["Project Financial Snapshot Report"] = {
	filters: [
		{fieldname: "project", label: __("Project"), fieldtype: "Link", options: "Project"},
		{fieldname: "snapshot_date", label: __("Snapshot Date"), fieldtype: "Date"}
	],
	formatter(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (!data) {
			return value;
		}
		if (["cost_risk_status", "overall_status"].includes(column.fieldname)) {
			return construct_erpnext_report_badge(data[column.fieldname]);
		}
		return value;
	},
};
