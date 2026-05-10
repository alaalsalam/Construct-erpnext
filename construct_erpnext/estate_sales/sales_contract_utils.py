# SPDX-License-Identifier: MIT
# Estate Sales services for Sales Contract and Installment Plan

import frappe
from frappe import _
from frappe.model.naming import make_autoname
from frappe.utils import add_days, cstr, flt, getdate, now_datetime, nowdate


FINAL_UNIT_STATUSES = {"Sold", "Rented", "Blocked", "Under Maintenance"}
ACTIVE_RESERVATION_STATUS = "Reserved"


def get_sales_contract_settings():
    """Return the current Sales Contract Settings singleton."""
    try:
        return frappe.get_single("Sales Contract Settings")
    except frappe.DoesNotExistError:
        return None


def generate_contract_number(settings=None):
    """Generate a contract number from settings prefix."""
    if settings is None:
        settings = get_sales_contract_settings()

    if settings and settings.contract_number_prefix:
        prefix = settings.contract_number_prefix.strip()
    else:
        prefix = "SC"

    return make_autoname(f"{prefix}-.YYYY.-.#####")


def get_active_sales_contract_for_unit(unit, exclude=None):
    """
    Return the name of the active Sales Contract for the given Unit,
    excluding a specific contract name if provided.

    Active means contract_status is one of: Under Review, Approved, Active.
    """
    active_statuses = ("Under Review", "Approved", "Active")

    filters = {
        "unit": unit,
        "contract_status": ["in", active_statuses],
    }
    if exclude:
        filters["name"] = ["!=", exclude]

    result = frappe.db.get_value(
        "Sales Contract",
        filters,
        "name",
        order_by="contract_date desc",
    )
    return result


def has_active_sales_contract(unit, exclude=None):
    """Return True if the unit has an active sales contract."""
    return bool(get_active_sales_contract_for_unit(unit, exclude=exclude))


def fetch_unit_metadata(contract):
    """
    Fetch and set unit-related read-only metadata on the contract document.
    Called from controller before_validate and on_submit.
    """
    if not contract.unit:
        return

    unit = frappe.get_cached_doc("Unit", contract.unit)

    contract.real_estate_project = contract.real_estate_project or unit.real_estate_project
    contract.project = unit.project
    contract.building = unit.building
    contract.floor = unit.floor
    contract.unit_type = unit.unit_type
    contract.unit_area = unit.area
    contract.expected_sale_price = unit.expected_sale_price
    contract.unit_status = unit.status

    if contract.real_estate_project and not contract.company:
        contract.company = frappe.db.get_value(
            "Real Estate Project",
            contract.real_estate_project,
            "company",
        )

    if not contract.currency:
        if contract.company:
            contract.currency = frappe.db.get_value("Company", contract.company, "default_currency")
        if not contract.currency:
            contract.currency = "YER"


def calculate_contract_amounts(contract):
    """
    Calculate commercial terms amounts.
    Called from controller validate and before_submit.
    """
    sale_price = flt(contract.sale_price)

    if contract.discount_percent:
        contract.discount_amount = sale_price * contract.discount_percent / 100.0

    net = sale_price - flt(contract.discount_amount)
    contract.net_price = max(net, 0)

    if contract.net_price and contract.down_payment_percent:
        contract.down_payment_amount = contract.net_price * contract.down_payment_percent / 100.0
    else:
        contract.down_payment_amount = 0


def calculate_installment_totals(contract):
    """
    Calculate total, outstanding, and count from installment child rows.
    Called from controller before_save and validate.
    """
    if not contract.installments:
        contract.total_installment_amount = 0
        contract.outstanding_installment_amount = 0
        contract.installment_count = 0
        return

    total = sum(flt(row.amount) for row in contract.installments)
    settled = sum(
        flt(row.amount)
        for row in contract.installments
        if row.installment_status in ("Paid", "Waived")
    )

    contract.total_installment_amount = total
    contract.outstanding_installment_amount = total - settled
    contract.installment_count = len(contract.installments)


