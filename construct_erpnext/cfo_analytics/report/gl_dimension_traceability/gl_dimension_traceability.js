frappe.query_reports["GL Dimension Traceability"] = {
	filters: [
		{fieldname: "company", label: __("Company"), fieldtype: "Link", options: "Company"},
		{fieldname: "project", label: __("Project"), fieldtype: "Link", options: "Project"},
		{fieldname: "unit", label: __("Unit"), fieldtype: "Link", options: "Unit"},
		{fieldname: "construction_work_item", label: __("Construction Work Item"), fieldtype: "Link", options: "Construction Work Item"},
		{fieldname: "cost_code", label: __("Cost Code"), fieldtype: "Link", options: "Cost Code"},
		{fieldname: "from_date", label: __("From Date"), fieldtype: "Date"},
		{fieldname: "to_date", label: __("To Date"), fieldtype: "Date"}
	]
};
