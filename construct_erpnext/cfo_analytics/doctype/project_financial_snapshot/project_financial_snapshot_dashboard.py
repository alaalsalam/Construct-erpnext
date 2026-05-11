from frappe import _


def get_data():
	return {
		"fieldname": "project_financial_snapshot",
		"non_standard_fieldnames": {
			"Project EVM Metrics": "project_financial_snapshot",
			"Unit Cost Allocation": "project_financial_snapshot",
		},
		"transactions": [
			{"label": _("Executive Analytics"), "items": ["Project EVM Metrics"]},
			{"label": _("Unit Costing"), "items": ["Unit Cost Allocation"]},
		],
	}