def validate_installment_schedule_totals(contract, tolerance_percent=None):
    """
    Validate that total installment amounts equals net price within tolerance.
    Raises frappe.ValidationError if mismatch exceeds tolerance.
    """
    settings = get_sales_contract_settings()
    if settings and not settings.require_installment_schedule:
        return

    if not contract.installments or not contract.net_price:
        return

    if tolerance_percent is None:
        tolerance_percent = 0.5
        if settings:
            tolerance_percent = flt(settings.installment_amount_tolerance_percent)

    calculate_installment_totals(contract)
    total = flt(contract.total_installment_amount)
    net_price = flt(contract.net_price)

    if net_price <= 0:
        return

    diff_pct = abs(total - net_price) / net_price * 100.0

    if diff_pct > tolerance_percent:
        frappe.throw(
            _(
                "Total installment amount ({0}) does not match net contract price ({1}). "
                "Difference is {2}% which exceeds the allowed tolerance of {3}%."
            ).format(
                frappe.bold(f"{total:,.2f}"),
                frappe.bold(f"{net_price:,.2f}"),
                frappe.bold(f"{diff_pct:.2f}%"),
                frappe.bold(f"{tolerance_percent:.2f}%"),
            )
        )


def generate_default_installments(contract):
    """
    Generate a default two-instalment schedule:
    - Down payment: down_payment_percent of net_price, due today + 30 days
    - Final: remainder, due today + 365 days

    Only generates rows if no installments exist and payment_terms_type is Installment.
    """
    if contract.installments:
        return

    if contract.payment_terms_type != "Installment":
        return

    settings = get_sales_contract_settings()
    dp_pct = contract.down_payment_percent
    if not dp_pct:
        if settings:
            dp_pct = flt(settings.default_down_payment_percent)
    if not dp_pct:
        dp_pct = 10.0

    net = contract.net_price or flt(contract.sale_price) or 0
    dp_amount = net * dp_pct / 100.0
    final_amount = net - dp_amount

    today = nowdate()

    rows = [
        {
            "sequence": 1,
            "label": "Down Payment",
            "installment_type": "Down Payment",
            "due_date": add_days(getdate(today), 30),
            "percentage": dp_pct,
            "amount": dp_amount,
            "installment_status": "Pending",
        },
        {
            "sequence": 2,
            "label": "Final Payment",
            "installment_type": "Handover",
            "due_date": add_days(getdate(today), 365),
            "percentage": 100.0 - dp_pct,
            "amount": final_amount,
            "installment_status": "Pending",
        },
    ]

    for row_dict in rows:
        contract.append("installments", row_dict)


def mark_unit_sold(contract):
    """
    Mark the linked unit as Sold on contract submission.
    Stores previous status for safe rollback on cancellation.
    """
    if not contract.unit:
        return

    unit = frappe.get_doc("Unit", contract.unit)

    if unit.status in FINAL_UNIT_STATUSES:
        frappe.throw(
            _(
                "Unit {0} cannot be sold because its status is {1}."
            ).format(frappe.bold(contract.unit), frappe.bold(unit.status))
        )

    if not contract.previous_unit_status:
        contract.db_set("previous_unit_status", unit.status, update_modified=False)
    if hasattr(unit, "marketing_status") and not contract.previous_marketing_status:
        contract.db_set("previous_marketing_status", unit.marketing_status, update_modified=False)

    values = {"status": "Sold"}
    if frappe.get_meta("Unit").has_field("marketing_status"):
        values["marketing_status"] = "Sold"

    frappe.db.set_value("Unit", contract.unit, values, update_modified=True)

    update_related_counts(contract.real_estate_project, contract.building, contract.floor)


def restore_unit_if_safe(contract):
    """
    Restore the linked unit to its previous status on contract cancellation,
    only if no other active sales contract or reservation exists.
    """
    if not contract.unit:
        return

    from construct_erpnext.real_estate_inventory.reservation_utils import (
        has_active_reservation,
    )

    has_active = has_active_reservation(contract.unit)
    has_contract = has_active_sales_contract(contract.unit, exclude=contract.name)

    if has_active or has_contract:
        return

    if contract.previous_unit_status and contract.previous_unit_status != "Sold":
        values = {"status": contract.previous_unit_status}
        if (
            frappe.get_meta("Unit").has_field("marketing_status")
            and contract.previous_marketing_status
        ):
            values["marketing_status"] = contract.previous_marketing_status
        frappe.db.set_value("Unit", contract.unit, values, update_modified=True)
        update_related_counts(
            contract.real_estate_project,
            contract.building,
            contract.floor,
        )


