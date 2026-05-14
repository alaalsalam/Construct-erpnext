from frappe import _


def get_data():
	return {
		"fieldname": "measurement_book",
		"non_standard_fieldnames": {"Subcontract": "subcontract"},
		"transactions": [
			{"label": _("Agreement"), "items": ["Subcontract"]},
			{"label": _("Measurements"), "items": ["Measurement Entry", "Interim Payment Certificate"]},
		],
	}
