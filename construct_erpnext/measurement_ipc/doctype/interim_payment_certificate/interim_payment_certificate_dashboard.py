from frappe import _


def get_data():
	return {
		"fieldname": "ipc",
		"non_standard_fieldnames": {
			"Measurement Entry": "interim_payment_certificate",
			"Subcontract": "subcontract",
			"Contractor Account": "last_ipc",
			"Contractor Ledger Entry": "ipc",
			"Retention Register": "ipc",
		},
		"transactions": [
			{"label": _("Agreement"), "items": ["Subcontract", "Measurement Book", "Measurement Entry"]},
			{"label": _("Contractor Ledger"), "items": ["Contractor Account", "Contractor Ledger Entry", "Retention Register"]},
		],
	}
