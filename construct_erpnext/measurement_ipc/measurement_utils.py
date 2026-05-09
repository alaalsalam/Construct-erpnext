import frappe
from frappe.utils import flt


def get_previous_measured_qty(work_item, exclude_entry=None):
	conditions = [
		"construction_work_item = %(work_item)s",
		"status in ('Verified', 'Locked')",
	]
	values = {"work_item": work_item}
	if exclude_entry:
		conditions.append("name != %(exclude_entry)s")
		values["exclude_entry"] = exclude_entry

	return flt(
		frappe.db.sql(
			"""
			SELECT COALESCE(SUM(accepted_qty), 0)
			FROM `tabMeasurement Entry`
			WHERE {conditions}
			""".format(conditions=" AND ".join(conditions)),
			values,
		)[0][0]
	)


def recalculate_work_item_measurement(work_item):
	if not work_item:
		return

	totals = frappe.db.sql(
		"""
		SELECT
			COALESCE(SUM(accepted_qty), 0) AS measured_qty,
			COALESCE(SUM(measured_amount), 0) AS measurement_amount,
			MAX(measurement_date) AS last_measurement_date
		FROM `tabMeasurement Entry`
		WHERE construction_work_item = %(work_item)s
			AND status in ('Verified', 'Locked')
		""",
		{"work_item": work_item},
		as_dict=True,
	)[0]

	planned_quantity = flt(
		frappe.db.get_value("Construction Work Item", work_item, "planned_quantity")
	)
	measured_qty = flt(totals.measured_qty)
	status = "Not Measured"
	if planned_quantity and measured_qty > planned_quantity:
		status = "Over Measured"
	elif planned_quantity and measured_qty == planned_quantity:
		status = "Fully Measured"
	elif measured_qty > 0:
		status = "Partially Measured"

	frappe.db.set_value(
		"Construction Work Item",
		work_item,
		{
			"measured_qty": measured_qty,
			"measurement_amount": flt(totals.measurement_amount),
			"measurement_progress_percent": (
				measured_qty / planned_quantity * 100 if planned_quantity else 0
			),
			"measurement_status": status,
			"last_measurement_date": totals.last_measurement_date,
		},
		update_modified=False,
	)


def recalculate_measurement_book_totals(measurement_book):
	if not measurement_book:
		return

	totals = frappe.db.sql(
		"""
		SELECT
			COUNT(name) AS total_entries,
			COALESCE(SUM(current_measured_qty), 0) AS total_current_measured_qty,
			COALESCE(SUM(accepted_qty), 0) AS total_accepted_qty,
			COALESCE(SUM(measured_amount), 0) AS total_measured_amount
		FROM `tabMeasurement Entry`
		WHERE measurement_book = %(measurement_book)s
			AND status != 'Cancelled'
		""",
		{"measurement_book": measurement_book},
		as_dict=True,
	)[0]

	frappe.db.set_value(
		"Measurement Book",
		measurement_book,
		{
			"total_entries": totals.total_entries,
			"total_current_measured_qty": flt(totals.total_current_measured_qty),
			"total_accepted_qty": flt(totals.total_accepted_qty),
			"total_measured_amount": flt(totals.total_measured_amount),
		},
		update_modified=False,
	)


def create_measurement_entries_from_work_items(measurement_book, work_items):
	book = frappe.get_doc("Measurement Book", measurement_book)
	created = []
	for work_item_name in work_items:
		if frappe.db.exists(
			"Measurement Entry",
			{
				"measurement_book": measurement_book,
				"construction_work_item": work_item_name,
				"status": ["!=", "Cancelled"],
			},
		):
			continue
		work_item = frappe.get_doc("Construction Work Item", work_item_name)
		if work_item.disabled or work_item.status == "Cancelled":
			continue
		entry = frappe.get_doc(
			{
				"doctype": "Measurement Entry",
				"measurement_book": measurement_book,
				"company": book.company,
				"project": work_item.project,
				"contractor": book.contractor,
				"construction_boq": work_item.construction_boq,
				"construction_work_item": work_item.name,
				"wbs_element": work_item.wbs_element,
				"cost_code": work_item.cost_code,
				"item_code": work_item.item_code,
				"description": work_item.description,
				"uom": work_item.uom,
				"planned_quantity": work_item.planned_quantity,
				"unit_rate": work_item.unit_rate,
				"measurement_method": "Direct Quantity",
				"number_of_units": 1,
				"status": "Draft",
			}
		)
		entry.insert(ignore_permissions=True)
		created.append(entry.name)
	return created
