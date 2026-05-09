from frappe.utils import get_first_day, get_last_day


def current_month_bounds(date=None):
	return get_first_day(date), get_last_day(date)
