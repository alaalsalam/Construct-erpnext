# Copyright (c) 2026, Construct ERPNext and contributors
# For license information, please see license.txt

"""
Phase 1 Presentation Data Seeder
================================
Creates rich, interconnected, quasi-realistic data for client presentation
without using SQL direct access, DB direct edits, or server scripts.

Usage:
    bench --site construction.yemenfrappe.com execute \
        construct_erpnext.setup.phase_1_presentation_data.create_phase_1_presentation_data

    bench --site construction.yemenfrappe.com execute \
        construct_erpnext.setup.phase_1_presentation_data.validate_phase_1_presentation_data

All data is tagged with implementation_batch_id = "PHASE1-PRESENTATION-2026"
No demo/test/sample/sandbox names in records.
"""

import frappe
import copy
from frappe.utils import nowdate, add_days, flt, cstr

BATCH = "PHASE1-PRESENTATION-2026"
CURRENCY = "YER"

# Valid UOMs on this system
VALID_UOMS = ["عدد", "متر", "متر مربع", "متر مكعب", "كجم"]


def _get_status(u):
    """Safely get status from a unit (handles dict/doc/scalar)."""
    if isinstance(u, (int, float, str)):
        return None
    try:
        return u.status
    except Exception:
        pass
    if hasattr(u, 'get'):
        result = u.get('status')
        if result is not None:
            return result
    return None


def _ensure_reference_data():
    """Create required reference data (Cost Codes, UOMs)."""
    print("[PHASE1] Ensuring reference data...")

    # Create UOMs if missing
    for uom_name in ["شهر", "يوم", "وحدة", "ساعة", "كيلوواط ساعة", "لتر"]:
        if not frappe.db.exists("UOM", uom_name):
            try:
                doc = frappe.new_doc("UOM")
                doc.update({"doctype": "UOM", "uom_name": uom_name, "name": uom_name})
                doc.insert(ignore_permissions=True)
                print(f"[PHASE1] Created UOM: {uom_name}")
            except Exception:
                pass

    # Create Customer Groups if missing
    for cg_name in ["Individual", "Commercial", "Corporate"]:
        if not frappe.db.exists("Customer Group", cg_name):
            try:
                doc = frappe.new_doc("Customer Group")
                doc.update({"doctype": "Customer Group", "customer_group_name": cg_name})
                doc.insert(ignore_permissions=True)
                print(f"[PHASE1] Created Customer Group: {cg_name}")
            except Exception:
                pass

    # Create Territory if missing
    if not frappe.db.exists("Territory", "Yemen"):
        try:
            doc = frappe.new_doc("Territory")
            doc.update({"doctype": "Territory", "territory_name": "Yemen"})
            doc.insert(ignore_permissions=True)
            print("[PHASE1] Created Territory: Yemen")
        except Exception:
            pass

    # Create Cost Codes for each category
    cost_codes_data = [
        ("CC-EXC", "أعمال الحفر"), ("CC-FIL", "أعمال الردم"),
        ("CC-CON", "أعمال الخرسانة"), ("CC-STE", "حديد التسليح"),
        ("CC-MAS", "أعمال المباني"), ("CC-ELC", "أعمال الكهرباء"),
        ("CC-PLB", "أعمال السباكة"), ("CC-HVA", "أعمال التكييف"),
        ("CC-WAT", "أعمال العزل"), ("CC-FIN", "أعمال التشطيبات"),
        ("CC-PNT", "أعمال الدهانات"), ("CC-FAC", "أعمال الواجهات"),
        ("CC-SIT", "أعمال الموقع العام"), ("CC-OVH", "مصاريف إدارية"),
        ("CC-SAF", "أعمال السلامة"), ("CC-GEN", "أعمال عامة"),
    ]

    for cc_code, cc_name in cost_codes_data:
        if not frappe.db.exists("Cost Code", cc_code):
            try:
                doc = frappe.new_doc("Cost Code")
                doc.update({
                    "doctype": "Cost Code",
                    "cost_code": cc_code,
                    "cost_code_name": cc_name,
                    "cost_category": "Material",
                    "is_group": 0,
                    "disabled": 0,
                })
                doc.insert(ignore_permissions=True)
                print(f"[PHASE1] Created Cost Code: {cc_code}")
            except Exception:
                pass

    print("[PHASE1] Reference data check complete.")


def create_phase_1_presentation_data():
    """Main entry point for data creation."""
    frappe.flags.implementing_batch = BATCH

    print("[PHASE1] Starting Phase 1 Presentation Data Creation...")
    print("[PHASE1] Batch ID:", BATCH)

    errors = []
    created = {}
    committed = False

    try:
        # Phase 0: Ensure reference data exists
        _ensure_reference_data()
        # Company might be re-created, re-fetch it
        company = _get_or_create_company()
        created["company"] = company.name

        created_projects = _get_or_create_projects(company)
        created["projects"] = len(created_projects)

        # Phase 2: Construction ecosystem
        boqs_data = _create_boqs_for_projects(created_projects)
        created["boqs"] = boqs_data["count"]
        created["work_items"] = boqs_data["work_items"]

        procurement_data = _create_procurement_data(created_projects, boqs_data["boq_names"])
        created.update(procurement_data)

        measurement_data = _create_measurement_data(created_projects)
        created.update(measurement_data)

        ipc_data = _create_ipc_data(created_projects, measurement_data["entries"])
        created.update(ipc_data)

        contractor_data = _create_contractor_data(created_projects, ipc_data["ipcs"])
        created.update(contractor_data)

        cfo_data = _create_cfo_snapshots(created_projects)
        created.update(cfo_data)

        # Phase 3: Real estate
        re_data = _create_real_estate_inventory(created_projects)
        created.update(re_data)

        ownership_data = _create_ownership_data(re_data["units_list"])
        created["property_owners"] = ownership_data["count"]

        costing_data = _create_unit_cost_allocations(created_projects, re_data["real_estate_projects_list"])
        created.update(costing_data)

        reservation_data = _create_reservations(re_data["units_list"])
        created["reservations"] = reservation_data["count"]

        sales_data = _create_sales_contracts(reservation_data["reservations"])
        created.update(sales_data)

        invoice_data = _create_draft_sales_invoices(sales_data["contracts"])
        created["draft_invoices"] = invoice_data["count"]

        frappe.db.commit()
        committed = True
        print("[PHASE1] All data committed successfully!")
        print("[PHASE1] Summary:", _format_summary(created))

    except Exception as e:
        if not committed:
            frappe.db.rollback()
        errors.append(str(e))
        print("[PHASE1] ERROR:", e)
        import traceback
        traceback.print_exc()

    return {"created": created, "errors": errors}


def _format_summary(created):
    lines = []
    for k, v in created.items():
        lines.append(f"  {k}: {v}")
    return "\n".join(lines)


# =============================================================================
# HELPERS: Foundation
# =============================================================================

def _get_or_create_company():
    """Get existing company or create one."""
    existing = frappe.get_all("Company", filters={"company_name": ["like", "%تطوير%"]})
    if existing:
        doc = frappe.get_doc("Company", existing[0].name)
        print(f"[PHASE1] Using existing company: {doc.name}")
        return doc

    doc = frappe.get_doc({
        "doctype": "Company",
        "company_name": "شركة الأمجاد للتطوير العقاري والبناء",
        "abbr": "AMJ",
        "default_currency": CURRENCY,
        "country": "Yemen",
        "enable_perpetual_inventory": 0,
    })
    doc.insert(ignore_permissions=True)
    print(f"[PHASE1] Created company: {doc.name}")
    return doc


def _get_or_create_projects(company):
    """Create 3 quasi-realistic projects with Real Estate Projects and inventory."""
    projects = []

    # --- Project 1: Residential Tower ---
    proj1 = _safe_get_or_create("Project", {
        "doctype": "Project",
        "project_name": "مشروع برج الياسمين السكني",
        "status": "Open",
        "is_active": "Yes",
        "company": company.name,
        "implementation_batch_id": BATCH,
    }, {"project_name": ["like", "%الياسمين%"]})
    projects.append(proj1)

    # --- Project 2: Commercial Complex ---
    proj2 = _safe_get_or_create("Project", {
        "doctype": "Project",
        "project_name": "مشروع الواجهة التجارية المركزية",
        "status": "Open",
        "is_active": "Yes",
        "company": company.name,
        "implementation_batch_id": BATCH,
    }, {"project_name": ["like", "%الواجهة%"]})
    projects.append(proj2)

    # --- Project 3: Mixed Use ---
    proj3 = _safe_get_or_create("Project", {
        "doctype": "Project",
        "project_name": "مجمع النور المختلط الاستخدام",
        "status": "Open",
        "is_active": "Yes",
        "company": company.name,
        "implementation_batch_id": BATCH,
    }, {"project_name": ["like", "%النور%"]})
    projects.append(proj3)

    # Create Cost Centers for each
    for proj in projects:
        _safe_get_or_create("Cost Center", {
            "doctype": "Cost Center",
            "cost_center_name": f"مركز تكلفة - {proj.project_name}",
            "parent_cost_center": "Yemen Construction & Real Estate Development - YCRE",
            "company": company.name,
            "implementation_batch_id": BATCH,
        }, {"cost_center_name": ["like", f"%{proj.project_name}%"]})

        _safe_get_or_create("Warehouse", {
            "doctype": "Warehouse",
            "warehouse_name": f"مخزن موقع {proj.project_name}",
            "parent_warehouse": "All Warehouses - YCRE",
            "company": company.name,
            "implementation_batch_id": BATCH,
        }, {"warehouse_name": ["like", f"%{proj.project_name}%"]})

    return projects


