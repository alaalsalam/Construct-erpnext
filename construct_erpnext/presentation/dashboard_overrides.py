import frappe
from frappe import _


def extend_project_dashboard(data=None):
	data = _ensure_dashboard(data)
	data.fieldname = data.get("fieldname") or "project"
	_add_group(
		data,
		_("Construction Control"),
		[
			"Construction BOQ",
			"Construction Work Item",
			"Measurement Book",
			"Measurement Entry",
			"Interim Payment Certificate",
		],
	)
	_add_group(
		data,
		_("Contractor Control"),
		["Contractor Account", "Retention Register", "Advance Register", "Guarantee Register"],
	)
	_add_group(
		data,
		_("Executive Analytics"),
		["Project Financial Snapshot", "Project Cash Flow Forecast", "Project EVM Metrics"],
	)
	_add_group(
		data,
		_("Real Estate"),
		["Real Estate Project", "Unit", "Unit Cost Allocation", "Unit Reservation", "Sales Contract"],
	)
	data.non_standard_fieldnames.update({
		"Real Estate Project": "project",
		"Unit": "project",
		"Unit Cost Allocation": "project",
		"Unit Reservation": "project",
		"Sales Contract": "project",
	})
	data.internal_links.update({"Sales Invoice": ["items", "project"]})
	return data


def extend_procurement_dashboard(data=None):
	data = _ensure_dashboard(data)
	_add_group(
		data,
		_("Construction Traceability"),
		["Construction Work Item", "Construction BOQ", "WBS Element", "Cost Code"],
	)
	data.internal_links.update({
		"Construction Work Item": ["items", "construction_work_item"],
		"Construction BOQ": ["items", "construction_boq"],
		"WBS Element": ["items", "wbs_element"],
		"Cost Code": ["items", "cost_code"],
	})
	return data


def extend_sales_invoice_dashboard(data=None):
	data = _ensure_dashboard(data)
	_add_group(
		data,
		_("Real Estate Sales"),
		["Sales Contract", "Unit Reservation", "Unit", "Real Estate Project"],
	)
	data.internal_links.update({
		"Sales Contract": ["items", "sales_contract"],
		"Unit Reservation": ["items", "unit_reservation"],
		"Unit": ["items", "unit"],
		"Real Estate Project": ["items", "real_estate_project"],
	})
	return data


def extend_customer_dashboard(data=None):
	data = _ensure_dashboard(data)
	data.fieldname = data.get("fieldname") or "customer"
	_add_group(data, _("Real Estate Sales"), ["Unit Reservation", "Sales Contract", "Sales Invoice"])
	data.non_standard_fieldnames.update({
		"Unit Reservation": "customer",
		"Sales Contract": "customer",
	})
	return data


def extend_supplier_dashboard(data=None):
	data = _ensure_dashboard(data)
	data.fieldname = data.get("fieldname") or "supplier"
	_add_group(
		data,
		_("Contractor Control"),
		["Contractor Account", "Interim Payment Certificate", "Retention Register", "Advance Register", "Guarantee Register"],
	)
	data.non_standard_fieldnames.update({
		"Contractor Account": "contractor",
		"Interim Payment Certificate": "contractor",
		"Retention Register": "contractor",
		"Advance Register": "contractor",
		"Guarantee Register": "contractor",
	})
	return data


def _ensure_dashboard(data):
	data = frappe._dict(data or {})
	data.setdefault("transactions", [])
	data.setdefault("non_standard_fieldnames", {})
	data.setdefault("internal_links", {})
	return data


def _add_group(data, label, items):
	for group in data.transactions:
		if group.get("label") == label:
			for item in items:
				if item not in group.get("items", []):
					group.setdefault("items", []).append(item)
			return
	data.transactions.append({"label": label, "items": items})
