# SPDX-License-Identifier: MIT
# Sales Invoice generation and synchronization for real estate Sales Contracts

import json

import frappe
from frappe import _
from frappe.utils import add_days, cstr, flt, getdate, nowdate


ACTIVE_CONTRACT_STATUSES = {"Approved", "Active"}
INVOICE_REMARKS = "فاتورة قسط بيع وحدة عقارية مرتبطة بعقد بيع"
DEFAULT_SELLING_PRICE_LIST = "قائمة أسعار بيع الوحدات العقارية"


def get_sales_invoice_collection_settings():
	"""Return Sales Invoice Collection Settings singleton."""
	try:
		return frappe.get_single("Sales Invoice Collection Settings")
	except frappe.DoesNotExistError:
		return None


def get_or_create_default_sales_item(company=None):
	"""Return the default non-stock item used for installment Sales Invoices."""
	settings = get_sales_invoice_collection_settings()
	if settings and settings.default_sales_item:
		return settings.default_sales_item

	item_code = "خدمة بيع وحدة عقارية"
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
				"Cannot create default sales item because Item Group or UOM is missing. "
				"Please configure Default Sales Item in Sales Invoice Collection Settings."
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
			"description": _("Service item for real estate unit sales invoices."),
		}
	)
	item.insert(ignore_permissions=True)

	if settings:
		settings.db_set("default_sales_item", item.name, update_modified=False)

	return item.name


def get_or_create_default_selling_price_list(currency):
	"""Return a selling price list for real estate invoices."""
	default_price_list = frappe.db.get_single_value("Selling Settings", "selling_price_list")
	if default_price_list:
		return default_price_list

	existing = frappe.db.get_value(
		"Price List",
		{"name": DEFAULT_SELLING_PRICE_LIST, "selling": 1},
		"name",
	)
	if existing:
		return existing

	price_list = frappe.new_doc("Price List")
	price_list.price_list_name = DEFAULT_SELLING_PRICE_LIST
	price_list.selling = 1
	price_list.buying = 0
	price_list.currency = currency
	price_list.enabled = 1
	price_list.insert(ignore_permissions=True)
	return price_list.name


@frappe.whitelist()
def create_invoice_from_contract_installments(sales_contract, installment_rows=None, submit=0):
	"""Whitelisted wrapper to create Sales Invoice from selected installment rows."""
	return create_sales_invoice_from_installments(
		sales_contract,
		installment_rows=_parse_installment_rows(installment_rows),
		submit=bool(flt(submit)),
	)


@frappe.whitelist()
def submit_sales_invoice_from_contract_invoice(sales_invoice_name):
	"""Submit one Sales Contract invoice through normal ERPNext accounting validation."""
	invoice = frappe.get_doc("Sales Invoice", sales_invoice_name)
	if invoice.docstatus != 0:
		frappe.throw(_("Sales Invoice {0} must be Draft before submission.").format(invoice.name))

	installments = _get_installments_for_invoice(invoice.name)
	if not installments:
		frappe.throw(_("Sales Invoice {0} is not linked to a Sales Contract installment.").format(invoice.name))

	_validate_invoice_for_contract_submission(invoice, installments)
	invoice.submit()
	sync_installments_from_sales_invoice(invoice)
	return invoice.name


