frappe.listview_settings["Unit"] = {
	add_fields: ["status", "marketing_status", "profitability_status"],
	get_indicator(doc) {
		const status_colors = {
			Available: "green",
			Reserved: "orange",
			Sold: "blue",
			Rented: "purple",
			Blocked: "red",
			"Under Maintenance": "red",
		};
		return [__(doc.status || "Available"), status_colors[doc.status] || "gray", "status,=," + (doc.status || "Available")];
	},
};
