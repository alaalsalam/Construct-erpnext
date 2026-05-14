from frappe import _


def get_data():
	return {
		"fieldname": "construction_work_item",
		"non_standard_fieldnames": {
			"Subcontract": "subcontract",
		},
		"transactions": [
			{
				"label": _("BOQ and Agreement"),
				"items": ["Construction BOQ", "Subcontract"],
			},
			{
				"label": _("Procurement"),
				"items": ["Material Request", "Purchase Order", "Purchase Receipt", "Purchase Invoice", "Stock Entry"],
			},
			{
				"label": _("Measurement and IPC"),
				"items": ["Measurement Entry", "Interim Payment Certificate"],
			},
		],
	}

