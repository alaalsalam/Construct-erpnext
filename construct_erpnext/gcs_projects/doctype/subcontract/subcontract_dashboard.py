from frappe import _


def get_data():
	return {
		"fieldname": "subcontract",
		"transactions": [
			{
				"label": _("Agreement Scope"),
				"items": ["Construction Work Item", "Measurement Book", "Measurement Entry"],
			},
			{
				"label": _("Certification"),
				"items": ["Interim Payment Certificate", "Contractor Account", "Retention Register"],
			},
			{
				"label": _("Contractor Controls"),
				"items": ["Advance Register", "Guarantee Register", "Contractor Ledger Entry"],
			},
		],
	}
