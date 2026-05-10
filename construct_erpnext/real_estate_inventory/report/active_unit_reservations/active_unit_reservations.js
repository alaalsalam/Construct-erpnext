frappe.query_reports["Active Unit Reservations"] = {
	filters: [
		{fieldname: "real_estate_project", label: __("Real Estate Project"), fieldtype: "Link", options: "Real Estate Project"},
		{fieldname: "building", label: __("Building"), fieldtype: "Link", options: "Building"},
		{fieldname: "reservation_type", label: __("Reservation Type"), fieldtype: "Select", options: "\nSale\nRent"}
	]
};
