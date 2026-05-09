import frappe
from frappe import _
from frappe.utils import flt, today


SNAPSHOT_FIELD_BY_SOURCE = {
	"BOQ Total": "boq_total_amount",
	"Committed Cost": "committed_amount",
	"Invoiced Cost": "procurement_invoiced_amount",
	"Consumed Cost": "consumed_amount",
	"Certified Cost": "certified_gross_amount",
}


def get_project_cost_source(
	real_estate_project, cost_source, project_financial_snapshot=None, manual_amount=None
):
	project = frappe.db.get_value("Real Estate Project", real_estate_project, "project")
	if cost_source == "Manual Amount":
		return flt(manual_amount)
	if cost_source == "Financial Snapshot":
		snapshot = project_financial_snapshot or _latest_snapshot(project)
		return flt(frappe.db.get_value("Project Financial Snapshot", snapshot, "boq_total_amount"))
	if cost_source in SNAPSHOT_FIELD_BY_SOURCE:
		snapshot = project_financial_snapshot or _latest_snapshot(project)
		if snapshot:
			return flt(
				frappe.db.get_value(
					"Project Financial Snapshot", snapshot, SNAPSHOT_FIELD_BY_SOURCE[cost_source]
				)
			)
	return 0


def get_units_for_allocation(real_estate_project):
	return frappe.get_all(
		"Unit",
		filters={"real_estate_project": real_estate_project},
		fields=[
			"name",
			"building",
			"floor",
			"unit_type",
			"status",
			"area",
			"expected_sale_price",
			"expected_monthly_rent",
		],
		order_by="building, floor, unit_code",
	)


def calculate_unit_allocation(allocation_doc):
	source_amount = flt(allocation_doc.source_amount)
	units = get_units_for_allocation(allocation_doc.real_estate_project)
	if not units:
		frappe.throw(_("No Units found for this Real Estate Project."))

	if allocation_doc.allocation_basis in ("By Area", "Equal Share"):
		allocation_doc.set("lines", [])
		for unit in units:
			allocation_doc.append("lines", _base_line(unit))
	elif not allocation_doc.lines:
		for unit in units:
			allocation_doc.append("lines", _base_line(unit))

	total_area = sum(flt(row.area) for row in allocation_doc.lines)
	unit_count = len(allocation_doc.lines)

	for row in allocation_doc.lines:
		if allocation_doc.allocation_basis == "By Area":
			if not total_area:
				frappe.throw(_("Total Unit area is required for By Area allocation."))
			row.allocation_percent = flt(row.area) / total_area * 100
			row.allocated_amount = source_amount * flt(row.allocation_percent) / 100
		elif allocation_doc.allocation_basis == "Equal Share":
			row.allocated_amount = source_amount / unit_count if unit_count else 0
			row.allocation_percent = (
				flt(row.allocated_amount) / source_amount * 100 if source_amount else 0
			)
		elif allocation_doc.allocation_basis == "Manual Percentage":
			row.allocated_amount = source_amount * flt(row.allocation_percent) / 100
		elif allocation_doc.allocation_basis == "Manual Amount":
			row.allocated_amount = flt(row.manual_amount)
			row.allocation_percent = (
				flt(row.allocated_amount) / source_amount * 100 if source_amount else 0
			)
		_calculate_line_profitability(row)


def apply_unit_allocation(allocation_doc):
	if allocation_doc.allocation_status == "Cancelled":
		frappe.throw(_("Cancelled allocations cannot be applied."))
	if flt(allocation_doc.source_amount) <= 0:
		frappe.throw(_("Source Amount must be greater than zero before applying."))
	if not allocation_doc.lines:
		frappe.throw(_("Allocation must have lines before applying."))
	for row in allocation_doc.lines:
		unit = frappe.get_doc("Unit", row.unit)
		unit.allocated_cost = flt(row.allocated_amount)
		unit.latest_cost_allocation = allocation_doc.name
		unit.allocated_cost_source = allocation_doc.cost_source
		unit.allocated_cost_date = allocation_doc.allocation_date
		unit.expected_margin = flt(row.expected_margin)
		unit.expected_margin_percent = flt(row.expected_margin_percent)
		unit.profitability_status = row.profitability_status
		unit.save(ignore_permissions=True)


def recalculate_unit_profitability(unit):
	unit.expected_margin = flt(unit.expected_sale_price) - flt(unit.allocated_cost)
	unit.expected_margin_percent = (
		flt(unit.expected_margin) / flt(unit.expected_sale_price) * 100
		if flt(unit.expected_sale_price)
		else 0
	)
	unit.profitability_status = get_profitability_status(
		unit.expected_sale_price, unit.expected_margin_percent
	)


def reverse_unit_allocation(allocation_doc):
	# Historical Unit allocated_cost values are not erased in this phase.
	allocation_doc.allocation_status = "Cancelled"


@frappe.whitelist()
def create_allocation_from_project(
	real_estate_project,
	allocation_basis,
	cost_source,
	project_financial_snapshot=None,
	manual_amount=None,
):
	project = frappe.db.get_value("Real Estate Project", real_estate_project, "project")
	company = frappe.db.get_value("Real Estate Project", real_estate_project, "company")
	source_amount = get_project_cost_source(
		real_estate_project, cost_source, project_financial_snapshot, manual_amount
	)
	doc = frappe.get_doc(
		{
			"doctype": "Unit Cost Allocation",
			"company": company,
			"real_estate_project": real_estate_project,
			"project": project,
			"allocation_date": today(),
			"allocation_basis": allocation_basis,
			"cost_source": cost_source,
			"project_financial_snapshot": project_financial_snapshot,
			"source_amount": source_amount,
			"allocation_status": "Draft",
			"remarks": "توزيع تكلفة مشروع البرج السكني على الوحدات",
		}
	)
	calculate_unit_allocation(doc)
	doc.insert(ignore_permissions=True)
	return doc.name


@frappe.whitelist()
def apply_allocation(allocation_name):
	doc = frappe.get_doc("Unit Cost Allocation", allocation_name)
	doc.allocation_status = "Applied"
	doc.save(ignore_permissions=True)
	return doc.name


def get_profitability_status(expected_sale_price, expected_margin_percent):
	if not flt(expected_sale_price):
		return "Not Priced"
	if flt(expected_margin_percent) >= 20:
		return "Profitable"
	if flt(expected_margin_percent) >= 0:
		return "Watch"
	return "Loss Risk"


def _base_line(unit):
	return {
		"unit": unit.name,
		"building": unit.building,
		"floor": unit.floor,
		"unit_type": unit.unit_type,
		"unit_status": unit.status,
		"area": unit.area,
		"expected_sale_price": unit.expected_sale_price,
		"expected_monthly_rent": unit.expected_monthly_rent,
	}


def _calculate_line_profitability(row):
	row.expected_margin = flt(row.expected_sale_price) - flt(row.allocated_amount)
	row.expected_margin_percent = (
		flt(row.expected_margin) / flt(row.expected_sale_price) * 100
		if flt(row.expected_sale_price)
		else 0
	)
	row.profitability_status = get_profitability_status(
		row.expected_sale_price, row.expected_margin_percent
	)


def _latest_snapshot(project):
	return frappe.db.get_value(
		"Project Financial Snapshot",
		{"project": project, "status": ["!=", "Archived"]},
		"name",
		order_by="snapshot_date desc, creation desc",
	)
