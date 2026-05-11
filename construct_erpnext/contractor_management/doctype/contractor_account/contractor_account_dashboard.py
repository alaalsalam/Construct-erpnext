from frappe import _


def get_data():
	return {
		"fieldname": "contractor_account",
		"transactions": [
			{"label": _("IPC"), "items": ["Interim Payment Certificate"]},
			{"label": _("Ledger"), "items": ["Contractor Ledger Entry"]},
			{"label": _("Controls"), "items": ["Retention Register", "Advance Register", "Guarantee Register"]},
		],
	}
