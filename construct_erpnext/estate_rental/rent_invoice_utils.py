# SPDX-License-Identifier: MIT
# Rent invoice generation and synchronization for Lease Contracts

import json

import frappe
from frappe import _
from frappe.utils import add_days, flt, getdate, nowdate


RENT_INVOICE_REMARKS = "فاتورة إيجار وحدة عقارية مرتبطة بعقد إيجار"
DEFAULT_RENT_PRICE_LIST = "قائمة أسعار إيجار الوحدات العقارية"


def get_rent_invoice_collection_settings():
	try:
		return frappe.get_single("Rent Invoice Collection Settings")
	except frappe.DoesNotExistError:
		return None


def get_or_create_default_rent_item(company=None):
	settings = get_rent_invoice_collection_settings()
	if settings and settings.default_rent_item:
		return settings.default_rent_item

	item_code = "خدمة إيجار وحدة عقارية"
	if frappe.db.exists("Item", item_code):
		return item_code

	item_group = (
		frappe.db.exists("Item Group", "خدمات المقاولين")
		or frappe.db.exists("Item Group", "Services")
		or frappe.db.exists("Item Group", "All Item Groups")
	)
	uom = (
		frappe.db.exists("UOM", "عدد")
		or frappe.db.exists("UOM", "Nos")
		or frappe.db.get_value("UOM", {}, "name")
	)
	if not item_group or not uom:
		frappe.throw(
			_(
				"Cannot create default rent item because Item Group or UOM is missing. "
				"Please configure Default Rent Item in Rent Invoice Collection Settings."
			)
		)

	item = frappe.get_doc(
		{
			"doctype": "Item",
			"item_code": item_code,
			"item_name": item_code,
			"item_group": item_group,
			"stock_uom": uom,
			"is_stock_item": 0,
			"is_sales_item": 1,
			"is_purchase_item": 0,
			"include_item_in_manufacturing": 0,
			"description": _("Service item for real estate unit rent invoices."),
		}
	)
	item.insert(ignore_permissions=True)

	if settings:
		settings.db_set("default_rent_item", item.name, update_modified=False)

	return item.name


def get_or_create_default_rent_price_list(currency):
	default_price_list = frappe.db.get_single_value("Selling Settings", "selling_price_list")
	if default_price_list:
		return default_price_list

	existing = frappe.db.get_value("Price List", {"name": DEFAULT_RENT_PRICE_LIST, "selling": 1}, "name")
	if existing:
		return existing

	price_list = frappe.new_doc("Price List")
	price_list.price_list_name = DEFAULT_RENT_PRICE_LIST
	price_list.selling = 1
	price_list.buying = 0
	price_list.currency = currency
	price_list.enabled = 1
	price_list.insert(ignore_permissions=True)
	return price_list.name


@frappe.whitelist()
def create_invoice_from_rent_schedule(lease_contract, rent_rows=None, submit=0):
	return create_rent_invoice_from_schedule(
		lease_contract,
		rent_rows=_parse_rent_rows(rent_rows),
		submit=bool(flt(submit)),
	)


@frappe.whitelist()
def submit_rent_invoice_from_schedule_invoice(sales_invoice_name):
	invoice = frappe.get_doc("Sales Invoice", sales_invoice_name)
	if invoice.docstatus != 0:
		frappe.throw(_("Sales Invoice {0} must be Draft before submission.").format(invoice.name))

	rows = _get_rent_rows_for_invoice(invoice.name)
	if not rows:
		frappe.throw(_("Sales Invoice {0} is not linked to a Rent Schedule row.").format(invoice.name))

	_validate_invoice_for_rent_submission(invoice, rows)
	invoice.submit()
	sync_rent_schedule_from_sales_invoice(invoice)
	return invoice.name


