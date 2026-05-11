from frappe import _


def get_data():
	return {
		"fieldname": "sales_contract",
		"non_standard_fieldnames": {
			"Unit Reservation": "converted_to_document",
		},
		"internal_links": {
			"Sales Invoice": ["items", "sales_contract"],
		},
		"transactions": [
			{"label": _("Reservation"), "items": ["Unit Reservation"]},
			{"label": _("Installments & Invoice Drafts"), "items": ["Sales Invoice"]},
		],
	}
