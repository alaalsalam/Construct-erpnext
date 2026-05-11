frappe.listview_settings["Construction Work Item"] = {
	add_fields: ["status", "procurement_status", "certification_status", "variance_amount"],
	get_indicator(doc) {
		if (flt(doc.variance_amount) > 0) {
			return [__("Overrun"), "red", "variance_amount,>,0"];
		}
		if (doc.certification_status === "Fully Certified") {
			return [__(doc.certification_status), "green", "certification_status,=," + doc.certification_status];
		}
		if (doc.procurement_status) {
			return [__(doc.procurement_status), "blue", "procurement_status,=," + doc.procurement_status];
		}
		return [__(doc.status || "Planned"), "gray", "status,=," + (doc.status || "Planned")];
	},
};
