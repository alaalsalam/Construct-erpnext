from frappe import _


def get_data():
	return {
		"fieldname": "unit_reservation",
		"internal_links": {
			"Sales Invoice": ["items", "unit_reservation"],
		},
		"transactions": [
			{"label": _("Sales Foundation"), "items": ["Sales Contract", "Sales Invoice"]},
		],
	}
