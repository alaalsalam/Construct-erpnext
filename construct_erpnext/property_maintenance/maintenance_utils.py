import frappe
from frappe import _
from frappe.utils import add_days, nowdate


@frappe.whitelist()
def create_phase_g_validation_data():
	units = frappe.get_all(
		"Unit",
		filters={"real_estate_project": "REP-2026-00002"},
		fields=["name", "real_estate_project", "building", "floor"],
		limit_page_length=4,
	)
	if not units:
		frappe.throw(_("No Units found for REP-2026-00002."))
	requests = []
	specs = [
		("Electrical", "High", "Under Review", 2500, 0, "فحص لوحة الكهرباء داخل الوحدة"),
		("Plumbing", "Medium", "In Progress", 1800, 600, "معالجة تسريب بسيط في دورة المياه"),
		("AC", "High", "New", 3200, 0, "فحص وحدة التكييف قبل التسليم"),
		("Civil", "Low", "Completed", 1500, 1450, "معالجة ملاحظة تشطيب بسيطة"),
	]
	for idx, unit in enumerate(units):
		requests.append(_get_or_create_request(unit, specs[idx % len(specs)], idx))
	return {"maintenance_requests": requests}


def _get_or_create_request(unit, spec, idx):
	issue_type, priority, status, estimated, actual, description = spec
	existing = frappe.db.get_value(
		"Property Maintenance Request",
		{"unit": unit.name, "issue_type": issue_type, "description": description},
		"name",
	)
	if existing:
		return existing
	doc = frappe.new_doc("Property Maintenance Request")
	doc.unit = unit.name
	doc.real_estate_project = unit.real_estate_project
	doc.building = unit.building
	doc.floor = unit.floor
	doc.request_date = nowdate()
	doc.status = status
	doc.requester_type = "Internal"
	doc.requester_name = "فريق إدارة العقار"
	doc.issue_type = issue_type
	doc.priority = priority
	doc.description = description
	doc.estimated_cost = estimated
	doc.actual_cost = actual
	doc.assigned_to = frappe.session.user
	doc.remarks = "طلب صيانة تشغيلي ضمن سيناريو العرض."
	doc.insert(ignore_permissions=False)
	_create_task(doc, idx)
	return doc.name


def _create_task(request, idx):
	if frappe.db.exists("Property Maintenance Task", {"maintenance_request": request.name}):
		return
	task = frappe.new_doc("Property Maintenance Task")
	task.maintenance_request = request.name
	task.task_title = f"تنفيذ {request.issue_type} للوحدة {request.unit}"
	task.status = "Completed" if request.status == "Completed" else "Open"
	task.priority = request.priority
	task.assigned_to = request.assigned_to
	task.planned_start = nowdate()
	task.planned_end = add_days(nowdate(), idx + 2)
	task.completed_on = nowdate() if task.status == "Completed" else None
	task.estimated_cost = request.estimated_cost
	task.actual_cost = request.actual_cost
	task.remarks = "مهمة تشغيلية مرتبطة بطلب الصيانة."
	task.insert(ignore_permissions=False)
