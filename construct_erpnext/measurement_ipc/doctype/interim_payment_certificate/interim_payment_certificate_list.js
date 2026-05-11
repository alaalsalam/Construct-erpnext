frappe.listview_settings["Interim Payment Certificate"] = {
	add_fields: ["status", "net_payable"],
	get_indicator(doc) {
		const colors = {
			Draft: "gray",
			"Under Review": "orange",
			Certified: "blue",
			Approved: "green",
			"Invoice Created": "green",
			Cancelled: "red",
		};
		return [__(doc.status || "Draft"), colors[doc.status] || "gray", "status,=," + (doc.status || "Draft")];
	},
};
