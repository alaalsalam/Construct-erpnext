import frappe


def after_migrate():
	doc = frappe.get_single("Matching Settings")
	changed = False
	for fieldname, value in {
		"minimum_score": 60,
		"location_weight": 10,
		"price_weight": 35,
		"area_weight": 25,
		"type_weight": 20,
		"feature_weight": 10,
	}.items():
		if not doc.get(fieldname):
			doc.set(fieldname, value)
			changed = True
	if changed:
		doc.save(ignore_permissions=True)
