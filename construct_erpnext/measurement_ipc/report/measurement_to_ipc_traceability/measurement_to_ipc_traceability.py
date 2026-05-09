import frappe
from frappe import _


def execute(filters=None):
	filters = filters or {}
	columns = [
		{"label": _("Measurement Book"), "fieldname": "measurement_book", "fieldtype": "Link", "options": "Measurement Book", "width": 160},
		{"label": _("Measurement Entry"), "fieldname": "measurement_entry", "fieldtype": "Link", "options": "Measurement Entry", "width": 160},
		{"label": _("Work Item"), "fieldname": "construction_work_item", "fieldtype": "Link", "options": "Construction Work Item", "width": 160},
		{"label": _("Measured Qty"), "fieldname": "current_measured_qty", "fieldtype": "Float", "width": 110},
		{"label": _("Accepted Qty"), "fieldname": "accepted_qty", "fieldtype": "Float", "width": 110},
		{"label": _("IPC"), "fieldname": "ipc", "fieldtype": "Link", "options": "Interim Payment Certificate", "width": 160},
		{"label": _("Current Certified Qty"), "fieldname": "current_certified_qty", "fieldtype": "Float", "width": 140},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 120},
	]
	conditions = ["1=1"]
	values = {}
	if filters.get("project"):
		conditions.append("entry.project = %(project)s")
		values["project"] = filters["project"]
	if filters.get("measurement_book"):
		conditions.append("entry.measurement_book = %(measurement_book)s")
		values["measurement_book"] = filters["measurement_book"]
	if filters.get("construction_work_item"):
		conditions.append("entry.construction_work_item = %(construction_work_item)s")
		values["construction_work_item"] = filters["construction_work_item"]
	if filters.get("ipc"):
		conditions.append("ipc.name = %(ipc)s")
		values["ipc"] = filters["ipc"]
	data = frappe.db.sql(
		f"""
		SELECT entry.measurement_book, entry.name AS measurement_entry,
			entry.construction_work_item, entry.current_measured_qty, entry.accepted_qty,
			ipc.name AS ipc, line.current_certified_qty, COALESCE(ipc.status, entry.status) AS status
		FROM `tabMeasurement Entry` entry
		LEFT JOIN `tabInterim Payment Certificate Line` line ON line.measurement_entry = entry.name
		LEFT JOIN `tabInterim Payment Certificate` ipc ON ipc.name = line.parent AND ipc.docstatus != 2
		WHERE {" AND ".join(conditions)}
		ORDER BY entry.measurement_date DESC, entry.modified DESC
		""",
		values,
		as_dict=True,
	)
	return columns, data
