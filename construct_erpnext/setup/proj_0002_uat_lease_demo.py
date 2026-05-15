import frappe
from frappe.utils import add_days, nowdate
from frappe.model.workflow import apply_workflow

from construct_erpnext.estate_rental.lease_contract_utils import create_lease_contract_from_reservation


UAT_CUSTOMER = "مستأجر تجاري محتمل"
UAT_UNIT = "BLD-PROJ-000-001-S-G-02"
UAT_PROJECT = "PROJ-0002"
UAT_REAL_ESTATE_PROJECT = "REP-2026-00002"
UAT_REMARKS = "عقد إيجار تشغيلي لعرض دورة الإيجار على العميل"


@frappe.whitelist()
def create_proj_0002_uat_lease_scenario():
	unit = _select_unit()
	existing_lease = _get_existing_lease(unit)
	if existing_lease:
		return _lease_summary(existing_lease)

	customer = _ensure_customer()
	reservation = _get_or_create_rent_reservation(unit, customer)
	if reservation.docstatus == 0:
		reservation = apply_workflow(reservation, "Reserve")

	lease_name = create_lease_contract_from_reservation(reservation.name)
	lease = frappe.get_doc("Lease Contract", lease_name)
	lease.remarks = UAT_REMARKS
	lease.security_deposit_amount = lease.monthly_rent
	lease.save()

	lease = apply_workflow(lease, "Submit for Review")
	lease = apply_workflow(lease, "Approve")
	lease = apply_workflow(lease, "Activate")

	return _lease_summary(lease.name)


def _select_unit():
	if not frappe.db.exists("Unit", UAT_UNIT):
		frappe.throw(f"UAT Unit {UAT_UNIT} does not exist.")
	unit = frappe.get_doc("Unit", UAT_UNIT)
	if unit.real_estate_project != UAT_REAL_ESTATE_PROJECT or unit.project != UAT_PROJECT:
		frappe.throw(f"UAT Unit {UAT_UNIT} is not linked to {UAT_PROJECT} / {UAT_REAL_ESTATE_PROJECT}.")
	if unit.status in ("Sold", "Rented", "Blocked", "Under Maintenance"):
		existing_lease = _get_existing_lease(unit.name)
		if existing_lease:
			return unit.name
		frappe.throw(f"UAT Unit {UAT_UNIT} is not rentable because status is {unit.status}.")
	return unit.name


def _ensure_customer():
	if frappe.db.exists("Customer", UAT_CUSTOMER):
		return UAT_CUSTOMER

	customer_group = frappe.db.get_value("Customer Group", {}, "name")
	territory = frappe.db.get_value("Territory", {}, "name")
	if not customer_group or not territory:
		frappe.throw("Customer Group and Territory are required before creating the UAT tenant customer.")

	customer = frappe.new_doc("Customer")
	customer.customer_name = UAT_CUSTOMER
	customer.customer_type = "Individual"
	customer.customer_group = customer_group
	customer.territory = territory
	customer.insert()
	return customer.name


def _get_or_create_rent_reservation(unit, customer):
	existing = frappe.db.get_value(
		"Unit Reservation",
		{
			"unit": unit,
			"reservation_type": "Rent",
			"customer": customer,
			"status": ["in", ("Reserved", "Converted")],
		},
		"name",
		order_by="creation desc",
	)
	if existing:
		return frappe.get_doc("Unit Reservation", existing)

	reservation = frappe.new_doc("Unit Reservation")
	reservation.reservation_type = "Rent"
	reservation.valid_from = nowdate()
	reservation.valid_until = add_days(nowdate(), 7)
	reservation.unit = unit
	reservation.customer = customer
	reservation.party_name = UAT_CUSTOMER
	reservation.remarks = "حجز إيجار مبدئي لاختبار دورة الإيجار ضمن مشروع العرض الرئيسي"
	reservation.insert()
	return reservation


def _get_existing_lease(unit):
	return frappe.db.get_value(
		"Lease Contract",
		{"unit": unit, "lease_status": ["in", ("Approved", "Active")], "docstatus": 1},
		"name",
		order_by="creation desc",
	)


def _lease_summary(lease_name):
	lease = frappe.get_doc("Lease Contract", lease_name)
	reservation_status = None
	if lease.unit_reservation:
		reservation_status = frappe.db.get_value("Unit Reservation", lease.unit_reservation, "status")
	return {
		"lease_contract": lease.name,
		"unit": lease.unit,
		"unit_status": frappe.db.get_value("Unit", lease.unit, "status"),
		"unit_reservation": lease.unit_reservation,
		"reservation_status": reservation_status,
		"lease_status": lease.lease_status,
		"workflow_state": lease.workflow_state,
		"docstatus": lease.docstatus,
		"monthly_rent": lease.monthly_rent,
		"rent_schedule_rows": len(lease.rent_schedule or []),
		"total_scheduled_rent": lease.total_scheduled_rent,
	}
