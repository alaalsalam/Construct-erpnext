import frappe
from frappe import _


@frappe.whitelist()
def create_phase_i_validation_data():
	profiles = []
	if frappe.db.exists("Sales Contract", "SC-PROJ-0002-001"):
		contract = frappe.get_doc("Sales Contract", "SC-PROJ-0002-001")
		profiles.append(_get_or_create_profile("Buyer", "Customer", contract.customer, unit=contract.unit, sales_contract=contract.name))
	if frappe.db.exists("Lease Contract", "LC-2026-00001"):
		lease = frappe.get_doc("Lease Contract", "LC-2026-00001")
		profiles.append(_get_or_create_profile("Tenant", "Customer", lease.customer, unit=lease.unit, lease_contract=lease.name))
	subcontract = frappe.db.get_value("Subcontract", {"project": "PROJ-0002"}, ["name", "contractor"], as_dict=True)
	if subcontract:
		profiles.append(_get_or_create_profile("Contractor", "Supplier", subcontract.contractor, contractor_agreement=subcontract.name))
	owner = frappe.db.get_value("Property Owner", {}, "name")
	unit = frappe.db.get_value("Unit", {"real_estate_project": "REP-2026-00002"}, "name") or frappe.db.get_value("Unit", {}, "name")
	if owner:
		profiles.append(_get_or_create_profile("Owner", "Property Owner", owner, unit=unit))
	return {"portal_access_profiles": [row for row in profiles if row]}


def _get_or_create_profile(access_type, party_type, party, **kwargs):
	if not party:
		return None
	existing = frappe.db.get_value("Portal Access Profile", {"access_type": access_type, "party_type": party_type, "party": party}, "name")
	doc = frappe.get_doc("Portal Access Profile", existing) if existing else frappe.new_doc("Portal Access Profile")
	doc.access_type = access_type
	doc.party_type = party_type
	doc.party = party
	doc.status = "Ready for Review"
	doc.unit = kwargs.get("unit")
	doc.sales_contract = kwargs.get("sales_contract")
	doc.lease_contract = kwargs.get("lease_contract")
	doc.contractor_agreement = kwargs.get("contractor_agreement")
	doc.access_notes = _("Portal readiness profile only. No public login has been created.")
	doc.save(ignore_permissions=False)
	return doc.name