def create_rent_invoice_from_schedule(lease_contract, rent_rows=None, submit=False):
	settings = get_rent_invoice_collection_settings()
	if settings and not settings.enable_rent_invoice_generation:
		frappe.throw(_("Rent invoice generation is disabled in Rent Invoice Collection Settings."))

	lease = frappe.get_doc("Lease Contract", lease_contract)
	_validate_lease_for_invoice(lease, settings)
	rows = _get_invoiceable_rent_rows(lease, rent_rows, settings)
	if not rows:
		frappe.throw(_("No invoiceable Rent Schedule rows were found for Lease Contract {0}.").format(lease.name))

	if settings and not settings.allow_grouped_rent_invoice and len(rows) > 1:
		frappe.throw(_("Grouped rent invoices are disabled in Rent Invoice Collection Settings."))

	item_code = get_or_create_default_rent_item(lease.company)
	company_currency = frappe.db.get_value("Company", lease.company, "default_currency") if lease.company else None
	currency = company_currency if settings and settings.use_company_default_currency else lease.currency
	currency = currency or company_currency or "YER"

	invoice = frappe.new_doc("Sales Invoice")
	invoice.customer = lease.customer
	invoice.company = lease.company
	invoice.currency = currency
	invoice.selling_price_list = get_or_create_default_rent_price_list(currency)
	invoice.price_list_currency = currency
	if company_currency and currency == company_currency:
		_set_if_has_field(invoice, "conversion_rate", 1)
		_set_if_has_field(invoice, "plc_conversion_rate", 1)
	invoice.posting_date = nowdate()
	earliest_due_date = min(row.due_date for row in rows if row.due_date) if any(row.due_date for row in rows) else nowdate()
	invoice.due_date = max(getdate(earliest_due_date), getdate(invoice.posting_date))
	invoice.remarks = RENT_INVOICE_REMARKS

	_set_if_has_field(invoice, "project", lease.project)
	_set_if_has_field(invoice, "unit", lease.unit)
	_set_if_has_field(invoice, "cost_center", _get_default_cost_center(lease.company))
	_set_if_has_field(invoice, "lease_contract", lease.name)
	_set_if_has_field(invoice, "real_estate_project", lease.real_estate_project)

	for row in rows:
		description = _("Real estate unit rent for period {0} under Lease Contract {1}").format(
			row.label or row.sequence or row.name,
			lease.name,
		)
		item = {
			"item_code": item_code,
			"item_name": item_code,
			"description": description,
			"qty": 1,
			"rate": flt(row.rent_amount),
			"price_list_rate": flt(row.rent_amount),
			"amount": flt(row.rent_amount),
		}
		_set_item_defaults(item, lease, row)
		invoice.append("items", item)

	invoice.insert(ignore_permissions=False)

	for row in rows:
		_update_rent_schedule_row(
			row.name,
			{
				"sales_invoice": invoice.name,
				"rent_status": "Draft Invoice",
				"invoice_amount": flt(row.rent_amount),
				"paid_amount": 0,
				"outstanding_amount": flt(row.rent_amount),
				"invoiced_on": nowdate(),
			},
		)

	_update_lease_invoice_flags(lease.name, invoice.name)
	recalculate_lease_collection_status(lease.name)

	if submit and settings and settings.auto_submit_rent_invoice:
		invoice.submit()
		sync_rent_schedule_from_sales_invoice(invoice)

	return invoice.name


def validate_rent_invoice_dimensions(sales_invoice, method=None):
	for item in sales_invoice.items:
		lease_name = getattr(item, "lease_contract", None)
		if not lease_name:
			continue
		lease = frappe.get_cached_doc("Lease Contract", lease_name)
		_set_if_has_field(item, "unit", lease.unit, only_if_empty=True)
		_set_if_has_field(item, "project", lease.project, only_if_empty=True)
		_set_if_has_field(item, "cost_center", _get_default_cost_center(lease.company), only_if_empty=True)
		_set_if_has_field(item, "real_estate_project", lease.real_estate_project, only_if_empty=True)
		_set_if_has_field(item, "unit_reservation", lease.unit_reservation, only_if_empty=True)

	settings = get_rent_invoice_collection_settings()
	if settings and settings.require_unit_on_invoice_item:
		for item in sales_invoice.items:
			if getattr(item, "lease_contract", None) and not getattr(item, "unit", None):
				frappe.throw(_("Unit is required on Sales Invoice Item for Lease Contract rent invoices."))


def sync_rent_schedule_from_sales_invoice(sales_invoice, method=None):
	if isinstance(sales_invoice, str):
		sales_invoice = frappe.get_doc("Sales Invoice", sales_invoice)

	rows = _get_rent_rows_for_invoice(sales_invoice.name)
	if not rows:
		return

	invoice_amount_total = sum(flt(row.rent_amount) for row in rows)
	paid_total = 0
	outstanding_total = invoice_amount_total
	if sales_invoice.docstatus == 1:
		paid_total = max(flt(sales_invoice.grand_total) - flt(sales_invoice.outstanding_amount), 0)
		outstanding_total = flt(sales_invoice.outstanding_amount)

	leases = set()
	for row in rows:
		ratio = (flt(row.rent_amount) / invoice_amount_total) if invoice_amount_total else 0
		paid = min(flt(row.rent_amount), paid_total * ratio)
		outstanding = max(flt(row.rent_amount) - paid, 0)
		status = _get_rent_status(sales_invoice, paid, outstanding, row)
		values = {
			"rent_status": status,
			"invoice_amount": flt(row.rent_amount),
			"paid_amount": paid,
			"outstanding_amount": outstanding,
			"overdue_days": _get_overdue_days(row.due_date, outstanding),
		}
		if paid and not outstanding:
			values["paid_on"] = nowdate()
		_update_rent_schedule_row(row.name, values)
		leases.add(row.parent)

	for lease in leases:
		recalculate_lease_collection_status(lease)


