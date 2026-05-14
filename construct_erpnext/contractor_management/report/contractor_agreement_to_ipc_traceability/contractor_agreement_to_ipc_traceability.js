frappe.query_reports["Contractor Agreement to IPC Traceability"] = {
	filters: [
		{ fieldname: "project", label: __("Project"), fieldtype: "Link", options: "Project" },
		{ fieldname: "contractor", label: __("Contractor"), fieldtype: "Link", options: "Supplier" },
		{ fieldname: "contractor_agreement", label: __("Contractor Agreement"), fieldtype: "Link", options: "Subcontract" },
		{ fieldname: "ipc", label: __("IPC"), fieldtype: "Link", options: "Interim Payment Certificate" },
	],
};
