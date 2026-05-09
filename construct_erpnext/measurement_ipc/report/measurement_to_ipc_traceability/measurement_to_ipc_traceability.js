frappe.query_reports["Measurement to IPC Traceability"] = {
	filters: [
		{fieldname: "project", label: __("Project"), fieldtype: "Link", options: "Project"},
		{fieldname: "measurement_book", label: __("Measurement Book"), fieldtype: "Link", options: "Measurement Book"},
		{fieldname: "ipc", label: __("IPC"), fieldtype: "Link", options: "Interim Payment Certificate"},
		{fieldname: "construction_work_item", label: __("Work Item"), fieldtype: "Link", options: "Construction Work Item"}
	]
};
