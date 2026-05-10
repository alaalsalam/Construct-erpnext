# SPDX-License-Identifier: MIT
# Lease Contract Document Controller

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, getdate, now_datetime, nowdate

from construct_erpnext.estate_rental.lease_contract_utils import (
	FINAL_UNIT_STATUSES,
	calculate_lease_amounts,
	calculate_rent_schedule_totals,
	convert_reservation_to_lease,
	fetch_unit_metadata,
	generate_contract_number,
	generate_rent_schedule,
	get_active_lease_contract_for_unit,
	get_lease_contract_settings,
	mark_unit_rented,
	release_unit_from_lease_if_safe,
	validate_rent_schedule_totals,
)


class LeaseContract(Document):
	def autoname(self):
		if not self.contract_number:
			self.contract_number = generate_contract_number()
		self.name = self.contract_number

	def before_validate(self):
		self.set_defaults()
		if self.unit:
			fetch_unit_metadata(self)
		self.sync_status_fields()

	def validate(self):
		self.validate_dates()
		self.validate_party_requirement()
		self.validate_unit_available_for_lease()
		self.validate_duplicate_active_lease()
		self.validate_rental_terms()
		self.validate_reservation_link()
		calculate_lease_amounts(self)
		settings = get_lease_contract_settings()
		if settings and settings.auto_generate_rent_schedule and not self.rent_schedule:
			generate_rent_schedule(self)
		calculate_rent_schedule_totals(self)
		if self.docstatus == 0:
			validate_rent_schedule_totals(self)

	def before_submit(self):
		validate_rent_schedule_totals(self)

	def on_submit(self):
		settings = get_lease_contract_settings()
		if not settings or settings.mark_unit_rented_on_activation:
			mark_unit_rented(self)
		convert_reservation_to_lease(self.unit_reservation, self.name)

	def on_update(self):
		if self.workflow_state and self.lease_status != self.workflow_state:
			self.db_set("lease_status", self.workflow_state, update_modified=False)

	def on_update_after_submit(self):
		if self.workflow_state and self.lease_status != self.workflow_state:
			self.db_set("lease_status", self.workflow_state, update_modified=False)

	def before_cancel(self):
		if not self.cancellation_reason:
			frappe.throw(_("Cancellation Reason is required before cancelling."))

	def on_cancel(self):
		self.db_set("cancellation_date", now_datetime(), update_modified=False)
		release_unit_from_lease_if_safe(self)

	def set_defaults(self):
		settings = get_lease_contract_settings()
		self.contract_date = self.contract_date or nowdate()
		self.lease_status = self.lease_status or "Draft"
		self.workflow_state = self.workflow_state or self.lease_status
		if settings:
			self.settings = self.settings or settings.name
			self.billing_frequency = self.billing_frequency or settings.default_billing_frequency or "Monthly"
		else:
			self.billing_frequency = self.billing_frequency or "Monthly"
		if not self.contract_number:
			self.contract_number = generate_contract_number(settings)

	def sync_status_fields(self):
		if self.workflow_state and self.workflow_state != self.lease_status:
			self.lease_status = self.workflow_state
		elif self.lease_status:
			self.workflow_state = self.lease_status

	def validate_dates(self):
		if self.lease_start_date and self.lease_end_date and getdate(self.lease_end_date) < getdate(self.lease_start_date):
			frappe.throw(_("Lease End Date must be on or after Lease Start Date."))
		settings = get_lease_contract_settings()
		if settings and not settings.allow_backdated_lease and self.lease_start_date and self.contract_date:
			if getdate(self.lease_start_date) < getdate(self.contract_date):
				frappe.throw(_("Lease Start Date cannot be before Contract Date."))

	def validate_party_requirement(self):
		settings = get_lease_contract_settings()
		if settings and not settings.require_customer:
			return
		if not self.customer:
			frappe.throw(_("Customer is required for a Lease Contract."))

	def validate_unit_available_for_lease(self):
		if not self.unit or self.lease_status in ("Draft", "Cancelled", "Closed", "Expired", "Terminated"):
			return

		unit_status = frappe.db.get_value("Unit", self.unit, "status")
		if unit_status == "Rented" and self.docstatus == 1:
			other_contract = get_active_lease_contract_for_unit(self.unit, exclude=self.name)
			if not other_contract:
				return
		if unit_status in FINAL_UNIT_STATUSES:
			frappe.throw(
				_("Unit {0} cannot be leased because its status is {1}.").format(
					frappe.bold(self.unit),
					frappe.bold(unit_status),
				)
			)

	def validate_duplicate_active_lease(self):
		if not self.unit or self.lease_status in ("Draft", "Cancelled", "Closed", "Expired", "Terminated"):
			return
		settings = get_lease_contract_settings()
		if settings and settings.allow_duplicate_active_lease_for_unit:
			return
		existing = get_active_lease_contract_for_unit(self.unit, exclude=self.name)
		if existing:
			frappe.throw(
				_("Unit {0} already has active Lease Contract {1}.").format(
					frappe.bold(self.unit),
					frappe.bold(existing),
				)
			)

	def validate_rental_terms(self):
		if flt(self.monthly_rent) <= 0:
			frappe.throw(_("Monthly Rent must be greater than zero."))
		for row in self.rent_schedule or []:
			if flt(row.rent_amount) < 0:
				frappe.throw(_("Rent Amount cannot be negative."))
			if row.rent_period_start and row.rent_period_end:
				if getdate(row.rent_period_end) < getdate(row.rent_period_start):
					frappe.throw(_("Rent period end must be on or after rent period start."))

	def validate_reservation_link(self):
		if not self.unit_reservation:
			return
		reservation = frappe.get_doc("Unit Reservation", self.unit_reservation)
		if reservation.unit != self.unit:
			frappe.throw(_("Reservation unit must match Lease Contract unit."))
		is_converted_to_this_lease = (
			reservation.status == "Converted"
			and reservation.converted_to_doctype == "Lease Contract"
			and reservation.converted_to_document == self.name
		)
		if reservation.status != "Reserved" and not is_converted_to_this_lease:
			frappe.throw(_("Reservation must be Reserved before conversion to Lease Contract."))
		if reservation.reservation_type != "Rent":
			frappe.throw(_("Only Rent reservations can be converted to Lease Contract."))


@frappe.whitelist()
def create_lease_contract_from_reservation(reservation):
	from construct_erpnext.estate_rental.lease_contract_utils import (
		create_lease_contract_from_reservation as _create,
	)

	return _create(reservation)
