frappe.listview_settings["Construction BOQ"] = {
	add_fields: ["status", "variance_percent"],
	get_indicator(doc) {
		if (doc.status === "Approved") {
			return [__(doc.status), "green", "status,=," + doc.status];
		}
		if (doc.status === "Under Review") {
			return [__(doc.status), "orange", "status,=," + doc.status];
		}
		if (flt(doc.variance_percent) > 10) {
			return [__("Overrun"), "red", "variance_percent,>,10"];
		}
		return [__(doc.status || "Draft"), "gray", "status,=," + (doc.status || "Draft")];
	},
};