def create_sales_invoice_from_installments(sales_contract, installment_rows=None, submit=False):
	"""Create a draft Sales Invoice from one or more Sales Contract installment rows."""
	settings = get_sales_invoice_collection_settings()
	if settings and not settings.enable_sales_invoice_generation:
		frappe.throw(_("Sales Invoice generation is disabled in Sales Invoice Collection Settings."))

	contract = frappe.get_doc("Sales Contract", sales_contract)
	_validate_contract_for_invoice(contract, settings)

	rows = _get_invoiceable_installments(contract, installment_rows, settings)
	if not rows:
		frappe.throw(_("No invoiceable installment rows were found for Sales Contract {0}.").format(contract.name))

	if settings and not settings.allow_grouped_installment_invoice and len(rows) > 1:
		frappe.throw(_("Grouped installment invoices are disabled in Sales Invoice Collection Settings."))

	item_code = get_or_create_default_sales_item(contract.company)
	company = contract.company
	company_currency = frappe.db.get_value("Company", company, "default_currency") if company else None
	currency = company_currency if settings and settings.use_company_default_currency else contract.currency
	currency = currency or company_currency or "YER"

	invoice = frappe.new_doc("Sales Invoice")
	invoice.customer = contract.customer
	invoice.company = company
	invoice.currency = currency
	invoice.selling_price_list = get_or_create_default_selling_price_list(currency)
	invoice.price_list_currency = currency
	if company_currency and currency == company_currency:
		_set_if_has_field(invoice, "conversion_rate", 1)
		_set_if_has_field(invoice, "plc_conversion_rate", 1)
	invoice.posting_date = nowdate()
	invoice.due_date = min(row.due_date for row in rows if row.due_date) if any(row.due_date for row in rows) else nowdate()
	invoice.remarks = INVOICE_REMARKS

	_set_if_has_field(invoice, "project", contract.project)
	_set_if_has_field(invoice, "unit", contract.unit)
	_set_if_has_field(invoice, "cost_center", _get_default_cost_center(company))
	_set_if_has_field(invoice, "sales_contract", contract.name)
	_set_if_has_field(invoice, "real_estate_project", contract.real_estate_project)

	for row in rows:
		description = _(
			"Real estate unit sales installment {0} for contract {1}"
		).format(row.installment_number or row.sequence or row.name, contract.name)
		item = {
			"item_code": item_code,
			"item_name": item_code,
			"description": description,
			"qty": 1,
			"rate": flt(row.amount),
			"price_list_rate": flt(row.amount),
			"amount": flt(row.amount),
		}
		_set_item_defaults(item, contract, row)
		invoice.append("items", item)

	invoice.insert(ignore_permissions=False)

	for row in rows:
		_update_installment_row(
			row.name,
			{
				"sales_invoice": invoice.name,
				"invoice_status": "Draft Invoice",
				"invoice_amount": flt(row.amount),
				"paid_amount": 0,
				"outstanding_amount": flt(row.amount),
				"invoiced_on": nowdate(),
			},
		)

	_update_contract_invoice_flags(contract.name, invoice.name)
	recalculate_sales_contract_collection_status(contract.name)

	if submit and settings and settings.auto_submit_sales_invoice:
		invoice.submit()
		sync_installments_from_sales_invoice(invoice)

	return invoice.name


def validate_sales_invoice_dimensions(sales_invoice, method=None):
	"""Validate/fill dimensions on Sales Invoice items linked to Sales Contracts."""
	for item in sales_invoice.items:
		contract_name = getattr(item, "sales_contract", None)
		if not contract_name:
			continue
		contract = frappe.get_cached_doc("Sales Contract", contract_name)
		_set_if_has_field(item, "unit", contract.unit, only_if_empty=True)
		_set_if_has_field(item, "project", contract.project, only_if_empty=True)
		_set_if_has_field(item, "cost_center", _get_default_cost_center(contract.company), only_if_empty=True)
		_set_if_has_field(item, "real_estate_project", contract.real_estate_project, only_if_empty=True)
		_set_if_has_field(item, "unit_reservation", contract.unit_reservation, only_if_empty=True)

	settings = get_sales_invoice_collection_settings()
	if settings and settings.require_unit_on_invoice_item:
		for item in sales_invoice.items:
			if getattr(item, "sales_contract", None) and not getattr(item, "unit", None):
				frappe.throw(_("Unit is required on Sales Invoice Item for Sales Contract invoices."))


def sync_installments_from_sales_invoice(sales_invoice, method=None):
	"""Sync installment rows and Sales Contract totals from a linked Sales Invoice."""
	if isinstance(sales_invoice, str):
		sales_invoice = frappe.get_doc("Sales Invoice", sales_invoice)

	installments = _get_installments_for_invoice(sales_invoice.name)
	if not installments:
		return

	invoice_amount_total = sum(flt(row.amount) for row in installments)
	paid_total = 0
	outstanding_total = invoice_amount_total
	if sales_invoice.docstatus == 1:
		paid_total = max(flt(sales_invoice.grand_total) - flt(sales_invoice.outstanding_amount), 0)
		outstanding_total = flt(sales_invoice.outstanding_amount)

	for row in installments:
		ratio = (flt(row.amount) / invoice_amount_total) if invoice_amount_total else 0
		paid = min(flt(row.amount), paid_total * ratio)
		outstanding = max(flt(row.amount) - paid, 0)
		status = _get_installment_invoice_status(sales_invoice, paid, outstanding, row)
		values = {
			"invoice_status": status,
			"installment_status": _map_installment_status(status, row.installment_status),
			"invoice_amount": flt(row.amount),
			"paid_amount": paid,
			"outstanding_amount": outstanding,
			"overdue_days": _get_overdue_days(row.due_date, outstanding),
		}
		if paid and not outstanding:
			values["paid_on"] = nowdate()
		_update_installment_row(row.name, values)

	for contract in {row.parent for row in installments}:
		recalculate_sales_contract_collection_status(contract)


