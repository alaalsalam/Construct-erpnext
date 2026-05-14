import frappe
from frappe import _
from frappe.utils import add_days, nowdate


@frappe.whitelist()
def create_phase_h_validation_data():
	units = frappe.get_all("Unit", filters={"real_estate_project": "REP-2026-00002"}, pluck="name", limit_page_length=3)
	if not units:
		frappe.throw(_("No Units found for REP-2026-00002."))
	docs = []
	specs = [
		("Title Deed", "صك ملكية الوحدة", units[0], 365),
		("Drawing", "مخطط الوحدة المعتمد", units[1], 0),
		("License", "رخصة تشغيل مبدئية", units[2], 45),
	]
	for document_type, title, unit, days in specs:
		docs.append(_get_or_create_property_document(document_type, title, unit, days))
	register = _get_or_create_contract_attachment()
	return {"property_documents": docs, "contract_attachment": register}


def _get_or_create_property_document(document_type, title, unit, expiry_days):
	existing = frappe.db.get_value("Property Document", {"document_title": title, "unit": unit}, "name")
	if existing:
		return existing
	doc = frappe.new_doc("Property Document")
	doc.document_type = document_type
	doc.document_title = title
	doc.status = "Active"
	doc.document_date = nowdate()
	doc.expiry_date = add_days(nowdate(), expiry_days) if expiry_days else None
	doc.real_estate_project = "REP-2026-00002"
	doc.unit = unit
	doc.remarks = "سجل وثيقة تشغيلي ضمن بيانات العرض."
	doc.insert(ignore_permissions=False)
	return doc.name


def _get_or_create_contract_attachment():
	if not frappe.db.exists("Sales Contract", "SC-PROJ-0002-001"):
		return None
	existing = frappe.db.get_value(
		"Contract Attachment Register",
		{"reference_doctype": "Sales Contract", "reference_name": "SC-PROJ-0002-001", "document_title": "مرفقات عقد البيع الرئيسية"},
		"name",
	)
	if existing:
		return existing
	doc = frappe.new_doc("Contract Attachment Register")
	doc.reference_doctype = "Sales Contract"
	doc.reference_name = "SC-PROJ-0002-001"
	doc.document_title = "مرفقات عقد البيع الرئيسية"
	doc.status = "Active"
	doc.remarks = "سجل مرفقات تشغيلي بدون ملف خارجي إلزامي."
	doc.insert(ignore_permissions=False)
	return doc.name
