frappe.query_reports["Notification Readiness Report"] = {
	filters: [
		{fieldname: "scenario", label: __("Scenario"), fieldtype: "Select", options: "\nReservation Expiry\nInstallment Due\nRent Due\nLease Expiry\nDocument Expiry\nBacklog Matched Unit"},
		{fieldname: "status", label: __("Status"), fieldtype: "Select", options: "\nEnabled\nDisabled"},
	],
};
