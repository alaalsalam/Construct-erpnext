frappe.ui.form.on("Unit Reservation", {
	refresh(frm) {
		if (!frm.doc.name || frm.doc.docstatus === 2 || frm.doc.status !== "Reserved") {
			return;
		}

		if (frm.doc.reservation_type === "Rent") {
			frm.add_custom_button(__("Create Lease Contract"), function () {
				frappe.call({
					method: "construct_erpnext.estate_rental.lease_contract.create_lease_contract_from_reservation",
					args: {
						reservation: frm.doc.name,
					},
					callback(r) {
						if (r.message) {
							frappe.set_route("Form", "Lease Contract", r.message);
						}
					},
				});
			}, __("Create"));
		}
	},
});