def release_installments_on_invoice_cancel(sales_invoice, method=None):
	"""Release installment links when a linked Sales Invoice is cancelled."""
	if isinstance(sales_invoice, str):
		sales_invoice = frappe.get_doc("Sales Invoice", sales_invoice)

	installments = _get_installments_for_invoice(sales_invoice.name)
	for row in installments:
		_update_installment_row(
			row.name,
			{
				"sales_invoice": None,
				"invoice_status": "Not Invoiced",
				"installment_status": "Pending",
				"invoice_amount": 0,
				"paid_amount": 0,
				"outstanding_amount": flt(row.amount),
				"payment_entry": None,
				"invoiced_on": None,
				"paid_on": None,
			},
		)
	for contract in {row.parent for row in installments}:
		recalculate_sales_contract_collection_status(contract)


def recalculate_sales_contract_collection_status(sales_contract):
	"""Recalculate invoice and collection totals on a Sales Contract."""
	contract = frappe.get_doc("Sales Contract", sales_contract)
	rows = contract.installments or []
	total_invoiced = sum(flt(row.invoice_amount) for row in rows if row.invoice_status != "Cancelled")
	total_collected = sum(flt(row.paid_amount) for row in rows if row.invoice_status != "Cancelled")
	total_outstanding = sum(flt(row.outstanding_amount) for row in rows if row.invoice_status != "Cancelled")
	contract_total = flt(contract.net_price)

	if total_invoiced <= 0:
		status = "Not Invoiced"
	elif total_collected > 0 and total_outstanding > 0:
		status = "Partially Collected"
	elif total_collected > 0 and total_outstanding <= 0:
		status = "Fully Collected" if total_invoiced + 0.01 >= contract_total else "Partially Collected"
	elif total_invoiced + 0.01 < contract_total:
		status = "Partially Invoiced"
	else:
		status = "Fully Invoiced"

	if any(row.invoice_status == "Overdue" for row in rows):
		status = "Overdue"

	latest_payment = frappe.db.get_value(
		"Sales Installment Schedule",
		{"parent": contract.name, "parenttype": "Sales Contract", "payment_entry": ["is", "set"]},
		"payment_entry",
		order_by="modified desc",
	)

	values = {
		"total_invoiced_amount": total_invoiced,
		"total_collected_amount": total_collected,
		"total_outstanding_amount": total_outstanding,
		"collection_status": status,
		"latest_payment_entry": latest_payment,
	}
	if total_invoiced:
		values["invoices_created"] = 1
	frappe.db.set_value("Sales Contract", contract.name, values, update_modified=True)


def _validate_contract_for_invoice(contract, settings):
	if contract.contract_status not in ACTIVE_CONTRACT_STATUSES:
		frappe.throw(_("Sales Contract must be Approved or Active before creating Sales Invoice."))
	if settings and settings.require_customer_on_contract and not contract.customer:
		frappe.throw(_("Customer is required on Sales Contract before creating Sales Invoice."))
	if not contract.unit:
		frappe.throw(_("Unit is required on Sales Contract before creating Sales Invoice."))
	if settings and settings.require_unit_dimension and not frappe.get_meta("Sales Invoice Item").has_field("unit"):
		frappe.throw(_("Unit dimension field is missing on Sales Invoice Item."))


def _get_invoiceable_installments(contract, installment_rows=None, settings=None):
	selected = set(installment_rows or [])
	rows = []
	for row in contract.installments:
		if selected and row.name not in selected and cstr(row.installment_number) not in selected:
			continue
		if row.installment_status in ("Paid", "Waived", "Cancelled"):
			continue
		if row.invoice_status in ("Paid", "Invoiced", "Partially Paid") and row.sales_invoice:
			continue
		if row.sales_invoice and settings and settings.block_duplicate_invoice_for_installment:
			if frappe.db.exists("Sales Invoice", row.sales_invoice):
				docstatus = frappe.db.get_value("Sales Invoice", row.sales_invoice, "docstatus")
				if docstatus != 2:
					frappe.throw(
						_("Installment {0} is already linked to active Sales Invoice {1}.").format(
							row.installment_number or row.name,
							row.sales_invoice,
						)
					)
		rows.append(row)
	return rows


def _set_item_defaults(item, contract, row):
	item["project"] = contract.project
	item["cost_center"] = _get_default_cost_center(contract.company)
	item["income_account"] = _get_default_income_account(contract.company)
	for fieldname, value in {
		"unit": contract.unit,
		"sales_contract": contract.name,
		"sales_installment_reference": row.name,
		"real_estate_project": contract.real_estate_project,
		"unit_reservation": contract.unit_reservation,
	}.items():
		if frappe.get_meta("Sales Invoice Item").has_field(fieldname):
			item[fieldname] = value


