from frappe.utils import flt


def safe_ratio(numerator, denominator):
	return flt(numerator) / flt(denominator) if flt(denominator) else 0
