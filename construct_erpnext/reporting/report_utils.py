from frappe import _
from frappe.utils import flt


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