def _get_default_income_account(company):
	return frappe.db.get_value("Company", company, "default_income_account") if company else None


def _get_default_cost_center(company):
	return frappe.db.get_value("Company", company, "cost_center") if company else None


def _set_if_has_field(doc, fieldname, value, only_if_empty=False):
	if value is None:
		return
	if doc.meta.has_field(fieldname):
		if only_if_empty and doc.get(fieldname):
			return
		doc.set(fieldname, value)


def _update_installment_row(row_name, values):
	for fieldname, value in values.items():
		if frappe.get_meta("Sales Installment Schedule").has_field(fieldname):
			frappe.db.set_value(
				"Sales Installment Schedule",
				row_name,
				fieldname,
				value,
				update_modified=False,
			)


def _update_contract_invoice_flags(contract_name, invoice_name):
	values = {"invoices_created": 1}
	if frappe.get_meta("Sales Contract").has_field("first_invoice_reference"):
		first_invoice = frappe.db.get_value("Sales Contract", contract_name, "first_invoice_reference")
		if not first_invoice:
			values["first_invoice_reference"] = invoice_name
	frappe.db.set_value("Sales Contract", contract_name, values, update_modified=True)


def _get_installments_for_invoice(invoice_name):
	return frappe.get_all(
		"Sales Installment Schedule",
		filters={"parenttype": "Sales Contract", "sales_invoice": invoice_name},
		fields=[
			"name",
			"parent",
			"amount",
			"due_date",
			"installment_status",
			"invoice_status",
			"sales_invoice",
		],
	)


def _validate_invoice_for_contract_submission(invoice, installments):
	if not invoice.customer:
		frappe.throw(_("Customer is required before submitting Sales Invoice {0}.").format(invoice.name))
	if not invoice.company:
		frappe.throw(_("Company is required before submitting Sales Invoice {0}.").format(invoice.name))

	for item in invoice.items:
		if getattr(item, "sales_contract", None) and not getattr(item, "unit", None):
			frappe.throw(_("Unit is required on every Sales Invoice Item linked to a Sales Contract."))

	for row in installments:
		if row.invoice_status in ("Invoiced", "Partially Paid", "Paid") and row.sales_invoice == invoice.name:
			continue
		if row.sales_invoice != invoice.name:
			frappe.throw(_("Installment {0} is not linked to Sales Invoice {1}.").format(row.name, invoice.name))

		for duplicate in frappe.get_all(
			"Sales Invoice Item",
			filters={"sales_installment_reference": row.name, "parent": ["!=", invoice.name]},
			fields=["parent"],
		):
			if frappe.db.get_value("Sales Invoice", duplicate.parent, "docstatus") == 1:
				frappe.throw(
					_("Installment {0} is already linked to submitted Sales Invoice {1}.").format(
						row.name,
						duplicate.parent,
					)
				)


def _get_installment_invoice_status(sales_invoice, paid, outstanding, row):
	if sales_invoice.docstatus == 0:
		return "Draft Invoice"
	if sales_invoice.docstatus == 2:
		return "Cancelled"
	if outstanding <= 0:
		return "Paid"
	if paid > 0:
		return "Partially Paid"
	if _get_overdue_days(row.due_date, outstanding) > 0:
		return "Overdue"
	return "Invoiced"


def _map_installment_status(invoice_status, current):
	if invoice_status == "Paid":
		return "Paid"
	if invoice_status == "Partially Paid":
		return "Partial"
	if invoice_status == "Overdue":
		return "Overdue"
	if invoice_status == "Cancelled":
		return "Cancelled"
	return current or "Pending"


def _get_overdue_days(due_date, outstanding):
	if not due_date or flt(outstanding) <= 0:
		return 0
	settings = get_sales_invoice_collection_settings()
	grace = settings.overdue_grace_days if settings else 0
	days = (getdate(nowdate()) - add_days(getdate(due_date), grace or 0)).days
	return max(days, 0)


def _parse_installment_rows(rows):
	if not rows:
		return None
	if isinstance(rows, str):
		try:
			parsed = json.loads(rows)
			if isinstance(parsed, list):
				return [cstr(row) for row in parsed]
		except Exception:
			return [cstr(part).strip() for part in rows.split(",") if cstr(part).strip()]
	if isinstance(rows, (list, tuple, set)):
		return [cstr(row) for row in rows]
	return [cstr(rows)]
