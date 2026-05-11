frappe.ui.form.on("Construction BOQ", {
	refresh(frm) {
		if (frm.is_new()) {
			return;
		}

		frm.add_custom_button(__("Refresh Execution Summary"), () => {
			frappe.call({
				method: "construct_erpnext.construction_boq.boq_sync.refresh_boq_execution_summary",
				args: { construction_boq: frm.doc.name },
				freeze: true,
				freeze_message: __("Refreshing execution summary..."),
			}).then(() => frm.reload_doc());
		});
	},
});
