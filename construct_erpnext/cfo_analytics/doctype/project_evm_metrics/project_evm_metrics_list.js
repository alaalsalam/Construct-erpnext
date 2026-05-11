frappe.listview_settings["Project EVM Metrics"] = {
	add_fields: ["overall_evm_status", "cost_status", "schedule_status"],
	get_indicator(doc) {
		const colors = {"On Track": "green", Watch: "orange", "At Risk": "red", Red: "red", Yellow: "orange", Green: "green"};
		return [__(doc.overall_evm_status || "On Track"), colors[doc.overall_evm_status] || "gray", "overall_evm_status,=," + (doc.overall_evm_status || "On Track")];
	},
};
