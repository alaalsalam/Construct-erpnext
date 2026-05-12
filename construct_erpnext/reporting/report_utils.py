import frappe
from frappe import _
from frappe.utils import escape_html, flt, fmt_money


def resolve_project_filter(value):
	if not value:
		return value

	if frappe.db.exists("Project", value):
		return value

	project = frappe.db.get_value("Project", {"project_name": value}, "name")
	return project or value


def normalize_common_filters(filters):
	filters = frappe._dict(filters or {})
	if filters.get("project"):
		filters.project = resolve_project_filter(filters.project)
	return filters


def sum_field(rows, fieldname):
	return sum(flt(row.get(fieldname)) for row in rows or [])


def count_where(rows, fieldname, values):
	if isinstance(values, str):
		values = {values}
	else:
		values = set(values or [])
	return sum(1 for row in rows or [] if row.get(fieldname) in values)


def summary_value(label, value, datatype="Currency", indicator="Blue"):
	return {
		"label": _(label),
		"value": flt(value) if datatype in ("Currency", "Float", "Percent") else value,
		"datatype": datatype,
		"indicator": indicator,
	}


def report_dashboard_message(summary_values):
	if not summary_values:
		return None

	cards = []
	for item in summary_values:
		label = escape_html(item.get("label") or "")
		value = _format_dashboard_value(item.get("value"), item.get("datatype"))
		color = _indicator_color(item.get("indicator"))
		cards.append(
			f"""
			<div style="min-width:180px;flex:1;padding:14px 16px;border:1px solid #dfe7ef;border-radius:10px;background:#f8fafc;">
				<div style="font-size:12px;color:#64748b;margin-bottom:8px;">{label}</div>
				<div style="font-size:20px;font-weight:700;color:{color};white-space:nowrap;">{value}</div>
			</div>
			"""
		)

	return (
		'<div class="construct-report-dashboard" '
		'style="display:flex;gap:12px;flex-wrap:wrap;margin:10px 0 16px 0;">'
		+ "".join(cards)
		+ "</div>"
	)


def _format_dashboard_value(value, datatype):
	if datatype == "Currency":
		return escape_html(fmt_money(flt(value), currency=frappe.defaults.get_global_default("currency")))
	if datatype == "Percent":
		return f"{flt(value):,.2f}%"
	if datatype == "Float":
		return f"{flt(value):,.2f}"
	if datatype == "Int":
		return f"{int(flt(value)):,}"
	return escape_html(value if value is not None else "")


def _indicator_color(indicator):
	return {
		"Green": "#059669",
		"Blue": "#2563eb",
		"Orange": "#ea580c",
		"Red": "#dc2626",
		"Grey": "#64748b",
		"Gray": "#64748b",
	}.get(indicator, "#334155")
