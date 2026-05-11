from frappe import _


def get_data():
	return {
		"fieldname": "cash_flow_forecast",
		"non_standard_fieldnames": {
			"Project EVM Metrics": "cash_flow_forecast",
		},
		"transactions": [
			{"label": _("Executive Analytics"), "items": ["Project EVM Metrics"]},
		],
	}
