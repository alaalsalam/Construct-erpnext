frappe.query_reports["Recommended Units Report"] = {
	filters: [
		{fieldname: "customer_requirement", label: __("Customer Requirement"), fieldtype: "Link", options: "Customer Requirement"},
		{fieldname: "unit", label: __("Unit"), fieldtype: "Link", options: "Unit"}
	]
};