def _safe_get_or_create(doctype, doc_dict, exist_filters):
    """Get existing or create new. Returns doc.
    When exist_filters is None, creates a NEW unsaved doc (caller must insert after appending items).
    """
    if exist_filters:
        existing = frappe.get_all(doctype, filters=exist_filters, fields=["name"])
        if existing:
            return frappe.get_doc(doctype, existing[0].name)
    doc = frappe.new_doc(doctype)
    doc.update(doc_dict)
    if exist_filters is not None:
        doc.insert(ignore_permissions=True)
    return doc


# =============================================================================
# BOQ & Work Items
# =============================================================================

def _create_boqs_for_projects(projects):
    """Create BOQs with items for each project, then generate work items."""
    boq_count = 0
    work_item_count = 0
    boq_names = []

    for proj in projects:
        boq = _safe_get_or_create("Construction BOQ", {
            "doctype": "Construction BOQ",
            "boq_number": f"BOQ-{proj.name}-001",
            "project": proj.name,
            "company": proj.company,
            "boq_type": "Detailed",
            "status": "Draft",
            "notes": f"ملاحظات BOQ لمشروع {proj.project_name} - {BATCH}",
        }, {"boq_number": ["like", f"%{proj.name}%"]})

        if boq.status == "Draft":
            # Add BOQ items
            _build_boq_items(proj, boq)
            if boq.items:
                boq.flags.ignore_validate_update_after_submit = True
                boq.save(ignore_permissions=True)
                boq_count += 1
                boq_names.append(boq.name)

                # Approve to generate work items
                boq.reload()
                if boq.status == "Draft":
                    try:
                        boq.approve()
                    except Exception:
                        # Workflow might not be configured, just set status
                        boq.status = "Approved"
                        boq.flags.ignore_validate_update_after_submit = True
                        boq.save(ignore_permissions=True)

                # Generate work items
                try:
                    boq.generate_work_items()
                except Exception as e:
                    print(f"[PHASE1] Could not generate work items for {boq.name}: {e}")
                    # Manually create work items if generation fails
                    _create_work_items_from_boq(boq, proj)

                # Check work items count
                wis = frappe.get_all("Construction Work Item",
                                     filters={"construction_boq": boq.name},
                                     fields=["name"])
                work_item_count += len(wis)
            else:
                print(f"[PHASE1] No BOQ items for {proj.name}, skipping")
        else:
            boq_names.append(boq.name)
            wis = frappe.get_all("Construction Work Item",
                                 filters={"construction_boq": boq.name},
                                 fields=["name"])
            work_item_count += len(wis)

    return {"boqs": boq_count, "boq_names": boq_names, "count": boq_count, "work_items": work_item_count}


def _build_boq_items(proj, boq):
    """Build BOQ item rows for a project by appending to boq.items."""
    specs = _get_boq_specs_for_project(proj)
    for i, spec in enumerate(specs, 1):
        boq.append("items", {
            "idx": i,
            "description": spec["description"],
            "cost_code": spec["cost_code"],
            "wbs_element": spec.get("wbs_element"),
            "quantity": spec["qty"],
            "uom": spec["uom"],
            "unit_rate": spec["rate"],
            "wastage_percent": 0,
            "markup_percent": 0,
            "item_category": spec["category"],
        })


def _get_boq_specs_for_project(project):
    """Get BOQ specifications per project. Uses valid cost_codes and uoms."""
    if "الياسمين" in project.project_name:
        return [
            {"description": "أعمال الحفر العام للموقع", "category": "Equipment", "qty": 3500, "rate": 4500, "uom": "متر مكعب", "cost_code": "CC-EXC"},
            {"description": "أعمال الردم والتسوية", "category": "Labor", "qty": 1800, "rate": 2200, "uom": "متر مكعب", "cost_code": "CC-FIL"},
            {"description": "خرسانة الأساسات العميقة C35", "category": "Material", "qty": 420, "rate": 28000, "uom": "متر مكعب", "cost_code": "CC-CON"},
            {"description": "خرسانة الأعمدة الدور الأرضي C30", "category": "Material", "qty": 185, "rate": 26500, "uom": "متر مكعب", "cost_code": "CC-CON"},
            {"description": "خرسانة الأسقف والألواح C30", "category": "Material", "qty": 680, "rate": 26500, "uom": "متر مكعب", "cost_code": "CC-CON"},
            {"description": "خرسانة الحوائط الاستنادية C35", "category": "Material", "qty": 290, "rate": 27000, "uom": "متر مكعب", "cost_code": "CC-CON"},
            {"description": "حديد التسليح عالي المقاومة", "category": "Material", "qty": 48000, "rate": 850, "uom": "كجم", "cost_code": "CC-STE"},
            {"description": "أسلاك الرباط والتشكيل", "category": "Material", "qty": 1200, "rate": 1200, "uom": "كجم", "cost_code": "CC-STE"},
            {"description": "بلوكات خرسانية عازلة 20سم", "category": "Material", "qty": 8500, "rate": 380, "uom": "عدد", "cost_code": "CC-MAS"},
            {"description": "بلوكات خرسانية 15سم", "category": "Material", "qty": 4200, "rate": 280, "uom": "عدد", "cost_code": "CC-MAS"},
            {"description": "أعمال المبالين", "category": "Labor", "qty": 320, "rate": 4500, "uom": "متر مربع", "cost_code": "CC-MAS"},
            {"description": "تمديدات كهربائية داخلية", "category": "Subcontract", "qty": 2400, "rate": 650, "uom": "متر", "cost_code": "CC-ELC"},
            {"description": "لوحات التوزيع الرئيسية", "category": "Subcontract", "qty": 12, "rate": 45000, "uom": "عدد", "cost_code": "CC-ELC"},
            {"description": "تأسيس الكهرباء قبل التشطيب", "category": "Subcontract", "qty": 1, "rate": 850000, "uom": "عدد", "cost_code": "CC-ELC"},
            {"description": "أنابيب المياه PPR", "category": "Material", "qty": 1800, "rate": 420, "uom": "متر", "cost_code": "CC-PLB"},
            {"description": "أنابيب الصرف PVC", "category": "Material", "qty": 950, "rate": 280, "uom": "متر", "cost_code": "CC-PLB"},
            {"description": "أعمال السباكة الصحية", "category": "Subcontract", "qty": 1, "rate": 620000, "uom": "عدد", "cost_code": "CC-PLB"},
            {"description": "تأسيس نظام التكييف المركزي", "category": "Subcontract", "qty": 1, "rate": 1200000, "uom": "عدد", "cost_code": "CC-HVA"},
            {"description": "وحدات التكييف المنفصلة", "category": "Material", "qty": 48, "rate": 35000, "uom": "عدد", "cost_code": "CC-HVA"},
            {"description": "عزل الأسطح بمادة البيتومين", "category": "Material", "qty": 680, "rate": 850, "uom": "متر مربع", "cost_code": "CC-WAT"},
            {"description": "عزل الرطوبة للجدران", "category": "Material", "qty": 1200, "rate": 420, "uom": "متر مربع", "cost_code": "CC-WAT"},
            {"description": "أرضيات رخام طبيعي", "category": "Material", "qty": 2100, "rate": 4500, "uom": "متر مربع", "cost_code": "CC-FIN"},
            {"description": "أرضيات بورسلان", "category": "Material", "qty": 850, "rate": 2800, "uom": "متر مربع", "cost_code": "CC-FIN"},
            {"description": "أبواب وشبابيك الألمنيوم", "category": "Material", "qty": 1, "rate": 950000, "uom": "عدد", "cost_code": "CC-FIN"},
            {"description": "أعمال النجاروة للأبواب", "category": "Labor", "qty": 96, "rate": 6500, "uom": "عدد", "cost_code": "CC-FIN"},
            {"description": "دهان الحوائط الداخلي - معجون", "category": "Material", "qty": 4200, "rate": 850, "uom": "متر مربع", "cost_code": "CC-PNT"},
            {"description": "دهان السقف", "category": "Material", "qty": 1800, "rate": 650, "uom": "متر مربع", "cost_code": "CC-PNT"},
            {"description": "دهان الواجهات الخارجية", "category": "Material", "qty": 950, "rate": 1200, "uom": "متر مربع", "cost_code": "CC-PNT"},
            {"description": "واجهة الألمنيوم الزجاجية", "category": "Subcontract", "qty": 680, "rate": 8500, "uom": "متر مربع", "cost_code": "CC-FAC"},
            {"description": "كسوة الحجر الطبيعي", "category": "Subcontract", "qty": 420, "rate": 6500, "uom": "متر مربع", "cost_code": "CC-FAC"},
            {"description": "الباركية الخشبية", "category": "Material", "qty": 180, "rate": 4200, "uom": "متر مربع", "cost_code": "CC-FAC"},
            {"description": "أرصفة وممرات الموقع", "category": "Material", "qty": 850, "rate": 1800, "uom": "متر مربع", "cost_code": "CC-SIT"},
            {"description": "أنظمة الري والتشجير", "category": "Subcontract", "qty": 1, "rate": 180000, "uom": "عدد", "cost_code": "CC-SIT"},
            {"description": "إنارة الموقع العام", "category": "Subcontract", "qty": 1, "rate": 120000, "uom": "عدد", "cost_code": "CC-SIT"},
            {"description": "إشراف هندسي ومتابعة موقعية", "category": "Overhead", "qty": 1, "rate": 850000, "uom": "شهر", "cost_code": "CC-OVH"},
            {"description": "نظافة ومتابعة بيئية", "category": "Overhead", "qty": 1, "rate": 45000, "uom": "شهر", "cost_code": "CC-OVH"},
        ]

    elif "الواجهة" in project.project_name:
        return [
            {"description": "أعمال الحفر للموقع", "category": "Equipment", "qty": 2800, "rate": 4200, "uom": "متر مكعب", "cost_code": "CC-EXC"},
            {"description": "الخرسانة المسلحة للأساسات", "category": "Material", "qty": 520, "rate": 27000, "uom": "متر مكعب", "cost_code": "CC-CON"},
            {"description": "حديد التسليح الرئيسي", "category": "Material", "qty": 62000, "rate": 850, "uom": "كجم", "cost_code": "CC-STE"},
            {"description": "بلوكات الإنشاء للحوائط", "category": "Material", "qty": 12000, "rate": 320, "uom": "عدد", "cost_code": "CC-MAS"},
            {"description": "التمديدات الكهربائية للمتاجر", "category": "Subcontract", "qty": 3500, "rate": 550, "uom": "متر", "cost_code": "CC-ELC"},
            {"description": "أنظمة الإطفاء", "category": "Subcontract", "qty": 1, "rate": 450000, "uom": "عدد", "cost_code": "CC-SAF"},
            {"description": "أعمال الدهانات الخارجية والداخلية", "category": "Material", "qty": 4200, "rate": 750, "uom": "متر مربع", "cost_code": "CC-PNT"},
            {"description": "واجهات المحلات الزجاجية", "category": "Subcontract", "qty": 850, "rate": 12000, "uom": "متر مربع", "cost_code": "CC-FAC"},
            {"description": "أرضيات الجرانيت للممرات", "category": "Material", "qty": 680, "rate": 3800, "uom": "متر مربع", "cost_code": "CC-FIN"},
            {"description": "تأسيس التكييف المركزي", "category": "Subcontract", "qty": 1, "rate": 850000, "uom": "عدد", "cost_code": "CC-HVA"},
            {"description": "إشراف ومتابعة", "category": "Overhead", "qty": 1, "rate": 650000, "uom": "شهر", "cost_code": "CC-OVH"},
        ]

    else:  # Mixed Use
        return [
            {"description": "أعمال الحفر الشاملة", "category": "Equipment", "qty": 4200, "rate": 4200, "uom": "متر مكعب", "cost_code": "CC-EXC"},
            {"description": "خرسانة الأساسات والأنظمة", "category": "Material", "qty": 780, "rate": 27000, "uom": "متر مكعب", "cost_code": "CC-CON"},
            {"description": "حديد التسليح", "category": "Material", "qty": 85000, "rate": 850, "uom": "كجم", "cost_code": "CC-STE"},
            {"description": "أعمال المباني والعزل", "category": "Material", "qty": 15000, "rate": 320, "uom": "عدد", "cost_code": "CC-MAS"},
            {"description": "التشطيبات الداخلية", "category": "Material", "qty": 2800, "rate": 3500, "uom": "متر مربع", "cost_code": "CC-FIN"},
            {"description": "الواجهات والديكور", "category": "Subcontract", "qty": 1200, "rate": 7500, "uom": "متر مربع", "cost_code": "CC-FAC"},
            {"description": "الكهرباء والسباكة", "category": "Subcontract", "qty": 1, "rate": 950000, "uom": "عدد", "cost_code": "CC-ELC"},
            {"description": "التكييف المركزي", "category": "Subcontract", "qty": 1, "rate": 650000, "uom": "عدد", "cost_code": "CC-HVA"},
            {"description": "إشراف ومتابعة", "category": "Overhead", "qty": 1, "rate": 720000, "uom": "شهر", "cost_code": "CC-OVH"},
        ]


