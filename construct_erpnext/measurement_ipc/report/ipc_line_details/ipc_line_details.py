import frappe
from frappe import _


def execute(filters=None):
	filters = filters or {}
	columns = [
		{"label": _("IPC"), "fieldname": "ipc", "fieldtype": "Link", "options": "Interim Payment Certificate", "width": 160},
		{"label": _("Work Item"), "fieldname": "construction_work_item", "fieldtype": "Link", "options": "Construction Work Item", "width": 160},
		{"label": _("WBS"), "fieldname": "wbs_element", "fieldtype": "Link", "options": "WBS Element", "width": 150},
		{"label": _("Cost Code"), "fieldname": "cost_code", "fieldtype": "Link", "options": "Cost Code", "width": 130},
		{"label": _("Description"), "fieldname": "description", "fieldtype": "Data", "width": 240},
		{"label": _("BOQ Qty"), "fieldname": "boq_qty", "fieldtype": "Float", "width": 100},
		{"label": _("Previous Certified Qty"), "fieldname": "previous_certified_qty", "fieldtype": "Float", "width": 140},
		{"label": _("Current Certified Qty"), "fieldname": "current_certified_qty", "fieldtype": "Float", "width": 140},
		{"label": _("Total Certified Qty"), "fieldname": "total_certified_qty", "fieldtype": "Float", "width": 130},
		{"label": _("Remaining Qty"), "fieldname": "remaining_qty", "fieldtype": "Float", "width": 120},
		{"label": _("Unit Rate"), "fieldname": "unit_rate", "fieldtype": "Currency", "width": 110},
		{"label": _("Current Amount"), "fieldname": "current_amount", "fieldtype": "Currency", "width": 130},
		{"label": _("Retention"), "fieldname": "retention_amount", "fieldtype": "Currency", "width": 120},
		{"label": _("Net Line Amount"), "fieldname": "net_line_amount", "fieldtype": "Currency", "width": 130},
	]
	conditions = ["1=1"]
	values = {}
	mapping = {
		"project": "ipc.project",
		"construction_boq": "line.construction_boq",
		"construction_work_item": "line.construction_work_item",
		"contractor": "ipc.contractor",
		"ipc": "ipc.name",
	}
	for field, column in mapping.items():
		if filters.get(field):
			conditions.append(f"{column} = %({field})s")
			values[field] = filters[field]
	data = frappe.db.sql(
		f"""
		SELECT ipc.name AS ipc, line.construction_work_item, line.wbs_element, line.cost_code,
			line.description, line.boq_qty, line.previous_certified_qty,
			line.current_certified_qty, line.total_certified_qty, line.remaining_qty,
			line.unit_rate, line.current_amount, line.retention_amount, line.net_line_amount
		FROM `tabInterim Payment Certificate Line` line
		INNER JOIN `tabInterim Payment Certificate` ipc ON ipc.name = line.parent
		WHERE {" AND ".join(conditions)}
		ORDER BY ipc.period_end DESC, line.idx ASC
		""",
		values,
		as_dict=True,
	)
	return columns, data
