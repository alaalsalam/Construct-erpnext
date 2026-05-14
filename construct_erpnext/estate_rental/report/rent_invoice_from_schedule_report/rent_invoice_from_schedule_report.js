frappe.query_reports["Rent Invoice from Schedule Report"] = {
	filters: [
		{ fieldname: "company", label: __("Company"), fieldtype: "Link", options: "Company" },
		{ fieldname: "real_estate_project", label: __("Real Estate Project"), fieldtype: "Link", options: "Real Estate Project" },
		{ fieldname: "lease_contract", label: __("Lease Contract"), fieldtype: "Link", options: "Lease Contract" },
		{ fieldname: "customer", label: __("Customer"), fieldtype: "Link", options: "Customer" },
		{ fieldname: "rent_status", label: __("Status"), fieldtype: "Select", options: "\nPending\nDue\nDraft Invoice\nInvoiced\nPartially Paid\nPaid\nOverdue\nWaived\nCancelled" },
		{ fieldname: "from_due_date", label: __("From Due Date"), fieldtype: "Date" },
		{ fieldname: "to_due_date", label: __("To Due Date"), fieldtype: "Date" },
	],
};