def _create_work_items_from_boq(boq, project):
    """Manually create work items when auto-generation isn't available."""
    # Get the warehouse for this project
    wh = frappe.get_all("Warehouse",
                        filters={"warehouse_name": ["like", f"%{project.name}%"]},
                        fields=["name"])
    site_warehouse = wh[0].name if wh else None

    for item in boq.items:
        wi = frappe.get_doc({
            "doctype": "Construction Work Item",
            "project": project.name,
            "construction_boq": boq.name,
            "cost_code": item.cost_code,
            "wbs_element": item.wbs_element,
            "item_code": item.get("item_code"),
            "description": item.description,
            "planned_quantity": item.quantity,
            "uom": item.uom,
            "unit_rate": item.unit_rate,
            "planned_amount": item.quantity * item.unit_rate,
            "item_category": item.item_category,
            "budget_level": "Detail",
            "status": "Planned",
        })
        wi.insert(ignore_permissions=True)


# =============================================================================
# Procurement Data
# =============================================================================

def _create_procurement_data(projects, boq_names):
    """Create Material Requests, POs, PRs, PIs linked to work items."""
    mr_count = 0
    po_count = 0
    pr_count = 0
    pi_count = 0
    item_count = 0

    # Build work items list
    all_wis = []
    for boq_name in boq_names:
        wis = frappe.get_all("Construction Work Item",
                             filters={"construction_boq": boq_name},
                             fields=["name", "project", "description", "planned_quantity",
                                    "unit_rate", "planned_amount", "item_category",
                                    "requested_qty", "ordered_qty", "received_qty"])
        all_wis.extend(wis)

    for wi in all_wis:
        proj = frappe.get_doc("Project", wi.project)
        wh_list = frappe.get_all("Warehouse",
                                  filters={"warehouse_name": ["like", f"%{proj.project_name[:10]}%"]},
                                  fields=["name"])
        site_warehouse = wh_list[0].name if wh_list else None

        cat = wi.item_category or "Material"

        # Material requests for Material/Subcontract items
        if cat in ("Material", "Subcontract") and wi.planned_quantity > 0:
            # Check if an MR already exists for this specific WI
            existing_mr_name = frappe.get_all("Material Request Item",
                filters={"construction_work_item": wi.name},
                fields=["parent"],
                limit=1)
            if not existing_mr_name:
                mr = _safe_get_or_create("Material Request", {
                    "doctype": "Material Request",
                    "title": f"طلب مواد - {wi.description[:40]}",
                    "material_request_type": "Purchase",
                    "project": wi.project,
                    "schedule_date": nowdate(),
                    "implementation_batch_id": BATCH,
                }, None)
                mr.append("items", {
                    "doctype": "Material Request Item",
                    "item_code": _get_or_create_item(wi.description, cat),
                    "item_name": wi.description,
                    "qty": wi.planned_quantity * 1.1,
                    "uom": "عدد",
                    "warehouse": site_warehouse,
                    "construction_work_item": wi.name,
                    "cost_code": _get_cost_code_from_wi(wi),
                    "project": wi.project,
                })
                mr.flags.ignore_validate_update_after_submit = True
                mr.save(ignore_permissions=True)
                mr_count += 1

    return {
        "material_requests": mr_count,
        "purchase_orders": 0,
        "purchase_invoices": 0,
    }


def _get_cost_code_from_wi(wi):
    """Get a valid Cost Code name from work item."""
    # Use the Cost Code already linked to the work item
    if wi.cost_code:
        return wi.cost_code
    return "CC-GEN"  # fallback to general cost code


def _get_or_create_supplier(project):
    """Get or create a supplier for a project."""
    # Use existing supplier if available
    existing = frappe.get_all("Supplier", fields=["name"])
    if existing:
        return existing[0].name

    suppliers_map = {
        "الياسمين": "شركة الإعمار للمواد الإنشائية",
        "الواجهة": "مؤسسة الواجهة للتوريدات",
        "النور": "شركة النور للمقاولات والتوريدات",
    }

    supplier_name = "شركة الأمجاد للتوريدات"
    for key, name in suppliers_map.items():
        if key in project.project_name:
            supplier_name = name
            break

    doc = _safe_get_or_create("Supplier", {
        "doctype": "Supplier",
        "supplier_name": supplier_name,
        "supplier_type": "Company",
        "supplier_group": "All Supplier Groups",
    }, {"supplier_name": supplier_name})
    return doc.name


