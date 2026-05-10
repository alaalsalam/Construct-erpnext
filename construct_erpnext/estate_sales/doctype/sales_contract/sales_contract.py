# SPDX-License-Identifier: MIT
# Sales Contract Document Controller

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cstr, flt, getdate, now_datetime, nowdate

from construct_erpnext.estate_sales.sales_contract_utils import (
    FINAL_UNIT_STATUSES,
    calculate_contract_amounts,
    calculate_installment_totals,
    convert_reservation_to_contract,
    fetch_unit_metadata,
    generate_contract_number,
    get_active_sales_contract_for_unit,
    get_sales_contract_settings,
    has_active_sales_contract,
    mark_unit_sold,
    release_unit_from_contract,
    restore_unit_if_safe,
    validate_installment_schedule_totals,
)


class SalesContract(Document):
    def autoname(self):
        if not self.contract_number:
            settings = get_sales_contract_settings()
            self.contract_number = generate_contract_number(settings)
        self.name = self.contract_number

    def before_validate(self):
        self.set_defaults()
        if self.unit:
            fetch_unit_metadata(self)
        self.sync_status_fields()

    def validate(self):
        self.validate_unit_not_final()
        self.validate_no_duplicate_contract()
        self.validate_party_requirement()
        self.validate_dates()
        self.validate_commercial_terms()
        self.validate_reservation_link()
        calculate_contract_amounts(self)
        calculate_installment_totals(self)
        if self.docstatus == 0:
            validate_installment_schedule_totals(self)

    def before_submit(self):
        self.validate_approve_conditions()

    def on_submit(self):
        settings = get_sales_contract_settings()
        if settings and settings.mark_unit_sold_on_approval:
            mark_unit_sold(self)
        convert_reservation_to_contract(self.unit_reservation, self.name)

    def on_update(self):
        if self.workflow_state and self.contract_status != self.workflow_state:
            self.db_set("contract_status", self.workflow_state, update_modified=False)

    def before_cancel(self):
        if not self.cancellation_reason:
            frappe.throw(_("Cancellation Reason is required before cancelling."))

    def on_cancel(self):
        self.db_set("cancellation_date", now_datetime(), update_modified=False)
        release_unit_from_contract(self)

    def set_defaults(self):
        settings = get_sales_contract_settings()
        self.contract_date = self.contract_date or nowdate()
        self.contract_status = self.contract_status or "Draft"
        self.workflow_state = self.workflow_state or self.contract_status

        if settings:
            if not self.settings:
                self.settings = settings.name
            if self.payment_terms_type is None:
                self.payment_terms_type = "Installment"
            if not self.valid_until and self.contract_date:
                self.valid_until = frappe.utils.add_days(
                    getdate(self.contract_date),
                    settings.default_contract_validity_days or 30,
                )
        if not self.contract_number:
            self.contract_number = generate_contract_number(settings)

    def sync_status_fields(self):
        if self.workflow_state and self.workflow_state != self.contract_status:
            self.contract_status = self.workflow_state
        elif self.contract_status:
            self.workflow_state = self.contract_status

    def validate_unit_not_final(self):
        if not self.unit or self.contract_status in ("Draft", "Cancelled", "Closed"):
            return

        unit_status = frappe.db.get_value("Unit", self.unit, "status")
        if unit_status == "Sold" and self.docstatus == 1:
            other_contract = get_active_sales_contract_for_unit(self.unit, exclude=self.name)
            if not other_contract:
                return

        if unit_status in FINAL_UNIT_STATUSES:
            frappe.throw(
                _(
                    "Unit {0} cannot be sold because its status is {1}."
                ).format(frappe.bold(self.unit), frappe.bold(unit_status))
            )

    def validate_no_duplicate_contract(self):
        if not self.unit or self.contract_status in ("Draft", "Cancelled", "Closed"):
            return

        settings = get_sales_contract_settings()
        if settings and settings.allow_duplicate_contract_for_unit:
            return

        existing = get_active_sales_contract_for_unit(self.unit, exclude=self.name)
        if existing:
            frappe.throw(
                _(
                    "Unit {0} already has an active sales contract {1}. "
                    "A new contract cannot be created for the same unit without enabling duplicate contracts in settings."
                ).format(
                    frappe.bold(self.unit),
                    frappe.bold(existing),
                )
            )

    def validate_party_requirement(self):
        settings = get_sales_contract_settings()
        if settings and not settings.require_customer:
            return

        if not (self.customer or self.lead or self.buyer_name):
            frappe.throw(
                _(
                    "Customer, Lead, or Buyer Name is required for a sales contract. "
                    "Disable the Customer requirement in Sales Contract Settings if needed."
                )
            )

    def validate_dates(self):
        if self.valid_until and self.contract_date:
            if getdate(self.valid_until) < getdate(self.contract_date):
                frappe.throw(_("Valid Until must be on or after Contract Date."))

    def validate_commercial_terms(self):
        if flt(self.sale_price) <= 0:
            frappe.throw(_("Sale Price must be greater than zero."))

        if flt(self.discount_amount) > flt(self.sale_price):
            frappe.throw(_("Discount Amount cannot exceed Sale Price."))

        if self.discount_percent and flt(self.discount_percent) >= 100:
            frappe.throw(_("Discount Percent cannot be 100 percent or more."))

    def validate_reservation_link(self):
        if not self.unit_reservation:
            return

        try:
            reservation = frappe.get_doc("Unit Reservation", self.unit_reservation)
        except frappe.DoesNotExistError:
            frappe.throw(
                _("Reservation {0} does not exist.").format(frappe.bold(self.unit_reservation))
            )
            return

        if reservation.unit != self.unit:
            frappe.throw(
                _("Reservation {0} is for unit {1}, but the contract is for unit {2}.").format(
                    frappe.bold(self.unit_reservation),
                    frappe.bold(reservation.unit),
                    frappe.bold(self.unit),
                )
            )

        is_converted_to_this_contract = (
            reservation.status == "Converted"
            and reservation.converted_to_doctype == "Sales Contract"
            and reservation.converted_to_document == self.name
        )

        if reservation.status != "Reserved" and not is_converted_to_this_contract:
            frappe.throw(
                _("Reservation {0} must be in Reserved status, but its current status is {1}.").format(
                    frappe.bold(self.unit_reservation),
                    frappe.bold(reservation.status),
                )
            )

        if reservation.reservation_type and reservation.reservation_type != "Sale":
            frappe.throw(
                _("Reservation {0} is of type {1}. Only Sale reservations can be converted.").format(
                    frappe.bold(self.unit_reservation),
                    frappe.bold(reservation.reservation_type),
                )
            )

    def validate_approve_conditions(self):
        settings = get_sales_contract_settings()
        if settings and settings.require_installment_schedule:
            validate_installment_schedule_totals(self)


def create_sales_contract_from_reservation(reservation_name):
    """
    Whitelisted method to create a draft Sales Contract from an active sale reservation.
    """
    from construct_erpnext.estate_sales.sales_contract_utils import (
        create_sales_contract_from_reservation as _create,
    )

    return _create(reservation_name)
