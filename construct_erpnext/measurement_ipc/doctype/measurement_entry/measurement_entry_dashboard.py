from frappe import _


def get_data():
	return {
		"fieldname": "measurement_entry",
		"internal_links": {
			"Interim Payment Certificate": ["lines", "measurement_entry"],
		},
		"transactions": [
			{"label": _("IPC"), "items": ["Interim Payment Certificate"]},
		],
	}
