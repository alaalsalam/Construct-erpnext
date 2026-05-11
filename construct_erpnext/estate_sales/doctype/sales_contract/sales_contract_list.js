frappe.listview_settings["Sales Contract"] = {
	add_fields: ["contract_status", "collection_status"],
	get_indicator(doc) {
		const colors = {
			Draft: "gray",
			"Under Review": "orange",
			Approved: "green",
			Active: "blue",
			Cancelled: "red",
			Closed: "gray",
		};
		return [__(doc.contract_status || "Draft"), colors[doc.contract_status] || "gray", "contract_status,=," + (doc.contract_status || "Draft")];
	},
};
