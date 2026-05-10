import frappe
from frappe.utils import add_days, flt, nowdate


def _doctype_exists(doctype):
	return frappe.db.exists("DocType", doctype)


def _has_field(doctype, fieldname):
	return _doctype_exists(doctype) and frappe.get_meta(doctype).has_field(fieldname)


def _sum(doctype, fieldname, filters=None):
	if not (_doctype_exists(doctype) and _has_field(doctype, fieldname)):
		return 0

	rows = frappe.get_all(doctype, filters=filters or {}, fields=[f"sum(`{fieldname}`) as total"])
	return flt(rows[0].total if rows else 0)


def _count(doctype, filters=None):
	if not _doctype_exists(doctype):
		return 0

	return frappe.db.count(doctype, filters or {})


def _latest_value(doctype, fieldname, filters=None):
	if not (_doctype_exists(doctype) and _has_field(doctype, fieldname)):
		return None

	row = frappe.get_all(
		doctype,
		filters=filters or {},
		fields=[fieldname],
		order_by="modified desc",
		limit=1,
	)
	return row[0].get(fieldname) if row else None


def _card(value, fieldtype="Currency", route=None, route_options=None):
	return {
		"value": flt(value) if fieldtype in {"Currency", "Float", "Percent", "Int"} else value,
		"fieldtype": fieldtype,
		"route": route,
		"route_options": route_options or {},
	}


def _report_route(report_name):
	return ["query-report", report_name]


@frappe.whitelist()
def boq_total(filters=None):
	total = _sum("Project Financial Snapshot", "boq_total_amount", {"status": ["!=", "Archived"]})
	if not total:
		total = _sum("Construction Work Item", "planned_amount", {"disabled": 0})
	return _card(total, route=_report_route("Project Financial Snapshot Report"))


@frappe.whitelist()
def committed_amount(filters=None):
	total = _sum("Project Financial Snapshot", "committed_amount", {"status": ["!=", "Archived"]})
	if not total:
		total = _sum("Construction Work Item", "committed_amount", {"disabled": 0})
	return _card(total, route=_report_route("Work Item Procurement Summary"))


@frappe.whitelist()
def certified_gross_amount(filters=None):
	total = _sum("Interim Payment Certificate", "gross_amount", {"docstatus": ["!=", 2]})
	if not total:
		total = _sum("Construction Work Item", "certified_amount", {"disabled": 0})
	return _card(total, route=_report_route("IPC Register"))


@frappe.whitelist()
def certified_amount(filters=None):
	return certified_gross_amount(filters)


@frappe.whitelist()
def net_payable(filters=None):
	total = _sum("Interim Payment Certificate", "net_payable", {"docstatus": ["!=", 2]})
	return _card(total, route=_report_route("IPC Register"))


@frappe.whitelist()
def retention_held(filters=None):
	total = _sum("Retention Register", "remaining_retention_amount", {"status": ["!=", "Cancelled"]})
	if not total:
		total = _sum("Retention Register", "retention_amount", {"status": ["!=", "Cancelled"]})
	return _card(total, route=_report_route("Retention Register Report"))


@frappe.whitelist()
def contractor_outstanding(filters=None):
	total = _sum("Contractor Account", "outstanding_balance", {"status": ["!=", "Closed"]})
	return _card(total, route=_report_route("Contractor Account Statement"))


@frappe.whitelist()
def cash_flow_risk(filters=None):
	value = _latest_value("Project Cash Flow Forecast", "cash_risk_status", {"status": ["!=", "Archived"]})
	return _card(value or "N/A", "Data", _report_route("Project Cash Flow Forecast Report"))


@frappe.whitelist()
def evm_cpi(filters=None):
	value = _latest_value("Project EVM Metrics", "cost_performance_index", {"status": ["!=", "Archived"]})
	return _card(value or 0, "Float", _report_route("Project EVM Metrics Report"))


@frappe.whitelist()
def evm_spi(filters=None):
	value = _latest_value("Project EVM Metrics", "schedule_performance_index", {"status": ["!=", "Archived"]})
	return _card(value or 0, "Float", _report_route("Project EVM Metrics Report"))


