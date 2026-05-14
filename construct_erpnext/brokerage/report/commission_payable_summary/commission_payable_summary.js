frappe.query_reports["Commission Payable Summary"] = {
	filters: [
		{ fieldname: "broker", label: __("Broker"), fieldtype: "Link", options: "Broker" },
		{ fieldname: "status", label: __("Status"), fieldtype: "Select", options: "\nAccrued\nApproved\nPaid" },
	],
};
