from construct_erpnext.property_maintenance.report.maintenance_request_register.maintenance_request_register import _columns
import frappe


def execute(filters=None):
	data = frappe.get_all("Property Maintenance Request", filters={"status": ["not in", ["Completed", "Cancelled"]]}, fields=["name as request", "unit", "real_estate_project", "request_date", "issue_type", "priority", "status", "estimated_cost", "actual_cost"], order_by="priority desc, modified desc")
	return _columns(), data
