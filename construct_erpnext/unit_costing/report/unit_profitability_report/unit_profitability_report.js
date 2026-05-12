function construct_erpnext_report_badge(value) {
	if (window.construct_erpnext_report_badge) {
		return window.construct_erpnext_report_badge(value);
	}
	return value || "";
}

frappe.query_reports["Unit Profitability Report"] = {
	filters: [
		{fieldname: "real_estate_project", label: __("Real Estate Project"), fieldtype: "Link", options: "Real Estate Project"},
		{fieldname: "building", label: __("Building"), fieldtype: "Link", options: "Building"},
		{fieldname: "floor", label: __("Floor"), fieldtype: "Link", options: "Floor"},
		{fieldname: "unit_type", label: __("Unit Type"), fieldtype: "Link", options: "Unit Type"},
		{fieldname: "unit_status", label: __("Unit Status"), fieldtype: "Select", options: "\nAvailable\nReserved\nSold\nRented\nBlocked\nUnder Maintenance\nUnder Construction"},
		{fieldname: "profitability_status", label: __("Profitability Status"), fieldtype: "Select", options: "\nProfitable\nWatch\nLoss Risk\nNot Priced"}
	],
	formatter(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (!data) {
			return value;
		}
		if (["status", "profitability_status"].includes(column.fieldname)) {
			return construct_erpnext_report_badge(data[column.fieldname]);
		}
		return value;
	},
};
