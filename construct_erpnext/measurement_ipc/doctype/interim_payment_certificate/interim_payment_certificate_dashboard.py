from frappe import _


def get_data():
	return {
		"fieldname": "interim_payment_certificate",
		"non_standard_fieldnames": {
			"Measurement Entry": "interim_payment_certificate",
			"Contractor Ledger Entry": "ipc",
			"Retention Register": "ipc",
		},
		"transactions": [
			{"label": _("Measurement"), "items": ["Measurement Entry"]},
			{"label": _("Contractor Control"), "items": ["Contractor Ledger Entry", "Retention Register"]},
		],
	}
