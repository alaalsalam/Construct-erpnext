# SPDX-License-Identifier: MIT
# Operational brokerage commission utilities

import frappe
from frappe import _
from frappe.utils import flt, nowdate


@frappe.whitelist()
def create_commission_entry_for_sales_contract(sales_contract, broker, commission_rule=None):
	contract = frappe.get_doc("Sales Contract", sales_contract)
	rule = _get_rule(commission_rule, "Sale", "Sales Contract", contract.company)
	base_amount = _get_sales_contract_base_amount(contract, rule.commission_basis)
	return _create_commission_entry(
		broker=broker,
		rule=rule,
		transaction_type="Sale",
		company=contract.company,
		customer=contract.customer,
		unit=contract.unit,
		sales_contract=contract.name,
		commission_base_amount=base_amount,
	)


@frappe.whitelist()
def create_commission_entry_for_lease_contract(lease_contract, broker, commission_rule=None):
	lease = frappe.get_doc("Lease Contract", lease_contract)
	rule = _get_rule(commission_rule, "Rent", "Lease Contract", lease.company)
	base_amount = _get_lease_contract_base_amount(lease, rule.commission_basis)
	return _create_commission_entry(
		broker=broker,
		rule=rule,
		transaction_type="Rent",
		company=lease.company,
		customer=lease.customer,
		unit=lease.unit,
		lease_contract=lease.name,
		commission_base_amount=base_amount,
	)


@frappe.whitelist()
def create_commission_entry_for_sales_invoice(sales_invoice, broker, commission_rule=None):
	invoice = frappe.get_doc("Sales Invoice", sales_invoice)
	transaction_type = "Rent" if invoice.get("lease_contract") else "Sale"
	rule = _get_rule(commission_rule, transaction_type, "Sales Invoice", invoice.company)
	base_amount = _get_invoice_base_amount(invoice, rule.commission_basis)
	return _create_commission_entry(
		broker=broker,
		rule=rule,
		transaction_type=transaction_type,
		company=invoice.company,
		customer=invoice.customer,
		unit=invoice.get("unit"),
		sales_contract=invoice.get("sales_contract"),
		lease_contract=invoice.get("lease_contract"),
		sales_invoice=invoice.name,
		commission_base_amount=base_amount,
	)


def calculate_commission_amount(base_amount, commission_percent=0, fixed_amount=0):
	return (flt(base_amount) * flt(commission_percent) / 100) + flt(fixed_amount)


@frappe.whitelist()
def create_phase_c_validation_data():
	"""Create one operational commission scenario for the PROJ-0002 presentation."""
	sales_contract = "SC-PROJ-0002-001"
	broker_name = "وسيط عقاري رئيسي"
	rule_name = "عمولة مبيعات عقارية 2.5%"

	if not frappe.db.exists("Sales Contract", sales_contract):
		frappe.throw(_("Sales Contract {0} does not exist.").format(sales_contract))

	contract = frappe.get_doc("Sales Contract", sales_contract)

	if not frappe.db.exists("Broker", broker_name):
		broker = frappe.new_doc("Broker")
		broker.broker_name = broker_name
		broker.broker_type = "Individual"
		broker.status = "Active"
		broker.mobile_no = "+966500000000"
		broker.remarks = _("Primary broker for operational sales commission validation.")
		broker.insert(ignore_permissions=False)

	if not frappe.db.exists("Commission Rule", rule_name):
		rule = frappe.new_doc("Commission Rule")
		rule.rule_name = rule_name
		rule.company = contract.company
		rule.status = "Active"
		rule.transaction_type = "Sale"
		rule.applies_to = "Sales Contract"
		rule.commission_basis = "Contract Amount"
		rule.commission_percent = 2.5
		rule.fixed_amount = 0
		rule.remarks = _("Operational sales commission rule for the main presentation project.")
		rule.insert(ignore_permissions=False)

	existing_entry = frappe.db.get_value(
		"Commission Entry",
		{
			"broker": broker_name,
			"commission_rule": rule_name,
			"sales_contract": sales_contract,
			"status": ["!=", "Cancelled"],
		},
		"name",
	)
	if existing_entry:
		entry_name = existing_entry
	else:
		entry_name = create_commission_entry_for_sales_contract(
			sales_contract=sales_contract,
			broker=broker_name,
			commission_rule=rule_name,
		)

	entry = frappe.get_doc("Commission Entry", entry_name)
	return {
		"broker": broker_name,
		"commission_rule": rule_name,
		"commission_entry": entry.name,
		"sales_contract": sales_contract,
		"commission_base_amount": flt(entry.commission_base_amount),
		"commission_percent": flt(entry.commission_percent),
		"commission_amount": flt(entry.commission_amount),
		"status": entry.status,
	}


