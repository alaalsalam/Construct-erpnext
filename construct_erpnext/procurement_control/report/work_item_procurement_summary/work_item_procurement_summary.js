function construct_erpnext_report_badge(value) {
	if (window.construct_erpnext_report_badge) {
		return window.construct_erpnext_report_badge(value);
	}
	return value || "";
}

frappe.query_reports["Work Item Procurement Summary"] = {
	filters: [
		{ fieldname: "project", label: __("Project"), fieldtype: "Link", options: "Project" },
		{ fieldname: "construction_boq", label: __("Construction BOQ"), fieldtype: "Link", options: "Construction BOQ" },
		{ fieldname: "construction_work_item", label: __("Construction Work Item"), fieldtype: "Link", options: "Construction Work Item" },
		{ fieldname: "item_category", label: __("Item Category"), fieldtype: "Select", options: "\nMaterial\nLabor\nEquipment\nSubcontract\nOverhead\nContingency\nOther" },
		{ fieldname: "procurement_status", label: __("Procurement Status"), fieldtype: "Select", options: "\nNot Requested\nPartially Requested\nFully Requested\nPartially Ordered\nFully Ordered\nPartially Received\nFully Received\nPartially Invoiced\nFully Invoiced\nOver Requested\nOver Ordered\nOver Received" },
	],
	formatter(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (column.fieldname === "procurement_status") {
			return construct_erpnext_report_badge(data.procurement_status);
		}
		return value;
	},
};
