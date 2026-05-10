frappe.query_reports["Expiring Unit Reservations"] = {
	filters: [
		{fieldname: "real_estate_project", label: __("Real Estate Project"), fieldtype: "Link", options: "Real Estate Project"},
		{fieldname: "within_days", label: __("Within Days"), fieldtype: "Int", default: 7}
	]
};
