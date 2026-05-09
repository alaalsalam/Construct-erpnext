import json

import frappe
from frappe import _

from construct_erpnext.measurement_ipc.measurement_utils import (
	create_measurement_entries_from_work_items,
)


@frappe.whitelist()
def create_entries_from_work_items(measurement_book, work_items):
	if isinstance(work_items, str):
		work_items = json.loads(work_items)
	if not work_items:
		frappe.throw(_("At least one Construction Work Item is required."))
	return create_measurement_entries_from_work_items(measurement_book, work_items)
