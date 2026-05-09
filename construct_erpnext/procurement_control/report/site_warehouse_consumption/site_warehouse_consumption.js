frappe.query_reports["Site Warehouse Consumption"] = {
	filters: [
		{ fieldname: "project", label: __("Project"), fieldtype: "Link", options: "Project" },
		{ fieldname: "site_warehouse", label: __("Site Warehouse"), fieldtype: "Link", options: "Warehouse" },
		{ fieldname: "construction_work_item", label: __("Construction Work Item"), fieldtype: "Link", options: "Construction Work Item" },
		{ fieldname: "item_code", label: __("Item"), fieldtype: "Link", options: "Item" },
		{ fieldname: "from_date", label: __("From Date"), fieldtype: "Date" },
		{ fieldname: "to_date", label: __("To Date"), fieldtype: "Date" },
	],
};
