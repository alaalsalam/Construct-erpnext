frappe.query_reports["Contractor Exposure Summary"] = {
	filters: [
		{fieldname: "project", label: __("Project"), fieldtype: "Link", options: "Project"},
		{fieldname: "contractor", label: __("Contractor"), fieldtype: "Link", options: "Supplier"}
	],
	formatter(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (!data) {
			return value;
		}
		if (column.fieldname === "outstanding_balance" && data.outstanding_balance > 0) {
			return `<span class="text-danger font-weight-bold">${value}</span>`;
		}
		if (column.fieldname === "total_paid_amount" && data.total_paid_amount > 0) {
			return `<span class="text-success font-weight-bold">${value}</span>`;
		}
		return value;
	},
};
