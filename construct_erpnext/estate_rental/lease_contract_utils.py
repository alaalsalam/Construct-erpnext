# SPDX-License-Identifier: MIT
# Estate Rental services for Lease Contract and Rent Schedule

import frappe
from frappe import _
from frappe.model.naming import make_autoname
from frappe.utils import add_days, add_months, date_diff, flt, getdate, now_datetime, nowdate


FINAL_UNIT_STATUSES = {"Sold", "Rented", "Blocked", "Under Maintenance"}
ACTIVE_LEASE_STATUSES = ("Under Review", "Approved", "Active")
ACTIVE_RESERVATION_STATUS = "Reserved"


def get_lease_contract_settings():
	try:
		return frappe.get_single("Lease Contract Settings")
	except frappe.DoesNotExistError:
		return None


def generate_contract_number(settings=None):
	if settings is None:
		settings = get_lease_contract_settings()
	prefix = (settings.contract_number_prefix if settings else None) or "LC"
	return make_autoname(f"{prefix.strip() or 'LC'}-.YYYY.-.#####")


def get_active_lease_contract_for_unit(unit, exclude=None):
	if not unit:
		return None

	filters = {"unit": unit, "lease_status": ["in", ACTIVE_LEASE_STATUSES]}
	if exclude:
		filters["name"] = ["!=", exclude]

	return frappe.db.get_value(
		"Lease Contract",
		filters,
		"name",
		order_by="contract_date desc",
	)


def fetch_unit_metadata(contract):
	if not contract.unit:
		return

	unit = frappe.get_cached_doc("Unit", contract.unit)
	contract.real_estate_project = contract.real_estate_project or unit.real_estate_project
	contract.project = unit.project
	contract.building = unit.building
	contract.floor = unit.floor
	contract.unit_type = unit.unit_type
	contract.unit_area = unit.area
	contract.expected_monthly_rent = unit.expected_monthly_rent
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


def calculate_lease_amounts(contract):
	if not (contract.lease_start_date and contract.lease_end_date):
		contract.total_contract_rent = 0
		return

	months = _months_between(contract.lease_start_date, contract.lease_end_date)
	contract.total_contract_rent = flt(contract.monthly_rent) * months

	if contract.security_deposit_amount is None:
		settings = get_lease_contract_settings()
		deposit_months = flt(settings.default_security_deposit_months) if settings else 0
		contract.security_deposit_amount = flt(contract.monthly_rent) * deposit_months


def generate_rent_schedule(contract):
	if contract.rent_schedule:
		return
	if not (contract.lease_start_date and contract.lease_end_date and flt(contract.monthly_rent) > 0):
		return

	frequency = contract.billing_frequency or "Monthly"
	months_per_row = {
		"Monthly": 1,
		"Quarterly": 3,
		"Semi Annual": 6,
		"Annual": 12,
	}.get(frequency, 1)

	start = getdate(contract.lease_start_date)
	end = getdate(contract.lease_end_date)
	sequence = 1
	current_start = start

	while current_start <= end:
		next_start = add_months(current_start, months_per_row)
		period_end = min(add_days(next_start, -1), end)
		period_months = max(_months_between(current_start, period_end), 0)
		amount = flt(contract.monthly_rent) * period_months
		if amount <= 0:
			amount = flt(contract.monthly_rent) * months_per_row

		contract.append(
			"rent_schedule",
			{
				"sequence": sequence,
				"rent_period_start": current_start,
				"rent_period_end": period_end,
				"due_date": current_start,
				"label": _("Rent Period {0}").format(sequence),
				"rent_amount": amount,
				"rent_status": "Pending",
				"outstanding_amount": amount,
			},
		)
		sequence += 1
		current_start = next_start


def calculate_rent_schedule_totals(contract):
	total = sum(flt(row.rent_amount) for row in contract.rent_schedule or [])
	invoiced = sum(flt(row.invoice_amount) for row in contract.rent_schedule or [])
	collected = sum(flt(row.paid_amount) for row in contract.rent_schedule or [])
	outstanding = sum(
		flt(row.outstanding_amount) if row.outstanding_amount is not None else flt(row.rent_amount)
		for row in contract.rent_schedule or []
	)

	contract.total_scheduled_rent = total
	contract.total_invoiced_rent = invoiced
	contract.total_collected_rent = collected
	contract.total_outstanding_rent = outstanding

	if invoiced <= 0:
		contract.rent_collection_status = "Not Invoiced"
	elif invoiced + 0.01 < total:
		contract.rent_collection_status = "Partially Invoiced"
	elif collected <= 0:
		contract.rent_collection_status = "Fully Invoiced"
	elif outstanding > 0:
		contract.rent_collection_status = "Partially Collected"
	else:
		contract.rent_collection_status = "Fully Collected"

	if any(row.rent_status == "Overdue" for row in contract.rent_schedule or []):
		contract.rent_collection_status = "Overdue"


def validate_rent_schedule_totals(contract):
	settings = get_lease_contract_settings()
	if settings and not settings.require_rent_schedule:
		return

	if not contract.rent_schedule:
		frappe.throw(_("Rent Schedule is required for this Lease Contract."))

	calculate_rent_schedule_totals(contract)
	calculate_lease_amounts(contract)
	total = flt(contract.total_scheduled_rent)
	expected = flt(contract.total_contract_rent)
	if not expected:
		return

	diff = abs(total - expected)
	if diff > 0.5:
		frappe.throw(
			_("Total scheduled rent ({0}) does not match total contract rent ({1}).").format(
				frappe.bold(f"{total:,.2f}"),
				frappe.bold(f"{expected:,.2f}"),
			)
		)


