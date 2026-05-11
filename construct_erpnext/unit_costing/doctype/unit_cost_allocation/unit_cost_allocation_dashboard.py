from frappe import _


def get_data():
	return {
		"fieldname": "unit_cost_allocation",
		"internal_links": {
			"Unit": ["lines", "unit"],
		},
		"transactions": [
			{"label": _("Allocated Units"), "items": ["Unit"]},
		],
	}
