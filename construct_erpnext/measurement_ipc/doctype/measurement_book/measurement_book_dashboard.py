from frappe import _


def get_data():
	return {
		"fieldname": "measurement_book",
		"transactions": [
			{"label": _("Measurements"), "items": ["Measurement Entry"]},
			{"label": _("IPC"), "items": ["Interim Payment Certificate"]},
		],
	}
