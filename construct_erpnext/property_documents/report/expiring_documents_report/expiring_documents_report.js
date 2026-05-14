frappe.query_reports["Expiring Documents Report"] = {
	filters: [{fieldname: "within_days", label: __("Within Days"), fieldtype: "Int", default: 90}]
};
