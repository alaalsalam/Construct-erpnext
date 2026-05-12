frappe.query_reports["Procurement Budget Control"] = {
	filters: [
		{ fieldname: "project", label: __("Project"), fieldtype: "Link", options: "Project" },
		{ fieldname: "construction_boq", label: __("Construction BOQ"), fieldtype: "Link", options: "Construction BOQ" },
		{ fieldname: "overrun_only", label: __("Overrun Only"), fieldtype: "Check" },
	],
	formatter(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (column.fieldname === "risk_status") {
			return window.construct_erpnext_report_badge(data.risk_status);
		}
		if (column.fieldname === "variance_percent" && data.variance_percent > 0) {
			return `<span class="text-danger font-weight-bold">${value}</span>`;
		}
		return value;
	},
};
