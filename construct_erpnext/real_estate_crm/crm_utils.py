import frappe
from frappe import _
from frappe.utils import add_days, now_datetime, nowdate


@frappe.whitelist()
def create_phase_d_validation_data():
	"""Create a small, connected PROJ-0002 CRM scenario without accounting impact."""
	project = "REP-2026-00002"
	if not frappe.db.exists("Real Estate Project", project):
		frappe.throw(_("Real Estate Project {0} does not exist.").format(project))

	units = frappe.get_all(
		"Unit",
		filters={"real_estate_project": project},
		fields=["name", "unit_type", "area", "expected_sale_price", "expected_monthly_rent"],
		order_by="name asc",
		limit_page_length=8,
	)
	if not units:
		frappe.throw(_("No Units found for {0}.").format(project))

	requirement_specs = [
		{
			"title": "طلب شراء شقة عائلية في مشروع الإبراهيم السكني",
			"type": "Buy",
			"status": "Qualified",
			"priority": "High",
			"source": "زيارة مكتب المبيعات",
			"budget_min": 900000,
			"budget_max": 1600000,
			"area_min": 110,
			"area_max": 180,
			"features": "موقف سيارة، مخزن، إطلالة جيدة",
		},
		{
			"title": "طلب استثمار لوحدة تجارية في الدور الأرضي",
			"type": "Investment",
			"status": "Matched",
			"priority": "Medium",
			"source": "إحالة من وسيط",
			"budget_min": 1800000,
			"budget_max": 3200000,
			"area_min": 80,
			"area_max": 160,
			"features": "واجهة شارع، سهولة وصول",
		},
		{
			"title": "طلب إيجار مكتب إداري متوسط المساحة",
			"type": "Rent",
			"status": "New",
			"priority": "Medium",
			"source": "اتصال مباشر",
			"budget_min": 18000,
			"budget_max": 45000,
			"area_min": 70,
			"area_max": 140,
			"features": "مصعد، خدمات مشتركة، مواقف",
		},
		{
			"title": "طلب شراء بنتهاوس بمساحة كبيرة",
			"type": "Buy",
			"status": "Backlog",
			"priority": "Urgent",
			"source": "حملة رقمية",
			"budget_min": 2500000,
			"budget_max": 4200000,
			"area_min": 220,
			"area_max": 360,
			"features": "سطح خاص، إطلالة مفتوحة",
		},
		{
			"title": "طلب استئجار محل صغير للعلامة التجارية",
			"type": "Rent",
			"status": "Qualified",
			"priority": "High",
			"source": "معرض عقاري",
			"budget_min": 25000,
			"budget_max": 65000,
			"area_min": 45,
			"area_max": 95,
			"features": "واجهة تجارية، مواقف قريبة",
		},
	]

	requirements = []
	for idx, spec in enumerate(requirement_specs):
		requirement = _get_or_create_requirement(spec, project, units[idx % len(units)])
		requirements.append(requirement)

	for idx, requirement in enumerate(requirements[:3]):
		_get_or_create_viewing(requirement, units[idx % len(units)], idx)

	for idx, requirement in enumerate(requirements[:4]):
		_get_or_create_follow_up(requirement, idx)

	return {
		"requirements": [row.name for row in requirements],
		"viewing_appointments": frappe.get_all(
			"Viewing Appointment",
			filters={"requirement": ["in", [row.name for row in requirements]]},
			pluck="name",
		),
		"follow_ups": frappe.get_all(
			"Real Estate Follow Up",
			filters={"requirement": ["in", [row.name for row in requirements]]},
			pluck="name",
		),
	}


def _get_or_create_requirement(spec, project, unit):
	existing = frappe.db.get_value("Customer Requirement", {"requirement_title": spec["title"]}, "name")
	if existing:
		return frappe.get_doc("Customer Requirement", existing)

	doc = frappe.new_doc("Customer Requirement")
	doc.requirement_title = spec["title"]
	doc.requirement_date = nowdate()
	doc.requirement_type = spec["type"]
	doc.status = spec["status"]
	doc.priority = spec["priority"]
	doc.lead_source = spec["source"]
	doc.preferred_project = project
	doc.unit_type = unit.get("unit_type")
	doc.property_nature = "سكني" if spec["type"] == "Buy" else "تجاري"
	doc.preferred_area_min = spec["area_min"]
	doc.preferred_area_max = spec["area_max"]
	doc.budget_min = spec["budget_min"]
	doc.budget_max = spec["budget_max"]
	doc.bedrooms = 3 if spec["type"] == "Buy" else 0
	doc.bathrooms = 2 if spec["type"] == "Buy" else 1
	doc.required_features = spec["features"]
	doc.location_notes = "يفضل أن تكون الوحدة ضمن نطاق مشروع الإبراهيم السكني."
	doc.remarks = "بيانات عرض تشغيلية مرتبطة بسيناريو PROJ-0002."
	doc.insert(ignore_permissions=False)
	return doc


def _get_or_create_viewing(requirement, unit, idx):
	existing = frappe.db.get_value(
		"Viewing Appointment",
		{"requirement": requirement.name, "unit": unit.name},
		"name",
	)
	if existing:
		return existing
	doc = frappe.new_doc("Viewing Appointment")
	doc.requirement = requirement.name
	doc.unit = unit.name
	doc.appointment_date = add_days(now_datetime(), idx + 1)
	doc.status = "Completed" if idx == 0 else "Scheduled"
	doc.assigned_to = frappe.session.user
	doc.feedback = "العميل مهتم ويحتاج مقارنة خيارات إضافية." if idx == 0 else ""
	doc.remarks = "موعد معاينة ضمن بيانات العرض التشغيلية."
	doc.insert(ignore_permissions=False)
	return doc.name


def _get_or_create_follow_up(requirement, idx):
	existing = frappe.db.get_value(
		"Real Estate Follow Up",
		{"requirement": requirement.name, "follow_up_date": nowdate()},
		"name",
	)
	if existing:
		return existing
	doc = frappe.new_doc("Real Estate Follow Up")
	doc.requirement = requirement.name
	doc.follow_up_date = nowdate()
	doc.channel = ["Call", "Visit", "Message", "Email"][idx % 4]
	doc.result = ["Interested", "Scheduled Viewing", "Needs More Options", "No Response"][idx % 4]
	doc.assigned_to = frappe.session.user
	doc.next_action = "تحديث الخيارات المقترحة ومراجعة الوحدات المتاحة."
	doc.remarks = "متابعة تشغيلية ضمن سيناريو CRM للعرض."
	doc.insert(ignore_permissions=False)
	return doc.name
