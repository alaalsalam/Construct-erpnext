frappe.query_reports["Project Purchase Control Summary"] = {
	filters: [
		{ fieldname: "project", label: __("Project"), fieldtype: "Link", options: "Project", reqd: 1 },
		{ fieldname: "construction_boq", label: __("Construction BOQ"), fieldtype: "Link", options: "Construction BOQ" },
		{ fieldname: "cost_code", label: __("Cost Code"), fieldtype: "Link", options: "Cost Code" },
		{ fieldname: "wbs_element", label: __("WBS"), fieldtype: "Link", options: "WBS Element" },
		{ fieldname: "item_category", label: __("Item Category"), fieldtype: "Select", options: "\nMaterial\nLabor\nEquipment\nSubcontract\nOverhead\nContingency\nOther" },
		{ fieldname: "execution_status", label: __("Execution Status"), fieldtype: "Select", options: "\nNot Started\nRequested\nOrdered\nReceived\nInvoiced\nPartially Consumed\nFully Consumed\nPartially Measured\nCertified\nOverrun\nUnderrun" },
	],
	formatter(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (["execution_status", "risk_status"].includes(column.fieldname)) {
			return window.construct_erpnext_report_badge(data[column.fieldname]);
		}
		if (column.fieldname === "variance_percent" && data.variance_percent > 10) {
			return `<span class="text-danger font-weight-bold">${value}</span>`;
		}
		return value;
	},
};