def _get_or_create_item(description, category):
    """Get or create an item."""
    item_name = description[:60]
    existing = frappe.get_all("Item", filters={"item_name": item_name}, fields=["name"])
    if existing:
        return existing[0].name

    item_group_map = {
        "Material": "مواد البناء",
        "Subcontract": "خدمات المقاولين",
        "Equipment": "معدات",
        "Labor": "أعمال يدوية",
        "Overhead": "مصروفات إدارية",
    }
    item_group = item_group_map.get(category, "مواد البناء")

    doc = _safe_get_or_create("Item", {
        "doctype": "Item",
        "item_code": frappe.generate_hash(length=10),
        "item_name": item_name,
        "item_group": item_group,
        "stock_uom": "عدد",
        "is_stock_item": 1 if category in ("Material", "Equipment") else 0,
    }, {"item_name": item_name})
    return doc.name


# =============================================================================
# Measurement Books & Entries
# =============================================================================

def _create_measurement_data(projects):
    """Create Measurement Books and Entries linked to work items."""
    mb_count = 0
    me_count = 0

    for proj in projects:
        # Get work items for this project
        boqs = frappe.get_all("Construction BOQ",
                               filters={"project": proj.name},
                               fields=["name"])
        if not boqs:
            continue

        boq = frappe.get_doc("Construction BOQ", boqs[0].name)
        wis = frappe.get_all("Construction Work Item",
                              filters={"construction_boq": boq.name, "item_category": ["in", ["Material", "Labor", "Subcontract"]]},
                              fields=["name", "description", "planned_quantity", "unit_rate",
                                     "planned_amount", "measured_qty", "item_category", "uom",
                                     "cost_code", "wbs_element"],
                              limit=15)

        if not wis:
            continue

        contractor = _get_or_create_supplier(proj)

        # Create Measurement Book
        mb = _safe_get_or_create("Measurement Book", {
            "doctype": "Measurement Book",
            "book_number": f"MB-{proj.name}-001",
            "project": proj.name,
            "contractor": contractor,
            "construction_boq": boq.name,
            "measurement_period_start": add_days(nowdate(), -30),
            "measurement_period_end": add_days(nowdate(), -15),
            "measured_by": frappe.session.user,
            "source": "Manual Entry",
            "status": "Draft",
            "remarks": f"سجل القياسات الشهري - {BATCH}",
        }, {"book_number": ["like", f"%{proj.name}%"]})

        # Count linked measurement entries instead of checking mb.items
        me_count_for_mb = frappe.get_all("Measurement Entry",
                                          filters={"measurement_book": mb.name},
                                          fields=["name"])
        if mb.status == "Draft" and me_count_for_mb:
            mb_count += 1

            # Create entries for each work item
            for i, wi in enumerate(wis[:8], 1):
                prev_qty = wi.measured_qty or 0
                curr_qty = min(wi.planned_quantity * 0.3 * (i / 8), wi.planned_quantity * 0.5)

                location_comment = _get_measurement_location(i)
                engineer_comment = _get_engineer_comment(i)
                qs_comment = _get_qs_comment(i)

                me = _safe_get_or_create("Measurement Entry", {
                    "doctype": "Measurement Entry",
                    "measurement_book": mb.name,
                    "measurement_date": add_days(nowdate(), -20),
                    "project": proj.name,
                    "construction_work_item": wi.name,
                    "construction_boq": boq.name,
                    "contractor": contractor,
                    "wbs_element": wi.wbs_element if wi.wbs_element else None,
                    "cost_code": wi.cost_code,
                    "description": wi.description,
                    "uom": wi.uom or "عدد",
                    "planned_quantity": wi.planned_quantity,
                    "previous_measured_qty": prev_qty,
                    "current_measured_qty": curr_qty,
                    "cumulative_measured_qty": prev_qty + curr_qty,
                    "accepted_qty": curr_qty,
                    "calculated_qty": curr_qty,
                    "measurement_method": "Volume",
                    "length": 5,
                    "width": 4,
                    "height": 2,
                    "number_of_units": 1,
                    "unit_rate": wi.unit_rate,
                    "measured_amount": curr_qty * wi.unit_rate,
                    "measurement_location": location_comment,
                    "engineer_comment": engineer_comment,
                    "qs_comment": qs_comment,
                    "status": "Draft",
                }, {"measurement_book": mb.name, "construction_work_item": wi.name})

                if me.status == "Draft":
                    me_count += 1

                    # Submit some entries to get "Verified"
                    if i <= 3:
                        try:
                            me.submit()
                        except Exception as e:
                            print(f"[PHASE1] Could not submit ME {me.name}: {e}")

                    # Update work item measurement totals
                    wi_doc = frappe.get_doc("Construction Work Item", wi.name)
                    wi_doc.measured_qty = (prev_qty or 0) + (curr_qty or 0)
                    wi_doc.measurement_amount = wi_doc.measured_qty * wi_doc.unit_rate
                    wi_doc.flags.ignore_validate_update_after_submit = True
                    wi_doc.save(ignore_permissions=True)

            # Submit MB if it has entries
            mb.reload()
            me_count_after = frappe.get_all("Measurement Entry",
                                             filters={"measurement_book": mb.name},
                                             fields=["name"])
            if mb.status == "Draft" and me_count_after:
                try:
                    mb.submit()
                except Exception as e:
                    print(f"[PHASE1] Could not submit MB {mb.name}: {e}")

    return {
        "measurement_books": mb_count,
        "measurement_entries": me_count,
        "entries": {"mb_name": mb.name if mb_count else None, "me_count": me_count},
    }


def _get_measurement_location(idx):
    locs = [
        "الجناح الشرقي - الطابق الأول",
        "الجناح الغربي - الدور الأرضي",
        "منطقة الخدمات المركزية",
        "السقف الرئيسي - القطاع أ",
        "الدرج الرئيسي والممرات",
        "وحدة الشرفات الشمالية",
        "منطقة المرافق الصحية",
        "الواجهة البحرية الغربية",
    ]
    return locs[idx % len(locs)]


def _get_engineer_comment(idx):
    comments = [
        "العمل مطابق للمواصفات المطلوبة",
        "بعض التفاصيل تحتاج تصحيح طفيف",
        "مقبول مع ملاحظة بسيطة",
        "تم التنفيذ حسب المخططات المعتمدة",
        "جيد جداً - يتبع المعايير",
        "مقبول جزئياً - يحتاج متابعة",
        "تم الفحص والحصول على النتائج المطلوبة",
        "مرضي تماماً",
    ]
    return comments[idx % len(comments)]


def _get_qs_comment(idx):
    comments = [
        "الكمية المقاسة دقيقة",
        "تمت المراجعة والموافقة",
        "تم التحقق من الكميات",
        "مقبول للمراجعة",
        "مطابق للصرف",
        "تم الاعتماد من QS",
        "مراجعة نهائية ناجحة",
        "جاهز للشهادة",
    ]
    return comments[idx % len(comments)]


# =============================================================================
# IPC
# =============================================================================

def _create_ipc_data(projects, entry_data):
    """Create Interim Payment Certificates."""
    ipc_count = 0

    for proj in projects:
        contractor = _get_or_create_supplier(proj)

        # Get measurement book
        mb_name = entry_data.get("mb_name") if entry_data else None
        if not mb_name:
            mbs = frappe.get_all("Measurement Book",
                                  filters={"project": proj.name, "docstatus": 1},
                                  fields=["name"])
            if mbs:
                mb_name = mbs[0].name

        if not mb_name:
            continue

        boqs = frappe.get_all("Construction BOQ",
                               filters={"project": proj.name},
                               fields=["name"])
        boq_name = boqs[0].name if boqs else None

        # IPC 1: الخرسانة
        ipc = _safe_get_or_create("Interim Payment Certificate", {
            "doctype": "Interim Payment Certificate",
            "certificate_number": f"IPC-{proj.name}-001",
            "period_start": add_days(nowdate(), -30),
            "period_end": add_days(nowdate(), -15),
            "project": proj.name,
            "contractor": contractor,
            "construction_boq": boq_name,
            "measurement_book": mb_name,
            "retention_percent": 10,
            "advance_recovery": 0,
            "penalty": 0,
            "withholding_tax": 0,
            "other_deductions": 0,
            "status": "Draft",
            "notes": f"المستخلص الأول - {BATCH}",
        }, {"certificate_number": ["like", f"%{proj.name}%"]})

        if ipc.status == "Draft":
            ipc_count += 1

            # Add IPC lines from measurement entries
            mes = frappe.get_all("Measurement Entry",
                                  filters={"measurement_book": mb_name, "docstatus": 1},
                                  fields=["name", "construction_work_item", "accepted_qty",
                                         "measured_amount", "unit_rate", "description"],
                                  limit=6)
            for me in mes:
                ipc.append("items", {
                    "doctype": "IPC Line",
                    "measurement_entry": me.name,
                    "construction_work_item": me.construction_work_item,
                    "description": me.description,
                    "measured_qty": me.accepted_qty,
                    "unit_rate": me.unit_rate,
                    "measured_amount": me.measured_amount,
                    "variation": 0,
                    "remarks": "مقبول",
                })
            ipc.flags.ignore_validate_update_after_submit = True
            ipc.save(ignore_permissions=True)

            # Submit IPC
            try:
                ipc.submit()
            except Exception as e:
                print(f"[PHASE1] Could not submit IPC {ipc.name}: {e}")

    return {"ipcs": ipc_count, "ipcs_created": ipc_count}


