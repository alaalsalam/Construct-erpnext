frappe.query_reports["IPC Line Details"] = {
	filters: [
		{fieldname: "project", label: __("Project"), fieldtype: "Link", options: "Project"},
		{fieldname: "construction_boq", label: __("Construction BOQ"), fieldtype: "Link", options: "Construction BOQ"},
		{fieldname: "construction_work_item", label: __("Work Item"), fieldtype: "Link", options: "Construction Work Item"},
		{fieldname: "contractor", label: __("Contractor"), fieldtype: "Link", options: "Supplier"},
		{fieldname: "ipc", label: __("IPC"), fieldtype: "Link", options: "Interim Payment Certificate"}
	]
};
