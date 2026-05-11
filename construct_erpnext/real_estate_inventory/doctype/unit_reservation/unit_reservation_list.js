frappe.listview_settings["Unit Reservation"] = {
	add_fields: ["status", "reservation_type", "valid_until"],
	get_indicator(doc) {
		const colors = {
			Draft: "gray",
			Reserved: "orange",
			Converted: "green",
			Expired: "red",
			Cancelled: "red",
		};
		return [__(doc.status || "Draft"), colors[doc.status] || "gray", "status,=," + (doc.status || "Draft")];
	},
};