def release_rent_schedule_on_invoice_cancel(sales_invoice, method=None):
	if isinstance(sales_invoice, str):
		sales_invoice = frappe.get_doc("Sales Invoice", sales_invoice)

	rows = _get_rent_rows_for_invoice(sales_invoice.name)
	if not rows:
		return

	leases = set()
	for row in rows:
		_update_rent_schedule_row(
			row.name,
			{
				"sales_invoice": None,
				"payment_entry": None,
				"rent_status": _default_open_rent_status(row.due_date),
				"invoice_amount": 0,
				"paid_amount": 0,
				"outstanding_amount": flt(row.rent_amount),
				"invoiced_on": None,
				"paid_on": None,
				"overdue_days": 0,
			},
		)
		leases.add(row.parent)

	for lease in leases:
		recalculate_lease_collection_status(lease)


def recalculate_lease_collection_status(lease_contract):
	if not lease_contract or not frappe.db.exists("Lease Contract", lease_contract):
		return

	rows = frappe.get_all(
		"Rent Schedule",
		filters={"parenttype": "Lease Contract", "parent": lease_contract},
		fields=[
			"name",
			"rent_amount",
			"invoice_amount",
			"paid_amount",
			"outstanding_amount",
			"rent_status",
			"sales_invoice",
			"payment_entry",
		],
	)
	total = sum(flt(row.rent_amount) for row in rows)
	invoiced = sum(flt(row.invoice_amount) for row in rows)
	collected = sum(flt(row.paid_amount) for row in rows)
	outstanding = sum(
		flt(row.outstanding_amount) if row.outstanding_amount is not None else flt(row.rent_amount)
		for row in rows
	)

	if collected > 0 and outstanding > 0:
		status = "Partially Collected"
	elif invoiced <= 0:
		status = "Not Invoiced"
	elif invoiced + 0.01 < total:
		status = "Partially Invoiced"
	elif collected <= 0:
		status = "Fully Invoiced"
	else:
		status = "Fully Collected"

	if any(row.rent_status == "Overdue" for row in rows):
		status = "Overdue"

	values = {
		"total_scheduled_rent": total,
		"total_invoiced_rent": invoiced,
		"total_collected_rent": collected,
		"total_outstanding_rent": outstanding,
		"rent_collection_status": status,
		"invoices_created": 1 if any(row.sales_invoice for row in rows) else 0,
	}
	first_invoice = next((row.sales_invoice for row in rows if row.sales_invoice), None)
	latest_payment = next((row.payment_entry for row in rows if row.payment_entry), None)
	if first_invoice:
		values["first_rent_invoice"] = first_invoice
	if latest_payment:
		values["latest_payment_entry"] = latest_payment

	for fieldname, value in values.items():
		if frappe.get_meta("Lease Contract").has_field(fieldname):
			frappe.db.set_value("Lease Contract", lease_contract, fieldname, value, update_modified=False)


@frappe.whitelist()
def refresh_lease_collection_status(lease_contract):
	recalculate_lease_collection_status(lease_contract)
	return lease_contract


@frappe.whitelist()
def mark_overdue_rent_schedules():
	settings = get_rent_invoice_collection_settings()
	grace_days = settings.overdue_grace_days if settings else 0
	today = getdate(nowdate())
	leases = set()
	rows = frappe.get_all(
		"Rent Schedule",
		filters={"parenttype": "Lease Contract", "rent_status": ["not in", ("Paid", "Waived", "Cancelled")]},
		fields=["name", "parent", "due_date", "outstanding_amount", "rent_amount"],
	)
	for row in rows:
		if not row.due_date:
			continue
		overdue_days = (today - add_days(getdate(row.due_date), grace_days or 0)).days
		outstanding = flt(row.outstanding_amount) if row.outstanding_amount is not None else flt(row.rent_amount)
		if overdue_days <= 0 or outstanding <= 0:
			continue
		_update_rent_schedule_row(row.name, {"rent_status": "Overdue", "overdue_days": overdue_days})
		leases.add(row.parent)

	for lease in leases:
		recalculate_lease_collection_status(lease)
	return {"updated_leases": len(leases)}


def _parse_rent_rows(rent_rows):
	if not rent_rows:
		return None
	if isinstance(rent_rows, str):
		try:
			return json.loads(rent_rows)
		except ValueError:
			return [row.strip() for row in rent_rows.split(",") if row.strip()]
	return rent_rows