def convert_reservation_to_contract(reservation_name, contract_name):
    """
    Mark a Unit Reservation as converted to a Sales Contract.
    Called from Sales Contract on_submit.
    """
    if not reservation_name:
        return

    try:
        reservation = frappe.get_doc("Unit Reservation", reservation_name)
    except frappe.DoesNotExistError:
        return

    if reservation.status != ACTIVE_RESERVATION_STATUS:
        return

    reservation.db_set(
        {
            "converted_to_doctype": "Sales Contract",
            "converted_to_document": contract_name,
            "converted_on": now_datetime(),
            "converted_by": frappe.session.user,
            "status": "Converted",
            "workflow_state": "Converted",
        }
    )


def release_unit_from_contract(contract):
    """
    Release the unit from a cancelled sales contract.
    Called from Sales Contract on_cancel.
    """
    if not contract.unit:
        return

    restore_unit_if_safe(contract)


def create_sales_contract_from_reservation(reservation_name):
    """
    Whitelisted method: create a draft Sales Contract from an active sale reservation.

    Input:
        reservation_name: name of a Unit Reservation

    Behavior:
        - Loads Unit Reservation.
        - Ensures status = Reserved and reservation_type = Sale.
        - Creates a draft Sales Contract.
        - Copies unit, project, real estate project, buyer info.
        - Sets sale_price from Unit.expected_sale_price.
        - Generates default installment schedule if required.
        - Does NOT submit automatically.
        - Returns Sales Contract name.

    Access: System Manager, Sales Manager
    """
    if not frappe.has_permission("Unit Reservation", "read"):
        frappe.throw(_("Insufficient permission to read Unit Reservation."))

    if not frappe.has_permission("Sales Contract", "create"):
        frappe.throw(_("Insufficient permission to create Sales Contract."))

    reservation = frappe.get_doc("Unit Reservation", reservation_name)

    if reservation.status != ACTIVE_RESERVATION_STATUS:
        frappe.throw(
            _("Only active reservations can be converted. Reservation {0} is {1}.").format(
                frappe.bold(reservation_name),
                frappe.bold(reservation.status),
            )
        )

    if reservation.reservation_type and reservation.reservation_type != "Sale":
        frappe.throw(
            _("Reservation {0} is of type {1}. Only Sale reservations can be converted.").format(
                frappe.bold(reservation_name),
                frappe.bold(reservation.reservation_type),
            )
        )

    settings = get_sales_contract_settings()

    contract = frappe.new_doc("Sales Contract")
    contract.contract_number = generate_contract_number(settings)
    contract.contract_date = nowdate()
    contract.settings = settings.name if settings else None
    contract.contract_type = "Standard"
    contract.unit_reservation = reservation.name

    contract.real_estate_project = reservation.real_estate_project
    contract.unit = reservation.unit

    contract.customer = reservation.customer
    contract.lead = reservation.lead
    contract.buyer_name = reservation.party_name
    contract.party_type = "Customer" if reservation.customer else ("Lead" if reservation.lead else "Individual")
    contract.mobile_no = reservation.mobile_no
    contract.email = reservation.email

    contract.company = reservation.company
    contract.contract_status = "Draft"
    contract.workflow_state = "Draft"

    fetch_unit_metadata(contract)

    if contract.expected_sale_price:
        contract.sale_price = contract.expected_sale_price

    contract.payment_terms_type = "Installment"

    calculate_contract_amounts(contract)
    generate_default_installments(contract)
    calculate_installment_totals(contract)

    contract.insert(ignore_permissions=True)

    return contract.name


def update_related_counts(real_estate_project=None, building=None, floor=None):
    """Recalculate unit counts on Real Estate Project, Building, and Floor."""
    try:
        from construct_erpnext.real_estate_inventory.inventory_utils import (
            update_related_counts as inv_update,
        )

        inv_update(
            real_estate_project=real_estate_project,
            building=building,
            floor=floor,
        )
    except Exception:
        pass
