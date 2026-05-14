import frappe


def after_migrate():
	doc = frappe.get_single("Portal Display Settings")
	if not doc.get("status"):
		doc.status = "Planning"
		doc.portal_message = "Portal readiness only. Public portal routes are not enabled yet."
		doc.save(ignore_permissions=True)
