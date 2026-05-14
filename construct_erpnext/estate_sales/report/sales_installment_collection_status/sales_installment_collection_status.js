frappe.query_reports["Sales Installment Collection Status"] = {
	filters: [
		{ fieldname: "real_estate_project", label: __("Real Estate Project"), fieldtype: "Link", options: "Real Estate Project" },
		{ fieldname: "sales_contract", label: __("Sales Contract"), fieldtype: "Link", options: "Sales Contract" },
		{ fieldname: "customer", label: __("Customer"), fieldtype: "Link", options: "Customer" },
		{
			fieldname: "status",
			label: __("Status"),
			fieldtype: "Select",
			options: "\nNot Invoiced\nDraft Invoice\nInvoiced\nPartially Paid\nPaid\nOverdue\nCancelled",
		},
		{ fieldname: "from_due_date", label: __("From Due Date"), fieldtype: "Date" },
		{ fieldname: "to_due_date", label: __("To Due Date"), fieldtype: "Date" },
	],
};