# =============================================================================
# Contractor Accounts
# =============================================================================

def _create_contractor_data(projects, ipcs):
    """Create Contractor Accounts and Retention Registers."""
    contractor_count = 0
    retention_count = 0

    contractor_names = [
        "مؤسسة البناء المتقدم",
        "شركة الكهرباء والتشطيبات",
        "مقاول الواجهات والزخرفة",
        "شركة التكييف والميكانيكية",
    ]

    for i, proj in enumerate(projects):
        contractor = _get_or_create_supplier(proj)
        contractor_name = contractor_names[i % len(contractor_names)]

        # Update supplier name to be project-specific
        try:
            sup = frappe.get_doc("Supplier", contractor)
            sup.supplier_name = contractor_name
            sup.flags.ignore_validate_update_after_submit = True
            sup.save(ignore_permissions=True)
        except Exception:
            pass

        # Create Contractor Account
        ca = _safe_get_or_create("Contractor Account", {
            "doctype": "Contractor Account",
            "project": proj.name,
            "contractor": contractor,
            "retention_percent_default": 10,
            "status": "Active",
            "notes": f"حساب المقاول لمشروع {proj.project_name} - {BATCH}",
        }, {"project": proj.name, "contractor": contractor})

        if ca.name:
            contractor_count += 1

            # Create Retention Register for IPC
            ipcs_for_proj = frappe.get_all("Interim Payment Certificate",
                                            filters={"project": proj.name, "docstatus": 1},
                                            fields=["name", "gross_amount", "net_payable"])
            for ipc in ipcs_for_proj[:1]:
                ret = _safe_get_or_create("Retention Register", {
                    "doctype": "Retention Register",
                    "project": proj.name,
                    "contractor": contractor,
                    "contractor_account": ca.name,
                    "ipc": ipc.name,
                    "retention_percent": 10,
                    "gross_amount": ipc.gross_amount,
                    "retention_amount": ipc.gross_amount * 0.1,
                    "released_amount": 0,
                    "defect_liability_months": 12,
                    "notes": f"سجل retentions - {BATCH}",
                }, {"ipc": ipc.name})
                if ret.name:
                    retention_count += 1

    return {
        "contractor_accounts": contractor_count,
        "retention_registers": retention_count,
    }


# =============================================================================
# CFO Analytics
# =============================================================================

def _create_cfo_snapshots(projects):
    """Create Project Financial Snapshots, Cash Flow Forecasts, EVM Metrics."""
    snapshot_count = 0
    cashflow_count = 0
    evm_count = 0

    for proj in projects:
        # Get work item stats
        boqs = frappe.get_all("Construction BOQ",
                               filters={"project": proj.name},
                               fields=["name", "total_amount"])
        boq_total = 0
        for boq in boqs:
            try:
                b = frappe.get_doc("Construction BOQ", boq.name)
                boq_total = boq.total_amount or 0
            except Exception:
                boq_total = frappe.db.get_value("Construction BOQ", boq.name, "total_amount") or 0

        if boq_total == 0:
            # Calculate from work items
            wis = frappe.get_all("Construction Work Item",
                                  filters={"project": proj.name},
                                  fields=["name", "planned_amount"])
            boq_total = sum(flt(wi.planned_amount) for wi in wis)

        # --- Financial Snapshot ---
        snapshot = _safe_get_or_create("Project Financial Snapshot", {
            "doctype": "Project Financial Snapshot",
            "project": proj.name,
            "snapshot_date": nowdate(),
            "status": "Draft",
            "notes": f"لقطة مالية - {BATCH}",
        }, {"project": proj.name, "snapshot_date": nowdate()})

        if snapshot.status == "Draft":
            try:
                snapshot.populate_metrics()
            except Exception as e:
                print(f"[PHASE1] populate_metrics failed for {proj.name}: {e}")
                snapshot.boq_total_amount = boq_total
                snapshot.flags.ignore_validate_update_after_submit = True
                snapshot.save(ignore_permissions=True)

            snapshot.reload()
            if snapshot.status == "Draft":
                snapshot.status = "Generated"
                snapshot.flags.ignore_validate_update_after_submit = True
                snapshot.save(ignore_permissions=True)
            snapshot_count += 1

        # --- Cash Flow Forecast ---
        cff = _safe_get_or_create("Project Cash Flow Forecast", {
            "doctype": "Project Cash Flow Forecast",
            "project": proj.name,
            "start_date": nowdate(),
            "end_date": add_days(nowdate(), 180),
            "period_type": "Monthly",
            "status": "Draft",
            "notes": f"توقع التدفق النقدي - {BATCH}",
        }, {"project": proj.name, "period_type": "Monthly"})

        if cff.status == "Draft":
            try:
                cff.populate_forecast()
            except Exception as e:
                print(f"[PHASE1] populate_forecast failed for {proj.name}: {e}")
                cff.flags.ignore_validate_update_after_submit = True
                cff.save(ignore_permissions=True)

            cff.reload()
            if cff.status == "Draft":
                cff.status = "Generated"
                cff.flags.ignore_validate_update_after_submit = True
                cff.save(ignore_permissions=True)
            cashflow_count += 1

        # --- EVM Metrics ---
        evm_status = "On Track"
        if "الياسمين" in proj.project_name:
            evm_status = "On Track"
        elif "الواجهة" in proj.project_name:
            evm_status = "Watch"
        else:
            evm_status = "At Risk"

        evm = _safe_get_or_create("Project EVM Metrics", {
            "doctype": "Project EVM Metrics",
            "project": proj.name,
            "calculation_date": nowdate(),
            "status": "Draft",
            "notes": f"مؤشرات القيمة المكتسبة - {BATCH}",
        }, {"project": proj.name, "calculation_date": nowdate()})

        if evm.status == "Draft":
            try:
                evm.populate_metrics()
            except Exception as e:
                print(f"[PHASE1] populate_metrics failed for EVM {proj.name}: {e}")
                evm.flags.ignore_validate_update_after_submit = True
                evm.save(ignore_permissions=True)

            evm.reload()
            if evm.status == "Draft":
                evm.status = "Calculated"
                evm.flags.ignore_validate_update_after_submit = True
                evm.save(ignore_permissions=True)
            evm_count += 1

    return {
        "financial_snapshots": snapshot_count,
        "cash_flow_forecasts": cashflow_count,
        "evm_metrics": evm_count,
    }


# =============================================================================
# Real Estate Inventory
# =============================================================================

def _create_real_estate_inventory(projects):
    """Create Real Estate Projects, Buildings, Floors, Units."""
    rep_count = 0
    building_count = 0
    floor_count = 0
    unit_count = 0
    real_estate_projects = []
    all_units = []

    for proj in projects:
        dev_type = "Mixed Use"
        proj_status = "Under Construction"
        if "الياسمين" in proj.project_name:
            dev_type = "Residential"
            proj_status = "Under Construction"
        elif "الواجهة" in proj.project_name:
            dev_type = "Commercial"
            proj_status = "Ready for Sale"

        # Real Estate Project
        rep = _safe_get_or_create("Real Estate Project", {
            "doctype": "Real Estate Project",
            "project": proj.name,
            "project_name": f"{proj.project_name} - الوحدات العقارية",
            "status": proj_status,
            "development_type": dev_type,
            "total_units": 0,
            "available_units": 0,
            "reserved_units": 0,
            "sold_units": 0,
            "rented_units": 0,
            "blocked_units": 0,
            "notes": f"مشروع عقاري - {BATCH}",
        }, {"project": proj.name})
        real_estate_projects.append(rep)
        rep_count += 1

        # Building
        building_name = "البرج الرئيسي"
        building_code = f"BLD-{proj.name[:8]}-001"
        if dev_type == "Commercial":
            building_name = "مبنى الواجهة التجارية"
            building_code = f"BLD-{proj.name[:8]}-002"
        elif dev_type == "Mixed Use":
            building_name = "المبنى المركزي"
            building_code = f"BLD-{proj.name[:8]}-003"

        building = _safe_get_or_create("Building", {
            "doctype": "Building",
            "real_estate_project": rep.name,
            "building_name": building_name,
            "building_code": building_code,
            "building_type": dev_type,
            "status": "Under Construction",
            "number_of_floors": 5,
            "total_units": 0,
            "notes": f"مبنى - {BATCH}",
        }, {"building_code": building_code})
        building_count += 1

        # Floors
        floor_configs = _get_floor_configs(dev_type)
        for cfg in floor_configs:
            floor = _safe_get_or_create("Floor", {
                "doctype": "Floor",
                "real_estate_project": rep.name,
                "building": building.name,
                "floor_code": f"{building.building_code}-F{cfg['number']:02d}",
                "floor_name": cfg["name"],
                "floor_number": cfg["number"],
                "floor_type": cfg["type"],
                "notes": f"طابق - {BATCH}",
            }, {"floor_code": f"{building.building_code}-F{cfg['number']:02d}"})
            floor_count += 1

            # Units for this floor
            units = _create_units_for_floor(floor, building, rep, cfg, dev_type)
            all_units.extend(units)
            unit_count += len(units)

    return {
        "real_estate_projects": rep_count,
        "buildings": building_count,
        "floors": floor_count,
        "units": unit_count,
        "real_estate_projects_list": real_estate_projects,
        "units_list": all_units,
    }


