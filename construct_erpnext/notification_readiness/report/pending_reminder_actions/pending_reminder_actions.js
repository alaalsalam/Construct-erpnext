frappe.query_reports["Pending Reminder Actions"] = {
	filters: [
		{fieldname: "scenario", label: __("Scenario"), fieldtype: "Select", options: "\nReservation Expiry\nInstallment Due\nRent Due\nLease Expiry\nDocument Expiry\nBacklog Matched Unit"},
		{fieldname: "status", label: __("Status"), fieldtype: "Select", options: "\nPending\nReady\nCompleted\nSkipped\nFailed", default: "Pending"},
	],
};
