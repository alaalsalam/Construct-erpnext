frappe.query_reports["Broker Performance Report"] = {
	filters: [
		{ fieldname: "broker", label: __("Broker"), fieldtype: "Link", options: "Broker" },
		{ fieldname: "transaction_type", label: __("Transaction Type"), fieldtype: "Select", options: "\nSale\nRent" },
	],
};