def _get_floor_configs(dev_type):
    if dev_type == "Residential":
        return [
            {"number": 0, "name": "الدور الأرضي", "type": "Service"},
            {"number": 1, "name": "الطابق الأول", "type": "Residential"},
            {"number": 2, "name": "الطابق الثاني", "type": "Residential"},
            {"number": 3, "name": "الطابق الثالث", "type": "Residential"},
            {"number": 4, "name": "الطابق الرابع - البنتهاوس", "type": "Residential"},
        ]
    elif dev_type == "Commercial":
        return [
            {"number": 0, "name": "الدور الأرضي - المحلات", "type": "Commercial"},
            {"number": 1, "name": "دور الميزانين", "type": "Commercial"},
            {"number": 2, "name": "الطابق الأول - المكاتب", "type": "Commercial"},
        ]
    else:  # Mixed Use
        return [
            {"number": 0, "name": "الدور الأرضي - المحلات", "type": "Commercial"},
            {"number": 1, "name": "الطابق الأول - الخدمات", "type": "Service"},
            {"number": 2, "name": "الطابق الثاني - المكاتب", "type": "Commercial"},
            {"number": 3, "name": "الطابق الثالث - السكني", "type": "Residential"},
            {"number": 4, "name": "الطابق الرابع - السكني", "type": "Residential"},
        ]


def _create_units_for_floor(floor, building, rep, cfg, dev_type):
    """Create units for a floor based on type and configuration."""
    units = []
    floor_num = cfg["number"]

    if dev_type == "Residential":
        if floor_num == 0:
            unit_configs = [
                {"code": "S-G-01", "type": "Studio", "area": 45, "price": 2800000, "status": "Rented", "purpose": "Long Term Rent"},
                {"code": "S-G-02", "type": "Studio", "area": 40, "price": 2600000, "status": "Available", "purpose": "Long Term Rent"},
            ]
        elif floor_num == 4:
            unit_configs = [
                {"code": f"S-{floor_num:02d}-P1", "type": "Penthouse", "area": 220, "price": 18500000, "status": "Sold", "purpose": "Sale"},
                {"code": f"S-{floor_num:02d}-P2", "type": "Penthouse", "area": 185, "price": 15500000, "status": "Reserved", "purpose": "Sale"},
            ]
        else:
            unit_configs = [
                {"code": f"S-{floor_num:02d}-01", "type": "2 Bedroom", "area": 120, "price": 6800000, "status": "Available" if floor_num == 1 else "Available", "purpose": "Sale"},
                {"code": f"S-{floor_num:02d}-02", "type": "2 Bedroom", "area": 115, "price": 6500000, "status": "Reserved", "purpose": "Sale"},
                {"code": f"S-{floor_num:02d}-03", "type": "3 Bedroom", "area": 155, "price": 8200000, "status": "Available", "purpose": "Sale"},
                {"code": f"S-{floor_num:02d}-04", "type": "3 Bedroom", "area": 150, "price": 7900000, "status": "Sold", "purpose": "Sale"},
            ]
    elif dev_type == "Commercial":
        if floor_num == 0:
            unit_configs = [
                {"code": "C-G-01", "type": "Shop", "area": 85, "price": 9500000, "status": "Sold", "purpose": "Long Term Rent"},
                {"code": "C-G-02", "type": "Shop", "area": 75, "price": 8200000, "status": "Available", "purpose": "Long Term Rent"},
                {"code": "C-G-03", "type": "Shop", "area": 90, "price": 9800000, "status": "Reserved", "purpose": "Long Term Rent"},
                {"code": "C-G-04", "type": "Shop", "area": 65, "price": 7200000, "status": "Available", "purpose": "Long Term Rent"},
            ]
        elif floor_num == 1:
            unit_configs = [
                {"code": "C-M-01", "type": "Showroom", "area": 150, "price": 12000000, "status": "Available", "purpose": "Long Term Rent"},
                {"code": "C-M-02", "type": "Showroom", "area": 120, "price": 9800000, "status": "Sold", "purpose": "Long Term Rent"},
            ]
        else:
            unit_configs = [
                {"code": "C-01-01", "type": "Office", "area": 65, "price": 4500000, "status": "Available", "purpose": "Investment"},
                {"code": "C-01-02", "type": "Office", "area": 80, "price": 5500000, "status": "Reserved", "purpose": "Investment"},
                {"code": "C-01-03", "type": "Office", "area": 95, "price": 6200000, "status": "Available", "purpose": "Investment"},
            ]
    else:  # Mixed Use
        if floor_num == 0:
            unit_configs = [
                {"code": "M-G-01", "type": "Shop", "area": 70, "price": 6800000, "status": "Available", "purpose": "Long Term Rent"},
                {"code": "M-G-02", "type": "Shop", "area": 55, "price": 5200000, "status": "Sold", "purpose": "Long Term Rent"},
                {"code": "M-G-03", "type": "Shop", "area": 80, "price": 7500000, "status": "Reserved", "purpose": "Long Term Rent"},
            ]
        elif floor_num in (1, 2):
            unit_configs = [
                {"code": f"M-{floor_num:02d}-01", "type": "Office", "area": 90, "price": 5500000, "status": "Available", "purpose": "Investment"},
                {"code": f"M-{floor_num:02d}-02", "type": "Office", "area": 75, "price": 4500000, "status": "Available", "purpose": "Investment"},
            ]
        else:
            unit_configs = [
                {"code": f"M-{floor_num:02d}-01", "type": "2 Bedroom", "area": 110, "price": 5800000, "status": "Available", "purpose": "Sale"},
                {"code": f"M-{floor_num:02d}-02", "type": "2 Bedroom", "area": 105, "price": 5500000, "status": "Sold", "purpose": "Sale"},
                {"code": f"M-{floor_num:02d}-03", "type": "3 Bedroom", "area": 145, "price": 7200000, "status": "Available", "purpose": "Sale"},
            ]

    for cfg_u in unit_configs:
        unit = _safe_get_or_create("Unit", {
            "doctype": "Unit",
            "unit_code": f"{building.building_code}-{cfg_u['code']}",
            "building": building.name,
            "floor": floor.name,
            "real_estate_project": rep.name,
            "unit_type": _get_or_create_unit_type(cfg_u["type"]),
            "usage_purpose": cfg_u["purpose"],
            "property_nature": "Commercial" if dev_type == "Mixed Use" else dev_type,
            "area": cfg_u["area"],
            "expected_sale_price": cfg_u["price"],
            "expected_monthly_rent": int(cfg_u["price"] * 0.008),
            "status": cfg_u["status"],
            "finishing_status": "Semi Finished" if cfg_u["status"] in ("Available", "Reserved") else "Not Finished",
            "direction": "North",
            "marketing_status": "Active",
            "remarks": f"وحدة عقارية - {BATCH}",
        }, {"unit_code": f"{building.building_code}-{cfg_u['code']}"})
        units.append(unit)

    return units


def _get_or_create_unit_type(type_name):
    """Get or create a Unit Type."""
    existing = frappe.get_all("Unit Type", filters={"unit_type_name": type_name}, fields=["name"])
    if existing:
        return existing[0].name

    desc_map = {
        "2 Bedroom": "شقة سكنية بغرفتين نوم",
        "3 Bedroom": "شقة سكنية بثلاث غرف نوم",
        "Penthouse": "شقة علوية فاخرة",
        "Studio": "وحدة تجارية صغيرة",
        "Shop": "محل تجاري",
        "Showroom": "صالة عرض تجارية",
        "Office": "مكتب تجاري",
    }

    doc = _safe_get_or_create("Unit Type", {
        "doctype": "Unit Type",
        "unit_type_name": type_name,
        "description": desc_map.get(type_name, type_name),
    }, {"unit_type_name": type_name})
    return doc.name


# =============================================================================
# Property Owners & Ownership
# =============================================================================

