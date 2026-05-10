import frappe
from frappe.utils import getdate, nowdate

from construct_erpnext.real_estate_inventory.inventory_utils import update_related_counts


ACTIVE_STATUS = "Reserved"
UNSAFE_RELEASE_STATUSES = {"Sold", "Rented", "Blocked", "Under Maintenance"}


def get_active_reservation_for_unit(unit, exclude=None):
	if not unit:
		return None

	filters = {
		"unit": unit,
		"status": ACTIVE_STATUS,
		"docstatus": ("<", 2),
	}
	if exclude:
		filters["name"] = ("!=", exclude)

	return frappe.db.get_value(
		"Unit Reservation",
		filters,
		"name",
		order_by="creation desc",
	)


def has_active_reservation(unit):
	return bool(get_active_reservation_for_unit(unit))


def release_unit_if_no_active_reservation(unit, exclude=None):
	if not unit:
		return False

	if get_active_reservation_for_unit(unit, exclude=exclude):
		return False

	unit_doc = frappe.get_doc("Unit", unit)
	if unit_doc.status in UNSAFE_RELEASE_STATUSES:
		return False

	values = {"status": "Available"}
	if frappe.get_meta("Unit").has_field("marketing_status"):
		values["marketing_status"] = "Available"

	frappe.db.set_value("Unit", unit, values, update_modified=True)
	update_related_counts(
		real_estate_project=unit_doc.real_estate_project,
		building=unit_doc.building,
		floor=unit_doc.floor,
	)
	return True


@frappe.whitelist()
def expire_overdue_reservations():
	settings = frappe.get_single("Unit Reservation Settings")
	if not settings.auto_release_expired_reservations:
		return []

	overdue_reservations = frappe.get_all(
		"Unit Reservation",
		filters={
			"status": ACTIVE_STATUS,
			"docstatus": 1,
			"valid_until": ("<", getdate(nowdate())),
		},
		pluck="name",
	)

	expired = []
	for reservation_name in overdue_reservations:
		reservation = frappe.get_doc("Unit Reservation", reservation_name)
		reservation.expire_reservation("انتهت مدة الحجز تلقائياً")
		expired.append(reservation_name)

	return expired


def recalculate_reservation_counts(real_estate_project):
	if not real_estate_project:
		return {}

	update_related_counts(real_estate_project=real_estate_project)
	return {
		"active_reservations": frappe.db.count(
			"Unit Reservation",
			{
				"real_estate_project": real_estate_project,
				"status": ACTIVE_STATUS,
				"docstatus": ("<", 2),
			},
		)
	}
