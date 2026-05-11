from frappe import _


def get_data():
	return {
		"fieldname": "unit",
		"non_standard_fieldnames": {
			"Property Ownership": "unit",
		},
		"internal_links": {
			"Unit Cost Allocation": ["lines", "unit"],
			"Sales Invoice": ["items", "unit"],
		},
		"transactions": [
			{"label": _("Ownership"), "items": ["Property Ownership"]},
			{"label": _("Costing"), "items": ["Unit Cost Allocation"]},
			{"label": _("Reservation & Sales"), "items": ["Unit Reservation", "Sales Contract", "Sales Invoice"]},
		],
	}
