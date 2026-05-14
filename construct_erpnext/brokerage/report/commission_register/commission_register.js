frappe.query_reports["Commission Register"] = {
	filters: [
		{ fieldname: "broker", label: __("Broker"), fieldtype: "Link", options: "Broker" },
		{ fieldname: "transaction_type", label: __("Transaction Type"), fieldtype: "Select", options: "\nSale\nRent" },
		{ fieldname: "status", label: __("Status"), fieldtype: "Select", options: "\nDraft\nAccrued\nApproved\nPaid\nCancelled" },
		{ fieldname: "from_date", label: __("From Date"), fieldtype: "Date" },
		{ fieldname: "to_date", label: __("To Date"), fieldtype: "Date" },
	],
};