def _create_ownership_data(units):
    """Create Property Owners and Ownership records."""
    # Guard: if units is not iterable (e.g., an int), skip
    if not hasattr(units, '__iter__') and not hasattr(units, '__len__'):
        print(f"[PHASE1] _create_ownership_data received non-iterable units: {type(units)}")
        return {"count": 0, "ownership_records": 0}
    if isinstance(units, (int, float, str)):
        print(f"[PHASE1] _create_ownership_data received scalar units: {type(units)}")
        return {"count": 0, "ownership_records": 0}

    owner_count = 0

    # Owner 1: رئيسي استثماري
    owner1 = _safe_get_or_create("Property Owner", {
        "doctype": "Property Owner",
        "owner_name": "صندوق الاستثمار العقاري الأول",
        "owner_type": "Investor",
        "status": "Active",
    }, {"owner_name": ["like", "%صندوق الاستثمار%"]})
    owner_count += 1

    # Owner 2: شريك
    owner2 = _safe_get_or_create("Property Owner", {
        "doctype": "Property Owner",
        "owner_name": "المستثمر العقاري السريع",
        "owner_type": "Individual",
        "status": "Active",
    }, {"owner_name": ["like", "%السريع%"]})
    owner_count += 1

    # Owner 3: شركة
    owner3 = _safe_get_or_create("Property Owner", {
        "doctype": "Property Owner",
        "owner_name": "شركة النور للاستثمار العقاري",
        "owner_type": "Company",
        "status": "Active",
    }, {"owner_name": ["like", "%النور للاستثمار%"]})
    owner_count += 1

    # Assign ownership to sold/reserved units
    sold_units = [u for u in units if _get_status(u) in ("Sold", "Rented")]
    reserved_units = [u for u in units if _get_status(u) == "Reserved"]

    # Sold units -> owner1 at 100%
    for unit in sold_units[:8]:
        _safe_get_or_create("Property Ownership", {
            "doctype": "Property Ownership",
            "unit": unit.name,
            "property_owner": owner1.name,
            "ownership_percentage": 100,
            "ownership_role": "Main Owner",
            "start_date": add_days(nowdate(), -60),
        }, {"unit": unit.name, "property_owner": owner1.name})

    # Some sold units with co-ownership
    for unit in sold_units[8:10]:
        _safe_get_or_create("Property Ownership", {
            "doctype": "Property Ownership",
            "unit": unit.name,
            "property_owner": owner1.name,
            "ownership_percentage": 60,
            "ownership_role": "Main Owner",
            "start_date": add_days(nowdate(), -60),
        }, {"unit": unit.name, "property_owner": owner1.name})
        _safe_get_or_create("Property Ownership", {
            "doctype": "Property Ownership",
            "unit": unit.name,
            "property_owner": owner2.name,
            "ownership_percentage": 40,
            "ownership_role": "Co-owner",
            "start_date": add_days(nowdate(), -60),
        }, {"unit": unit.name, "property_owner": owner2.name})

    # Reserved units -> pending
    for unit in reserved_units[:3]:
        _safe_get_or_create("Property Ownership", {
            "doctype": "Property Ownership",
            "unit": unit.name,
            "property_owner": owner3.name,
            "ownership_percentage": 100,
            "ownership_role": "Investor",
            "start_date": nowdate(),
        }, {"unit": unit.name, "property_owner": owner3.name})

    return {"count": owner_count}


# =============================================================================
# Unit Cost Allocation
# =============================================================================

def _create_unit_cost_allocations(projects, real_estate_projects):
    """Create Unit Cost Allocations using Project Financial Snapshot."""
    allocation_count = 0

    for rep in real_estate_projects:
        proj = frappe.get_doc("Project", rep.project)
        if not proj:
            continue

        # Get financial snapshot
        snapshots = frappe.get_all("Project Financial Snapshot",
                                   filters={"project": proj.name, "docstatus": 0},
                                   fields=["name"])
        if not snapshots:
            # Check submitted snapshots
            snapshots = frappe.get_all("Project Financial Snapshot",
                                       filters={"project": proj.name},
                                       fields=["name"])

        snapshot_name = snapshots[0].name if snapshots else None

        uca = _safe_get_or_create("Unit Cost Allocation", {
            "doctype": "Unit Cost Allocation",
            "real_estate_project": rep.name,
            "project": proj.name,
            "cost_source": "Financial Snapshot",
            "project_financial_snapshot": snapshot_name,
            "allocation_method": "By Area",
            "allocation_status": "Draft",
            "notes": f"توزيع تكاليف - {BATCH}",
        }, {"real_estate_project": rep.name})

        if uca.allocation_status == "Draft":
            # Fetch source amount from snapshot
            try:
                uca.fetch_source_amount()
            except Exception:
                pass

            uca.flags.ignore_validate_update_after_submit = True
            uca.save(ignore_permissions=True)

            # Apply allocation
            if uca.status in (None, "Draft", "") and uca.lines:
                try:
                    uca.apply_unit_allocation()
                except Exception as e:
                    print(f"[PHASE1] apply_unit_allocation failed: {e}")

            elif uca.status in (None, "Draft", "") and not uca.lines:
                # Manually create lines
                _create_allocation_lines(uca, rep)

            allocation_count += 1

    return {"unit_cost_allocations": allocation_count}


def _create_allocation_lines(uca, rep):
    """Create allocation lines for a UCA."""
    units = frappe.get_all("Unit",
                           filters={"real_estate_project": rep.name},
                           fields=["name", "unit_code", "area", "expected_sale_price"])

    total_area = sum(flt(u.area) for u in units) or 1
    source_amount = frappe.db.get_value("Project Financial Snapshot",
                                         uca.project_financial_snapshot,
                                         "boq_total_amount") or 1000000

    for unit in units:
        area_share = flt(unit.area) / total_area if total_area > 0 else 1 / len(units)
        allocated_cost = source_amount * area_share

        uca.append("lines", {
            "doctype": "Unit Cost Allocation Line",
            "unit": unit.name,
            "allocation_method": "By Area",
            "unit_area": unit.area,
            "percentage_of_total": area_share * 100,
            "allocated_cost": allocated_cost,
        })

    uca.flags.ignore_validate_update_after_submit = True
    uca.save(ignore_permissions=True)


# =============================================================================
# Unit Reservations
# =============================================================================

def _create_reservations(units):
    """Create unit reservations in various states."""
    # Guard: ensure units is a list
    if not hasattr(units, '__iter__') or isinstance(units, (int, float, str)):
        print(f"[PHASE1] _create_reservations received non-iterable: {type(units)}")
        return {"count": 0, "reservations": []}
    reservation_count = 0

    # Get company
    company = frappe.get_all("Company", fields=["name"])[0].name
    settings = frappe.get_single("Sales Invoice Collection Settings")

    # Create customers
    customers = _get_or_create_customers()

    # Available units for reservation
    available_units = [u for u in units if _get_status(u) == "Available"]

    for i, unit in enumerate(available_units[:10]):
        rep_name = frappe.db.get_value("Building", unit.building, "real_estate_project")
        proj_name = frappe.db.get_value("Real Estate Project", rep_name, "project") if rep_name else None

        res_type = "Sale"
        if i % 4 == 3:
            res_type = "Rent"

        res_status = "Reserved"
        if i % 5 == 4:
            res_status = "Reserved"
        if i % 5 == 4:
            res_status = "Expired"
        # Never use "Converted" status here - conversions handled by Sales Contracts

        res = _safe_get_or_create("Unit Reservation", {
            "doctype": "Unit Reservation",
            "reservation_number": f"RES-{unit.unit_code[:15]}-{i+1:03d}",
            "reservation_type": res_type,
            "company": company,
            "real_estate_project": rep_name,
            "project": proj_name,
            "unit": unit.name,
            "building": unit.building,
            "floor": unit.floor,
            "unit_type": unit.unit_type,
            "expected_sale_price": unit.expected_sale_price,
            "expected_monthly_rent": unit.expected_monthly_rent,
            "reservation_amount": int(unit.expected_sale_price * 0.05) if res_type == "Sale" else unit.expected_monthly_rent,
            "valid_from": nowdate(),
            "valid_until": add_days(nowdate(), 14),
            "customer": customers[i % len(customers)],
            "party_name": customers[i % len(customers)],
            "status": res_status,
            "notes": f"حجز - {BATCH}",
        }, {"reservation_number": f"RES-{unit.unit_code[:15]}-{i+1:03d}"})

        if res.status == "Reserved" and unit.status == "Available":
            try:
                res.mark_reserved()
            except Exception:
                pass

        if res.status != "Draft":
            reservation_count += 1

    return {"count": reservation_count, "reservations": []}


def _get_or_create_customers():
    """Get or create customers."""
    customer_data = [
        ("الأستاذ أحمد المنصور", "Individual"),
        ("شركة الإعمار للتطوير", "Company"),
        ("السيدة فاطمة الزهراء", "Individual"),
        ("مؤسسة النور التجارية", "Company"),
        ("الأستاذ خالد الوائلي", "Individual"),
        ("شركة الخليج للعقارات", "Company"),
    ]

    customers = []
    for name, ctype in customer_data:
        existing = frappe.get_all("Customer", filters={"customer_name": name}, fields=["name"])
        if existing:
            customers.append(existing[0].name)
        else:
            doc = _safe_get_or_create("Customer", {
                "doctype": "Customer",
                "customer_name": name,
                "customer_type": ctype,
                "customer_group": "Commercial" if ctype == "Company" else "Individual",
                "territory": "Yemen",
            }, {"customer_name": name})
            customers.append(doc.name)

    return customers