def _create_commission_entry(**kwargs):
	rule = kwargs.pop("rule")
	broker = kwargs.pop("broker")
	if not frappe.db.exists("Broker", broker):
		frappe.throw(_("Broker {0} does not exist.").format(broker))

	if _duplicate_exists(broker, rule.name, kwargs):
		frappe.throw(_("Commission Entry already exists for this broker/rule/transaction."))

	entry = frappe.new_doc("Commission Entry")
	entry.broker = broker
	entry.commission_rule = rule.name
	entry.transaction_type = kwargs.get("transaction_type")
	entry.company = kwargs.get("company")
	entry.customer = kwargs.get("customer")
	entry.unit = kwargs.get("unit")
	entry.sales_contract = kwargs.get("sales_contract")
	entry.lease_contract = kwargs.get("lease_contract")
	entry.sales_invoice = kwargs.get("sales_invoice")
	entry.payment_entry = kwargs.get("payment_entry")
	entry.commission_basis = rule.commission_basis
	entry.commission_base_amount = flt(kwargs.get("commission_base_amount"))
	entry.commission_percent = flt(rule.commission_percent)
	entry.fixed_amount = flt(rule.fixed_amount)
	entry.commission_amount = calculate_commission_amount(
		entry.commission_base_amount,
		entry.commission_percent,
		entry.fixed_amount,
	)
	entry.status = "Accrued"
	entry.posting_date = nowdate()
	entry.remarks = _("Commission calculated from {0}.").format(rule.name)
	entry.insert(ignore_permissions=False)
	return entry.name


def _get_rule(rule_name, transaction_type, applies_to, company=None):
	if rule_name:
		rule = frappe.get_doc("Commission Rule", rule_name)
	else:
		filters = {
			"transaction_type": transaction_type,
			"applies_to": applies_to,
			"status": "Active",
		}
		if company and frappe.get_meta("Commission Rule").has_field("company"):
			filters["company"] = ["in", (company, "")]
		rule_name = frappe.db.get_value("Commission Rule", filters, "name", order_by="modified desc")
		if not rule_name and company:
			filters.pop("company", None)
			rule_name = frappe.db.get_value("Commission Rule", filters, "name", order_by="modified desc")
		if not rule_name:
			frappe.throw(_("No active Commission Rule found for {0} / {1}.").format(transaction_type, applies_to))
		rule = frappe.get_doc("Commission Rule", rule_name)

	if rule.status != "Active":
		frappe.throw(_("Commission Rule {0} is not Active.").format(rule.name))
	if rule.transaction_type != transaction_type or rule.applies_to != applies_to:
		frappe.throw(_("Commission Rule {0} does not match the requested transaction.").format(rule.name))
	return rule


def _get_sales_contract_base_amount(contract, basis):
	if basis == "Collected Amount":
		return flt(contract.total_collected_amount)
	if basis == "Invoice Amount":
		return flt(contract.total_invoiced_amount)
	return flt(contract.net_price or contract.sale_price)


def _get_lease_contract_base_amount(lease, basis):
	if basis == "Collected Amount":
		return flt(lease.total_collected_rent)
	if basis == "Invoice Amount":
		return flt(lease.total_invoiced_rent)
	return flt(lease.total_scheduled_rent or lease.total_contract_rent)


def _get_invoice_base_amount(invoice, basis):
	if basis == "Collected Amount":
		return max(flt(invoice.grand_total) - flt(invoice.outstanding_amount), 0)
	return flt(invoice.grand_total)


def _duplicate_exists(broker, rule, values):
	filters = {
		"broker": broker,
		"commission_rule": rule,
		"status": ["!=", "Cancelled"],
	}
	for fieldname in ("sales_contract", "lease_contract", "sales_invoice", "payment_entry"):
		if values.get(fieldname):
			filters[fieldname] = values.get(fieldname)
	return frappe.db.exists("Commission Entry", filters)
