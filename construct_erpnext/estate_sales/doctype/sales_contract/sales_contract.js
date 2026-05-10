frappe.ui.form.on("Sales Contract", {
	refresh(frm) {
		if (!frm.doc.name || frm.doc.docstatus === 2) {
			return;
		}

		if (["Approved", "Active"].includes(frm.doc.contract_status)) {
			frm.add_custom_button(__("Create Sales Invoice"), function () {
				frappe.call({
					method: "construct_erpnext.estate_sales.sales_invoice_utils.create_invoice_from_contract_installments",
					args: {
						sales_contract: frm.doc.name,
					},
					callback(r) {
						if (r.message) {
							frappe.set_route("Form", "Sales Invoice", r.message);
						}
					},
				});
			}, __("Create"));
		}

		frm.add_custom_button(__("Refresh Collection Status"), function () {
			frappe.call({
				method: "construct_erpnext.estate_sales.collections_utils.refresh_contract_collection_status",
				args: {
					sales_contract: frm.doc.name,
				},
				callback() {
					frm.reload_doc();
				},
			});
		}, __("Actions"));
	},
});