@frappe.whitelist()
def evm_overall_status(filters=None):
	value = _latest_value("Project EVM Metrics", "overall_evm_status", {"status": ["!=", "Archived"]})
	return _card(value or "N/A", "Data", _report_route("EVM Forecast Summary"))


@frappe.whitelist()
def work_items_count(filters=None):
	return _card(_count("Construction Work Item", {"disabled": 0}), "Int", _report_route("Construction BOQ Cost Analysis"))


@frappe.whitelist()
def invoiced_amount(filters=None):
	total = _sum("Project Financial Snapshot", "procurement_invoiced_amount", {"status": ["!=", "Archived"]})
	if not total:
		total = _sum("Construction Work Item", "invoiced_amount", {"disabled": 0})
	return _card(total, route=_report_route("Work Item Procurement Summary"))


@frappe.whitelist()
def consumed_amount(filters=None):
	total = _sum("Project Financial Snapshot", "consumed_amount", {"status": ["!=", "Archived"]})
	if not total:
		total = _sum("Construction Work Item", "consumed_amount", {"disabled": 0})
	return _card(total, route=_report_route("Site Warehouse Consumption"))


@frappe.whitelist()
def measured_amount(filters=None):
	total = _sum("Project Financial Snapshot", "measured_amount", {"status": ["!=", "Archived"]})
	if not total:
		total = _sum("Construction Work Item", "measurement_amount", {"disabled": 0})
	return _card(total, route=_report_route("Work Item Measurement Progress"))


@frappe.whitelist()
def ipc_count(filters=None):
	return _card(_count("Interim Payment Certificate", {"docstatus": ["!=", 2]}), "Int", _report_route("IPC Register"))


@frappe.whitelist()
def advance_balance(filters=None):
	total = _sum("Advance Register", "outstanding_advance_amount", {"status": ["!=", "Cancelled"]})
	if not total:
		total = _sum("Contractor Account", "current_advance_balance", {"status": ["!=", "Closed"]})
	return _card(total, route=_report_route("Advance Recovery Report"))


@frappe.whitelist()
def total_units(filters=None):
	return _card(_count("Unit"), "Int", _report_route("Unit Inventory Report"))


@frappe.whitelist()
def available_units(filters=None):
	return _card(_count("Unit", {"status": "Available"}), "Int", _report_route("Unit Availability Report"))


@frappe.whitelist()
def reserved_units(filters=None):
	return _card(_count("Unit", {"status": "Reserved"}), "Int", _report_route("Unit Reservation Impact"))


@frappe.whitelist()
def rented_units(filters=None):
	return _card(_count("Unit", {"status": "Rented"}), "Int", _report_route("Unit Availability Report"))


@frappe.whitelist()
def expected_gross_margin(filters=None):
	return _card(_sum("Unit", "expected_margin"), route=_report_route("Unit Profitability Report"))


@frappe.whitelist()
def expected_margin_percent(filters=None):
	margin = _sum("Unit", "expected_margin")
	sales = _sum("Unit", "expected_sale_price")
	return _card((margin / sales * 100) if sales else 0, "Percent", _report_route("Unit Profitability Report"))


@frappe.whitelist()
def active_reservations(filters=None):
	return _card(
		_count("Unit Reservation", {"status": "Reserved", "docstatus": ["!=", 2]}),
		"Int",
		_report_route("Active Unit Reservations"),
	)


@frappe.whitelist()
def expiring_reservations(filters=None):
	within_days = 2
	if _doctype_exists("Unit Reservation Settings"):
		within_days = frappe.db.get_single_value("Unit Reservation Settings", "warning_days_before_expiry") or 2

	return _card(
		_count(
			"Unit Reservation",
			{
				"status": "Reserved",
				"docstatus": ["!=", 2],
				"valid_until": ["between", [nowdate(), add_days(nowdate(), within_days)]],
			},
		),
		"Int",
		_report_route("Expiring Unit Reservations"),
	)
