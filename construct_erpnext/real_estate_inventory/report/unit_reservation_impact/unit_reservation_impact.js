frappe.query_reports["Unit Reservation Impact"] = {
	filters: [
		{fieldname: "real_estate_project", label: __("Real Estate Project"), fieldtype: "Link", options: "Real Estate Project"},
		{fieldname: "building", label: __("Building"), fieldtype: "Link", options: "Building"}
	],
	formatter(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (!data) {
			return value;
		}
		if (column.fieldname === "reservation_rate" && data.reservation_rate > 30) {
			return `<span class="text-warning font-weight-bold">${value}</span>`;
		}
		return value;
	},
};
