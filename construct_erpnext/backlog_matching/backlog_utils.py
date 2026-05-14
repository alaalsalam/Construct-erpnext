import frappe
from frappe import _
from frappe.utils import flt, now_datetime, nowdate

from construct_erpnext.smart_matching.matching_utils import run_matching_for_requirement


@frappe.whitelist()
def create_or_update_backlog_from_requirement(requirement):
	req = frappe.get_doc("Customer Requirement", requirement)
	existing = frappe.db.get_value("Backlog Request", {"customer_requirement": req.name}, "name")
	doc = frappe.get_doc("Backlog Request", existing) if existing else frappe.new_doc("Backlog Request")
	doc.customer_requirement = req.name
	doc.lead = req.lead
	doc.customer = req.customer
	doc.status = "Active"
	doc.reason = _infer_reason(req)
	doc.priority_score = _priority_score(req)
	doc.waiting_since = doc.waiting_since or nowdate()
	doc.requirement_summary = _summary(req)
	doc.remarks = _("Created from Customer Requirement with no suitable match.")
	doc.save(ignore_permissions=False)
	return doc.name


@frappe.whitelist()
def retry_backlog_matching(backlog_request=None):
	filters = {"status": "Active"}
	if backlog_request:
		filters["name"] = backlog_request
	backlogs = frappe.get_all("Backlog Request", filters=filters, pluck="name")
	attempts = []
	for backlog_name in backlogs:
		backlog = frappe.get_doc("Backlog Request", backlog_name)
		requirement = frappe.get_doc("Customer Requirement", backlog.customer_requirement)
		match_result = frappe.get_doc("Match Result", run_matching_for_requirement(backlog.customer_requirement))
		best_item = max(match_result.items, key=lambda row: flt(row.score), default=None)
		attempt = frappe.new_doc("Backlog Match Attempt")
		attempt.backlog_request = backlog.name
		attempt.attempt_date = now_datetime()
		attempt.units_checked = _count_available_units(requirement)
		attempt.best_score = flt(match_result.best_score)
		if best_item:
			attempt.result = "Matched"
			attempt.matched_unit = best_item.unit
			backlog.status = "Matched"
			backlog.matched_unit = best_item.unit
		else:
			attempt.result = "No Match"
		attempt.remarks = _("Backlog matching retry completed.")
		attempt.insert(ignore_permissions=False)
		backlog.last_match_attempt = attempt.attempt_date
		backlog.save(ignore_permissions=False)
		attempts.append(attempt.name)
	return {"attempts": attempts}


@frappe.whitelist()
def create_phase_f_validation_data():
	no_match_results = frappe.get_all(
		"Match Result",
		filters={"status": "No Suitable Match"},
		fields=["customer_requirement"],
		limit_page_length=10,
	)
	if not no_match_results:
		frappe.throw(_("No unmatched Match Results found. Run Smart Matching first."))
	backlogs = [create_or_update_backlog_from_requirement(row.customer_requirement) for row in no_match_results[:3]]
	attempts = retry_backlog_matching()
	return {"backlog_requests": backlogs, "attempts": attempts.get("attempts", [])}


def _infer_reason(req):
	if req.budget_max:
		return "Budget Gap"
	if req.preferred_area_min or req.preferred_area_max:
		return "Area Gap"
	if req.unit_type:
		return "Type Gap"
	return "No Match"


def _priority_score(req):
	return {"Urgent": 90, "High": 75, "Medium": 50, "Low": 25}.get(req.priority, 50)


def _summary(req):
	return f"{req.requirement_type} - {req.requirement_title} - Budget {flt(req.budget_min):,.0f} to {flt(req.budget_max):,.0f}"


def _count_available_units(req):
	filters = {"status": "Available"}
	if req.preferred_project:
		filters["real_estate_project"] = req.preferred_project
	return frappe.db.count("Unit", filters)