def mark_unit_rented(contract):
	if not contract.unit:
		return

	unit = frappe.get_doc("Unit", contract.unit)
	if unit.status in FINAL_UNIT_STATUSES and unit.status != "Rented":
		frappe.throw(
			_("Unit {0} cannot be leased because its status is {1}.").format(
				frappe.bold(contract.unit),
				frappe.bold(unit.status),
			)
		)

	if not contract.previous_unit_status:
		contract.db_set("previous_unit_status", unit.status, update_modified=False)
	if frappe.get_meta("Unit").has_field("marketing_status") and not contract.previous_marketing_status:
		contract.db_set("previous_marketing_status", unit.marketing_status, update_modified=False)

	values = {"status": "Rented"}
	if frappe.get_meta("Unit").has_field("marketing_status"):
		values["marketing_status"] = "Rented"
	frappe.db.set_value("Unit", contract.unit, values, update_modified=True)
	update_related_counts(contract.real_estate_project, contract.building, contract.floor)


def release_unit_from_lease_if_safe(contract):
	if not contract.unit:
		return False

	from construct_erpnext.real_estate_inventory.reservation_utils import has_active_reservation

	if has_active_reservation(contract.unit):
		return False
	if get_active_lease_contract_for_unit(contract.unit, exclude=contract.name):
		return False

	unit = frappe.get_doc("Unit", contract.unit)
	if unit.status in {"Sold", "Blocked", "Under Maintenance"}:
		return False

	values = {"status": contract.previous_unit_status or "Available"}
	if values["status"] in ("Rented", "Sold", "Blocked", "Under Maintenance"):
		values["status"] = "Available"
	if frappe.get_meta("Unit").has_field("marketing_status"):
		values["marketing_status"] = contract.previous_marketing_status or values["status"]
		if values["marketing_status"] in ("Rented", "Sold", "Blocked", "Under Maintenance"):
			values["marketing_status"] = "Available"
	frappe.db.set_value("Unit", contract.unit, values, update_modified=True)
	update_related_counts(contract.real_estate_project, contract.building, contract.floor)
	return True


def convert_reservation_to_lease(reservation_name, contract_name):
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
			"converted_to_doctype": "Lease Contract",
			"converted_to_document": contract_name,
			"converted_on": now_datetime(),
			"converted_by": frappe.session.user,
			"status": "Converted",
			"workflow_state": "Converted",
		}
	)


@frappe.whitelist()
def create_lease_contract_from_reservation(reservation_name):
	if not frappe.has_permission("Unit Reservation", "read"):
		frappe.throw(_("Insufficient permission to read Unit Reservation."))
	if not frappe.has_permission("Lease Contract", "create"):
		frappe.throw(_("Insufficient permission to create Lease Contract."))

	reservation = frappe.get_doc("Unit Reservation", reservation_name)
	if reservation.status != ACTIVE_RESERVATION_STATUS:
		frappe.throw(_("Only active reservations can be converted to Lease Contract."))
	if reservation.reservation_type != "Rent":
		frappe.throw(_("Only Rent reservations can be converted to Lease Contract."))

	settings = get_lease_contract_settings()
	lease = frappe.new_doc("Lease Contract")
	lease.contract_number = generate_contract_number(settings)
	lease.contract_date = nowdate()
	lease.settings = settings.name if settings else None
	lease.lease_type = "Long Term Rent"
	lease.unit_reservation = reservation.name
	lease.real_estate_project = reservation.real_estate_project
	lease.unit = reservation.unit
	lease.customer = reservation.customer
	lease.lead = reservation.lead
	lease.tenant_name = reservation.party_name
	lease.party_type = "Customer" if reservation.customer else ("Lead" if reservation.lead else "Individual")
	lease.mobile_no = reservation.mobile_no
	lease.email = reservation.email
	lease.company = reservation.company
	lease.lease_status = "Draft"
	lease.workflow_state = "Draft"
	lease.lease_start_date = nowdate()
	months = settings.default_lease_period_months if settings else 12
	lease.lease_end_date = add_days(add_months(getdate(lease.lease_start_date), months or 12), -1)
	lease.billing_frequency = (settings.default_billing_frequency if settings else None) or "Monthly"

	fetch_unit_metadata(lease)
	if lease.expected_monthly_rent:
		lease.monthly_rent = lease.expected_monthly_rent

	calculate_lease_amounts(lease)
	if not settings or settings.auto_generate_rent_schedule:
		generate_rent_schedule(lease)
	calculate_rent_schedule_totals(lease)
	lease.insert(ignore_permissions=True)
	return lease.name


def update_related_counts(real_estate_project=None, building=None, floor=None):
	try:
		from construct_erpnext.real_estate_inventory.inventory_utils import update_related_counts as inv_update

		inv_update(real_estate_project=real_estate_project, building=building, floor=floor)
	except Exception:
		pass


def _months_between(start_date, end_date):
	start = getdate(start_date)
	end = getdate(end_date)
	if end < start:
		return 0
	whole_months = (end.year - start.year) * 12 + (end.month - start.month)
	anniversary_end = add_days(add_months(start, whole_months), -1)
	if anniversary_end == end:
		return max(whole_months, 1)
	if anniversary_end < end:
		return whole_months + ((date_diff(end, anniversary_end)) / 30.0)
	return max((date_diff(end, start) + 1) / 30.0, 0)
