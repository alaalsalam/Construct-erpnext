from frappe import _


def get_data():
	return {
		"fieldname": "construction_boq",
		"internal_links": {
			"Material Request": ["items", "construction_boq"],
			"Purchase Order": ["items", "construction_boq"],
			"Purchase Receipt": ["items", "construction_boq"],
			"Purchase Invoice": ["items", "construction_boq"],
			"Stock Entry": ["items", "construction_boq"],
		},
		"transactions": [
			{"label": _("Execution"), "items": ["Construction Work Item"]},
			{"label": _("Procurement"), "items": ["Material Request", "Purchase Order", "Purchase Receipt", "Purchase Invoice", "Stock Entry"]},
			{"label": _("Measurement & IPC"), "items": ["Measurement Entry", "Interim Payment Certificate"]},
		],
	}
