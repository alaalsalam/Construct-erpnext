import frappe
from frappe import _
from construct_erpnext.reporting.report_utils import count_where, sum_field, summary_value, normalize_common_filters, report_dashboard_message


def execute(filters=None):
	filters = normalize_common_filters(filters)
	data = get_data(filters)
	return get_columns(), data, report_dashboard_message(get_report_summary(data)), None, None, False


def get_columns():
	return [
		{"label": _("Work Item"), "fieldname": "name", "fieldtype": "Link", "options": "Construction Work Item", "width": 170},
		{"label": _("Planned Amount"), "fieldname": "planned_amount", "fieldtype": "Currency", "width": 130},
		{"label": _("Committed Amount"), "fieldname": "committed_amount", "fieldtype": "Currency", "width": 140},
		{"label": _("Invoiced Amount"), "fieldname": "invoiced_amount", "fieldtype": "Currency", "width": 130},
		{"label": _("Consumed Amount"), "fieldname": "consumed_amount", "fieldtype": "Currency", "width": 140},
		{"label": _("Variance Amount"), "fieldname": "procurement_variance_amount", "fieldtype": "Currency", "width": 140},
		{"label": _("Variance %"), "fieldname": "variance_percent", "fieldtype": "Percent", "width": 110},
		{"label": _("Risk Status"), "fieldname": "risk_status", "fieldtype": "Data", "width": 120},
	]


def get_data(filters):
	conditions = ["disabled = 0"]
	values = {}
	if filters.get("project"):
		conditions.append("project = %(project)s")
		values["project"] = filters.get("project")
	if filters.get("construction_boq"):
		conditions.append("construction_boq = %(construction_boq)s")
		values["construction_boq"] = filters.get("construction_boq")
	if filters.get("overrun_only"):
		conditions.append("committed_amount > planned_amount")

	return frappe.db.sql(
		"""
		SELECT
			name,
			planned_amount,
			committed_amount,
			invoiced_amount,
			consumed_amount,
			procurement_variance_amount,
			CASE
				WHEN planned_amount > 0
				THEN procurement_variance_amount / planned_amount * 100
				ELSE 0
			END AS variance_percent,
			CASE
				WHEN committed_amount > planned_amount THEN 'Overrun'
				WHEN committed_amount = planned_amount THEN 'Fully Committed'
				WHEN committed_amount > 0 THEN 'Committed'
				ELSE 'Open'
			END AS risk_status
		FROM `tabConstruction Work Item`
		WHERE {conditions}
		ORDER BY risk_status DESC, name
		""".format(conditions=" AND ".join(conditions)),
		values,
		as_dict=True,
	)


def get_report_summary(data):
	return [
		summary_value("Planned Amount", sum_field(data, "planned_amount"), "Currency", "Blue"),
		summary_value("Committed Amount", sum_field(data, "committed_amount"), "Currency", "Orange"),
		summary_value("Invoiced Amount", sum_field(data, "invoiced_amount"), "Currency", "Green"),
		summary_value("Variance Amount", sum_field(data, "procurement_variance_amount"), "Currency", "Red"),
		summary_value("Overrun Items", count_where(data, "risk_status", "Overrun"), "Int", "Red"),
	]