def _validate_lease_for_invoice(lease, settings):
	if lease.docstatus == 2:
		frappe.throw(_("Cancelled Lease Contract cannot be invoiced."))
	if settings and settings.require_customer_on_lease and not lease.customer:
		frappe.throw(_("Customer is required on Lease Contract before rent invoice generation."))
	if not lease.unit:
		frappe.throw(_("Unit is required on Lease Contract before rent invoice generation."))
	if not lease.company:
		frappe.throw(_("Company is required on Lease Contract before rent invoice generation."))


def _get_invoiceable_rent_rows(lease, requested_rows, settings):
	requested = set(requested_rows or [])
	rows = []
	for row in lease.rent_schedule:
		if requested and row.name not in requested and str(row.sequence) not in requested:
			continue
		if row.rent_status in ("Paid", "Waived", "Cancelled"):
			continue
		if settings and settings.block_duplicate_invoice_for_rent_schedule and row.sales_invoice:
			if frappe.db.get_value("Sales Invoice", row.sales_invoice, "docstatus") != 2:
				frappe.throw(_("Rent Schedule row {0} is already linked to active Sales Invoice {1}.").format(row.sequence or row.name, row.sales_invoice))
		rows.append(row)
	return rows


def _validate_invoice_for_rent_submission(invoice, rows):
	for item in invoice.items:
		if getattr(item, "lease_contract", None) and not getattr(item, "unit", None):
			frappe.throw(_("Unit is required on Sales Invoice Item before submitting rent invoice."))

	for row in rows:
		duplicates = frappe.get_all(
			"Rent Schedule",
			filters={
				"parenttype": "Lease Contract",
				"name": ["!=", row.name],
				"sales_invoice": invoice.name,
			},
			fields=["name"],
			limit=1,
		)
		if duplicates:
			frappe.throw(_("Duplicate Rent Schedule linkage found for Sales Invoice {0}.").format(invoice.name))


def _get_rent_rows_for_invoice(invoice_name):
	return frappe.get_all(
		"Rent Schedule",
		filters={"parenttype": "Lease Contract", "sales_invoice": invoice_name},
		fields=[
			"name",
			"parent",
			"sequence",
			"label",
			"due_date",
			"rent_amount",
			"rent_status",
			"payment_entry",
		],
		order_by="sequence asc, idx asc",
	)


def _set_item_defaults(item, lease, row):
	item["cost_center"] = _get_default_cost_center(lease.company)
	_set_dict_if_has_field("Sales Invoice Item", item, "project", lease.project)
	_set_dict_if_has_field("Sales Invoice Item", item, "unit", lease.unit)
	_set_dict_if_has_field("Sales Invoice Item", item, "lease_contract", lease.name)
	_set_dict_if_has_field("Sales Invoice Item", item, "rent_schedule_reference", row.name)
	_set_dict_if_has_field("Sales Invoice Item", item, "real_estate_project", lease.real_estate_project)
	_set_dict_if_has_field("Sales Invoice Item", item, "unit_reservation", lease.unit_reservation)


def _set_if_has_field(doc, fieldname, value, only_if_empty=False):
	if doc.meta.has_field(fieldname) and (not only_if_empty or not doc.get(fieldname)):
		doc.set(fieldname, value)


def _set_dict_if_has_field(doctype, target, fieldname, value):
	if frappe.get_meta(doctype).has_field(fieldname):
		target[fieldname] = value


def _get_default_cost_center(company):
	if not company:
		return None
	return frappe.db.get_value("Company", company, "cost_center")


def _update_rent_schedule_row(row_name, values):
	meta = frappe.get_meta("Rent Schedule")
	for fieldname, value in values.items():
		if meta.has_field(fieldname):
			frappe.db.set_value("Rent Schedule", row_name, fieldname, value, update_modified=False)


def _update_lease_invoice_flags(lease_contract, invoice_name):
	for fieldname, value in {
		"first_rent_invoice": invoice_name,
		"invoices_created": 1,
	}.items():
		if frappe.get_meta("Lease Contract").has_field(fieldname):
			current = frappe.db.get_value("Lease Contract", lease_contract, fieldname)
			if not current:
				frappe.db.set_value("Lease Contract", lease_contract, fieldname, value, update_modified=False)


def _get_rent_status(invoice, paid, outstanding, row):
	if invoice.docstatus == 0:
		return "Draft Invoice"
	if invoice.docstatus == 2:
		return _default_open_rent_status(row.due_date)
	if outstanding <= 0:
		return "Paid"
	if paid > 0:
		return "Partially Paid"
	if _get_overdue_days(row.due_date, outstanding) > 0:
		return "Overdue"
	return "Invoiced"


def _default_open_rent_status(due_date):
	if due_date and getdate(due_date) <= getdate(nowdate()):
		return "Due"
	return "Pending"


def _get_overdue_days(due_date, outstanding):
	if not due_date or flt(outstanding) <= 0:
		return 0
	overdue = (getdate(nowdate()) - getdate(due_date)).days
	return max(overdue, 0)
