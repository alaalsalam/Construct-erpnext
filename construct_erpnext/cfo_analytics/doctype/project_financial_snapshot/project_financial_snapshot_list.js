frappe.listview_settings["Project Financial Snapshot"] = {
	add_fields: ["overall_status", "cost_risk_status", "cash_risk_status"],
	get_indicator(doc) {
		const colors = {"On Track": "green", Watch: "orange", "At Risk": "red", Red: "red", Yellow: "orange", Green: "green"};
		return [__(doc.overall_status || "On Track"), colors[doc.overall_status] || "gray", "overall_status,=," + (doc.overall_status || "On Track")];
	},
};