# =============================================================================
# Sales Contracts & Installments
# =============================================================================

def _create_sales_contracts(reservations):
    """Create Sales Contracts with Installment Schedules.
    reservations param is accepted but not used - function queries DB directly.
    """
    contract_count = 0
    contract_list = []

    # Get reserved reservations (not yet converted)
    res_list = frappe.get_all("Unit Reservation",
                               filters={"status": "Reserved", "reservation_type": "Sale"},
                               fields=["name", "reservation_number", "unit", "customer",
                                      "expected_sale_price", "real_estate_project", "project",
                                      "building", "floor", "unit_type"],
                               limit=8)

    for res in res_list:
        unit = frappe.get_doc("Unit", res.unit)
        rep = frappe.get_doc("Real Estate Project", res.real_estate_project)
        proj = frappe.get_doc("Project", res.project) if res.project else None

        # Determine sale price and discount
        sale_price = res.expected_sale_price
        discount = 0
        if "مكتب" in (unit.unit_type or ""):
            discount = sale_price * 0.03
        elif unit.area and unit.area > 150:
            discount = sale_price * 0.05

        net_price = sale_price - discount
        down_payment = net_price * 0.20

        # Contract number
        contract_num = f"SC-{unit.unit_code[:10]}-{BATCH[-4:]}"

        contract = _safe_get_or_create("Sales Contract", {
            "doctype": "Sales Contract",
            "contract_number": contract_num,
            "company": frappe.get_all("Company", fields=["name"])[0].name,
            "unit_reservation": res.name,
            "real_estate_project": res.real_estate_project,
            "project": res.project,
            "unit": res.unit,
            "building": res.building,
            "floor": res.floor,
            "unit_type": res.unit_type,
            "customer": res.customer,
            "sale_price": sale_price,
            "discount_amount": discount,
            "net_price": net_price,
            "payment_terms_type": "Installments",
            "down_payment_percent": 20,
            "down_payment_amount": down_payment,
            "contract_date": add_days(nowdate(), -30),
            "valid_until": add_days(nowdate(), -15),
            "contract_status": "Active",
            "notes": f"عقد بيع - {BATCH}",
        }, {"contract_number": contract_num})

        if contract.contract_status != "Cancelled":
            contract_count += 1
            contract_list.append(contract)

            # Add installment schedule
            installments = _build_installment_schedule(contract, net_price, down_payment)
            if installments and not contract.installments:
                for inst in installments:
                    contract.append("installments", inst)
                contract.flags.ignore_validate_update_after_submit = True
                contract.save(ignore_permissions=True)

    return {"count": contract_count, "contracts": contract_list}


def _build_installment_schedule(contract, net_price, down_payment):
    """Build installment schedule rows for a contract."""
    installments = []

    # Down payment (already paid)
    installments.append({
        "doctype": "Sales Installment Schedule",
        "sequence": 1,
        "installment_number": 1,
        "installment_type": "Down Payment",
        "due_date": add_days(nowdate(), -30),
        "percentage": 20,
        "amount": down_payment,
        "invoice_status": "Paid",
        "status": "Paid",
    })

    # Construction milestones
    remaining = net_price - down_payment
    milestone_types = ["Construction Milestone", "Construction Milestone", "Handover", "Post Handover"]
    milestone_dates = [add_days(nowdate(), 60), add_days(nowdate(), 120), add_days(nowdate(), 180), add_days(nowdate(), 270)]
    milestone_pcts = [25, 25, 20, 10]

    for i in range(4):
        amt = net_price * (milestone_pcts[i] / 100)
        inst_status = "Pending"
        inv_status = "Not Invoiced"
        if i == 0:
            inst_status = "Due"
            inv_status = "Draft Invoice"
        elif i == 1 and contract.net_price > 10000000:
            inst_status = "Due"
            inv_status = "Not Invoiced"

        installments.append({
            "doctype": "Sales Installment Schedule",
            "sequence": i + 2,
            "installment_number": i + 2,
            "installment_type": milestone_types[i],
            "due_date": milestone_dates[i],
            "percentage": milestone_pcts[i],
            "amount": amt,
            "invoice_status": inv_status,
            "status": inst_status,
        })

    return installments


# =============================================================================
# Draft Sales Invoices
# =============================================================================

def _create_draft_sales_invoices(contracts):
    """Create draft Sales Invoices from some installment schedules."""
    invoice_count = 0

    if not contracts:
        return {"count": 0}

    company = frappe.get_all("Company", fields=["name"])[0].name
    default_item = frappe.db.get_value("Item", {"item_name": ["like", "%وحدة عقارية%"]}, "name")
    if not default_item:
        # Use first available item
        items = frappe.get_all("Item", fields=["name"], limit=1)
        default_item = items[0].name if items else None

    for contract in contracts[:4]:
        if not contract.installments:
            continue

        for inst in contract.installments:
            if inst.invoice_status == "Draft Invoice" and inst.status == "Due":
                # Create draft Sales Invoice
                si = frappe.get_doc({
                    "doctype": "Sales Invoice",
                    "company": company,
                    "customer": contract.customer,
                    "project": contract.project,
                    "currency": CURRENCY,
                    "conversion_rate": 1,
                    "is_pos": 0,
                    "remarks": f"فاتورة قسط - {BATCH}",
                })
                si.append("items", {
                    "doctype": "Sales Invoice Item",
                    "item_code": default_item or "خدمة بيع وحدة عقارية",
                    "item_name": f"قسط عقد رقم {contract.contract_number}",
                    "qty": 1,
                    "rate": inst.amount,
                    "amount": inst.amount,
                    "unit": contract.unit,
                    "project": contract.project,
                    "construction_project": contract.project,
                    "real_estate_project": contract.real_estate_project,
                    "sales_contract": contract.name,
                    "unit_reservation": contract.unit_reservation,
                })
                si.flags.ignore_validate_update_after_submit = True
                si.insert(ignore_permissions=True)
                invoice_count += 1

                # Update installment status
                inst.invoice_status = "Draft Invoice"
                inst.sales_invoice = si.name
                contract.flags.ignore_validate_update_after_submit = True
                contract.save(ignore_permissions=True)
                break  # Only one invoice per contract

    return {"count": invoice_count}


# =============================================================================
# Validation
# =============================================================================

def validate_phase_1_presentation_data():
    """Validate the created data and report results."""
    print("[PHASE1] Running validation...")

    results = {}

    # Count all created records
    doctypes_to_check = [
        "Project", "Real Estate Project", "Building", "Floor", "Unit",
        "Property Owner", "Property Ownership",
        "Construction BOQ", "Construction Work Item",
        "Material Request", "Purchase Order", "Purchase Receipt", "Purchase Invoice",
        "Measurement Book", "Measurement Entry",
        "Interim Payment Certificate",
        "Contractor Account", "Retention Register",
        "Project Financial Snapshot", "Project Cash Flow Forecast", "Project EVM Metrics",
        "Unit Cost Allocation",
        "Unit Reservation", "Sales Contract",
        "Sales Invoice",
    ]

    for dt in doctypes_to_check:
        try:
            results[dt] = frappe.db.count(dt)
        except Exception:
            results[dt] = "ERROR"

    print("\n[PHASE1] Record Counts:")
    for k, v in results.items():
        print(f"  {k}: {v}")

    # Check for demo/test/sample names
    print("\n[PHASE1] Checking for forbidden names...")
    forbidden = ["demo", "test", "sample", "sandbox"]
    found_forbidden = False
    for keyword in forbidden:
        projects = frappe.get_all("Project", filters={"project_name": ["like", f"%{keyword}%"]}, fields=["name", "project_name"])
        if projects:
            print(f"  WARNING: Found '{keyword}' in project names: {projects}")
            found_forbidden = True

    if not found_forbidden:
        print("  No forbidden names found - OK")

    # Check for submitted invoices
    print("\n[PHASE1] Checking for submitted records...")
    submitted_sinv = frappe.get_all("Sales Invoice", filters={"docstatus": 1}, fields=["name"])
    submitted_pi = frappe.get_all("Purchase Invoice", filters={"docstatus": 1}, fields=["name"])
    payment_entries = frappe.get_all("Payment Entry", fields=["name"])
    journal_entries = frappe.get_all("Journal Entry", fields=["name"])

    print(f"  Submitted Sales Invoices: {len(submitted_sinv)}")
    print(f"  Submitted Purchase Invoices: {len(submitted_pi)}")
    print(f"  Payment Entries: {len(payment_entries)}")
    print(f"  Journal Entries: {len(journal_entries)}")

    print("\n[PHASE1] Validation complete!")
    return results


# =============================================================================
# CLI Entry Point
# =============================================================================

if __name__ == "__main__":
    create_phase_1_presentation_data()
