from frappe import _


def get_data():
	return {
		"fieldname": "floor",
		"transactions": [
			{"label": _("Units"), "items": ["Unit"]},
			{"label": _("Reservation & Sales"), "items": ["Unit Reservation", "Sales Contract"]},
		],
	}
