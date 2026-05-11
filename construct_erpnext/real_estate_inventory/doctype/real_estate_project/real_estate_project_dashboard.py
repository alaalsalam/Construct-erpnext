from frappe import _


def get_data():
	return {
		"fieldname": "real_estate_project",
		"internal_links": {
			"Sales Invoice": ["items", "real_estate_project"],
		},
		"transactions": [
			{"label": _("Inventory"), "items": ["Building", "Floor", "Unit", "Property Ownership"]},
			{"label": _("Unit Costing"), "items": ["Unit Cost Allocation"]},
			{"label": _("Reservation & Sales"), "items": ["Unit Reservation", "Sales Contract", "Sales Invoice"]},
		],
	}
