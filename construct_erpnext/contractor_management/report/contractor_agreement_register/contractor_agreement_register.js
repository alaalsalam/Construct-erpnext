frappe.query_reports["Contractor Agreement Register"] = {
	filters: [
		{ fieldname: "project", label: __("Project"), fieldtype: "Link", options: "Project" },
		{ fieldname: "contractor", label: __("Contractor"), fieldtype: "Link", options: "Supplier" },
		{ fieldname: "status", label: __("Status"), fieldtype: "Select", options: "\nDraft\nUnder Review\nApproved\nActive\nCompleted\nCancelled\nClosed" },
		{ fieldname: "agreement_type", label: __("Agreement Type"), fieldtype: "Select", options: "\nUnit Rate\nLump Sum\nLabor Only\nMaterial & Labor\nOther" },
	],
};
