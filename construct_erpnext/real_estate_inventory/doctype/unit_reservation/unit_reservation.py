import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe.utils import add_days, cstr, flt, getdate, now_datetime, nowdate

from construct_erpnext.real_estate_inventory.inventory_utils import update_related_counts
from construct_erpnext.real_estate_inventory.reservation_utils import (
	get_active_reservation_for_unit,
	release_unit_if_no_active_reservation,
)


FINAL_UNIT_STATUSES = {"Sold", "Rented", "Blocked", "Under Maintenance"}
ACTIVE_RESERVATION_STATUS = "Reserved"


class UnitReservation(Document):
	def autoname(self):
		self.set_reservation_number()
		self.name = self.reservation_number

	def before_validate(self):
		self.set_defaults()
		self.fetch_unit_metadata()
		self.sync_status_fields()

	def validate(self):
		self.fetch_unit_metadata()
		self.validate_dates()
		self.validate_party_requirement()
		self.validate_amount()
		self.validate_status_reason()
		self.validate_unit_available_for_reservation()

	def on_submit(self):
		self.mark_reserved()

	def before_cancel(self):
		if not self.cancelled_reason:
			frappe.throw(_("Cancelled Reason is required before cancelling a reservation."))

	def on_cancel(self):
		self.db_set("status", "Cancelled", update_modified=False)
		self.db_set("workflow_state", "Cancelled", update_modified=False)
		self.release_unit_if_safe()

	def set_defaults(self):
		settings = get_reservation_settings()
		self.reservation_date = self.reservation_date or nowdate()
		self.valid_from = self.valid_from or nowdate()

		if not self.valid_until:
			self.valid_until = add_days(
				getdate(self.valid_from),
				settings.default_reservation_validity_days or 7,
			)

		self.set_reservation_number()

		self.status = self.status or "Draft"
		self.workflow_state = self.workflow_state or self.status

	def set_reservation_number(self):
		if self.reservation_number:
			return

		settings = get_reservation_settings()
		prefix = (settings.reservation_number_prefix or "RES").strip() or "RES"
		self.reservation_number = make_autoname(f"{prefix}-.YYYY.-.#####")

	def fetch_unit_metadata(self):
		if not self.unit:
			return

		unit = frappe.get_cached_doc("Unit", self.unit)
		self.real_estate_project = self.real_estate_project or unit.real_estate_project
		self.project = unit.project
		self.building = unit.building
		self.floor = unit.floor
		self.unit_type = unit.unit_type
		self.expected_sale_price = unit.expected_sale_price
		self.expected_monthly_rent = unit.expected_monthly_rent

		if self.real_estate_project:
			self.company = self.company or frappe.db.get_value(
				"Real Estate Project", self.real_estate_project, "company"
			)

	def sync_status_fields(self):
		if self.workflow_state and self.workflow_state != self.status:
			self.status = self.workflow_state
		elif self.status:
			self.workflow_state = self.status

	def validate_dates(self):
		if self.valid_from and self.valid_until and getdate(self.valid_until) < getdate(self.valid_from):
			frappe.throw(_("Valid Until must be on or after Valid From."))

	def validate_party_requirement(self):
		settings = get_reservation_settings()
		if settings.require_customer_or_lead and not (self.customer or self.lead or self.party_name):
			frappe.throw(_("Customer, Lead, or Party Name is required for a unit reservation."))

	def validate_amount(self):
		if flt(self.reservation_amount) < 0:
			frappe.throw(_("Reservation Amount cannot be negative."))

		settings = get_reservation_settings()
		if settings.require_reservation_amount and flt(self.reservation_amount) <= 0:
			frappe.throw(_("Reservation Amount is required by reservation settings."))

	def validate_status_reason(self):
		if self.status == "Cancelled" and not self.cancelled_reason:
			frappe.throw(_("Cancelled Reason is required."))
		if self.status == "Expired" and not self.expiry_reason:
			frappe.throw(_("Expiry Reason is required."))

	def validate_unit_available_for_reservation(self):
		if not self.unit or self.status not in ("Draft", ACTIVE_RESERVATION_STATUS):
			return

		unit_status = frappe.db.get_value("Unit", self.unit, "status")
		active_reservation = get_active_reservation_for_unit(self.unit, exclude=self.name)
		current_active_reservation = get_active_reservation_for_unit(self.unit)
		settings = get_reservation_settings()

		if unit_status in FINAL_UNIT_STATUSES:
			frappe.throw(
				_("Unit {0} cannot be reserved because its status is {1}.").format(
					frappe.bold(self.unit), frappe.bold(unit_status)
				)
			)

		if (
			unit_status == ACTIVE_RESERVATION_STATUS
			and current_active_reservation != self.name
			and not settings.allow_reservation_for_reserved_units
		):
			frappe.throw(
				_("Unit {0} is already marked as reserved.").format(frappe.bold(self.unit))
			)

		if active_reservation and not settings.allow_reservation_for_reserved_units:
			frappe.throw(
				_("Unit {0} already has active reservation {1}.").format(
					frappe.bold(self.unit), frappe.bold(active_reservation)
				)
			)

	def validate_duplicate_active_reservation(self):
		settings = get_reservation_settings()
		if settings.allow_reservation_for_reserved_units:
			return

		active_reservation = get_active_reservation_for_unit(self.unit, exclude=self.name)
		if active_reservation:
			frappe.throw(
				_("Unit {0} already has active reservation {1}.").format(
					frappe.bold(self.unit), frappe.bold(active_reservation)
				)
			)

		unit_status = frappe.db.get_value("Unit", self.unit, "status")
		if unit_status == ACTIVE_RESERVATION_STATUS:
			frappe.throw(_("Unit {0} is already marked as reserved.").format(frappe.bold(self.unit)))

	def mark_reserved(self):
		self.validate_duplicate_active_reservation()

		unit = frappe.get_doc("Unit", self.unit)
		if unit.status in FINAL_UNIT_STATUSES:
			frappe.throw(
				_("Unit {0} cannot be reserved because its status is {1}.").format(
					frappe.bold(self.unit), frappe.bold(unit.status)
				)
			)

		if not self.previous_unit_status:
			self.db_set("previous_unit_status", unit.status, update_modified=False)
		if hasattr(unit, "marketing_status") and not self.previous_marketing_status:
			self.db_set("previous_marketing_status", unit.marketing_status, update_modified=False)

		values = {"status": ACTIVE_RESERVATION_STATUS}
		if frappe.get_meta("Unit").has_field("marketing_status"):
			values["marketing_status"] = ACTIVE_RESERVATION_STATUS
		frappe.db.set_value("Unit", self.unit, values, update_modified=True)

		self.db_set("status", ACTIVE_RESERVATION_STATUS, update_modified=False)
		self.db_set("workflow_state", ACTIVE_RESERVATION_STATUS, update_modified=False)
		update_related_counts(
			real_estate_project=self.real_estate_project,
			building=self.building,
			floor=self.floor,
		)

	def cancel_reservation(self, reason):
		if not reason:
			frappe.throw(_("Cancellation reason is required."))

		self.db_set("cancelled_reason", reason)
		if self.docstatus == 1:
			self.cancel()
		else:
			self.status = "Cancelled"
			self.workflow_state = "Cancelled"
			self.save()
			self.release_unit_if_safe()

	def expire_reservation(self, reason=None):
		reason = reason or _("Reservation validity period has expired.")
		if self.status != ACTIVE_RESERVATION_STATUS:
			return

		self.db_set("expiry_reason", cstr(reason), update_modified=False)
		self.db_set("status", "Expired", update_modified=False)
		self.db_set("workflow_state", "Expired", update_modified=False)
		self.release_unit_if_safe()

	def convert_reservation(self, target_doctype, target_document):
		if self.status != ACTIVE_RESERVATION_STATUS:
			frappe.throw(_("Only active reservations can be converted."))
		if not target_doctype or not target_document:
			frappe.throw(_("Target document is required to convert a reservation."))

		self.db_set(
			{
				"converted_to_doctype": target_doctype,
				"converted_to_document": target_document,
				"converted_on": now_datetime(),
				"converted_by": frappe.session.user,
				"status": "Converted",
				"workflow_state": "Converted",
			}
		)

	def release_unit_if_safe(self):
		release_unit_if_no_active_reservation(self.unit, exclude=self.name)


def get_reservation_settings():
	return frappe.get_single("Unit Reservation Settings")
