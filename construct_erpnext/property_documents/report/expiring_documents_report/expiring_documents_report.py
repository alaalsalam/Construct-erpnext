import frappe
from frappe.utils import add_days, nowdate
from construct_erpnext.property_documents.report.property_document_register.property_document_register import _columns


def execute(filters=None):
	filters = filters or {}
	to_date = add_days(nowdate(), int(filters.get("within_days") or 90))
	data = frappe.get_all(
		"Property Document",
		filters={"expiry_date": ["between", [nowdate(), to_date]]},
		fields=["name as property_document", "document_type", "document_title", "real_estate_project", "unit", "document_date", "expiry_date", "status"],
		order_by="expiry_date asc",
	)
	return _columns(), data
