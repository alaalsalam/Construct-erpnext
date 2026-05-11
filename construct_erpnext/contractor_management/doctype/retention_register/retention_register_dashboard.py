from frappe import _


def get_data():
	return {
		"fieldname": "retention_register",
		"non_standard_fieldnames": {
			"Contractor Ledger Entry": "reference_name",
		},
		"transactions": [
			{"label": _("Ledger"), "items": ["Contractor Ledger Entry"]},
		],
	}
