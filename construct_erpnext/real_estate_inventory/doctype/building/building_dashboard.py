from frappe import _


def get_data():
	return {
		"fieldname": "building",
		"transactions": [
			{"label": _("Hierarchy"), "items": ["Floor", "Unit"]},
			{"label": _("Reservation & Sales"), "items": ["Unit Reservation", "Sales Contract"]},
		],
	}
