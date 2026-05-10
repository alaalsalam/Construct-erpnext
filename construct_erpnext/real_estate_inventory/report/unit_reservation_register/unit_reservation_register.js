frappe.query_reports["Unit Reservation Register"] = {
	filters: [
		{fieldname: "real_estate_project", label: __("Real Estate Project"), fieldtype: "Link", options: "Real Estate Project"},
		{fieldname: "unit", label: __("Unit"), fieldtype: "Link", options: "Unit"},
		{fieldname: "customer", label: __("Customer"), fieldtype: "Link", options: "Customer"},
		{fieldname: "lead", label: __("Lead"), fieldtype: "Link", options: "Lead"},
		{fieldname: "reservation_type", label: __("Reservation Type"), fieldtype: "Select", options: "\nSale\nRent"},
		{fieldname: "status", label: __("Status"), fieldtype: "Select", options: "\nDraft\nReserved\nConverted\nExpired\nCancelled"},
		{fieldname: "from_date", label: __("From Date"), fieldtype: "Date"},
		{fieldname: "to_date", label: __("To Date"), fieldtype: "Date"}
	]
};
