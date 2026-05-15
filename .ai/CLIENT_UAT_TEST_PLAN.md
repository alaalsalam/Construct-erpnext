---
name: CLIENT_UAT_TEST_PLAN
description: Client UAT test plan with scenarios, acceptance criteria, and pass/fail fields
type: reference
---

# خطة اختبار قبول المستخدم (UAT)
# Client UAT Test Plan
**Project:** Real Estate Development ERP
**Date:** 2026-05-15
**Test Environment:** construction.yemenfrappe.com
**Test Data:** PROJ-0002 (مشروع برج الياسمين السكني)

---

## 1. معلومات الاختبار

### المستخدمون المشاركون في الاختبار

| الدور | الاسم المقترح | الوحدات النمطية المختبرة |
|---|---|---|
| مدير المشروعات (Projects Manager) | أحمد محمد | Construction BOQ, Work Items, Measurement, IPC, Contractor |
| مدير المبيعات (Sales Manager) | سارة علي | Real Estate Inventory, Unit Reservation, Sales Contract, CRM, Smart Matching |
| المدير المالي (CFO / Accounts Manager) | خالد عمر | CFO Analytics, Cash Flow, EVM, Reports |
| مدير المقاولات (Contractor Manager) | محمد حسن | Contractor Account, Retention, Advance, Guarantee |
| مدير النظام (System Manager) | - | Admin functions, permissions, audit trail |

---

## 2. سيناريوهات الاختبار

### المجموعة أ: التخطيط الإنشائي والمقاولون

#### UAT-A1: عرض BOQ وتتبع التنفيذ

**الهدف:** التأكد من أن BOQ يعرض خط الأساس المالي correctement

**الخطوات:**
1. تسجيل الدخول كمستخدم Projects Manager
2. الانتقال إلى Construction BOQ
3. فتح BOQ-PROJ-0002-001
4. مراجعة الأعمدة: total_amount, work_items_generated, variance_amount
5. فتح تقرير BOQ Variance Analysis
6. فتح تقرير BOQ Cost Analysis

**نتيجة متوقعة:**
- BOQ يعرض إجمالي التكلفة
- 72 عنصر عمل مربوط
- أعمدة التنفيذ تظهر البيانات

**حقل Pass/Fail:**
- `variance_amount` صحيح؟ (نعم/لا)
- عدد `work_items_generated` = 72؟ (نعم/لا)

**ملاحظات:**
- يتم الحفظ في شاشة BOQ
- أي انحراف عن المخطط يجب توثيقه

---

#### UAT-A2: عرض عناصر العمل وتتبع Pipeline

**الهدف:** التأكد من أن Work Items تربط التخطيط بالعمليات

**الخطوات:**
1. الانتقال إلى Construction Work Item
2. تصفية: project = PROJ-0002
3. مراجعة الأعمدة: planned_quantity, requested_qty, ordered_qty, received_qty, invoiced_qty, consumed_qty, measured_qty, certified_qty
4. فتح تقرير Work Item Procurement Summary
5. فتح تقرير BOQ Procurement Pipeline

**نتيجة متوقعة:**
- 72 عنصر ظاهر
- أعمدة Pipeline تظهر الكميات الفعلية
- الاختلاف بين المخطط والفعلي ظاهر

**حقل Pass/Fail:**
- عدد العناصر = 72؟ (نعم/لا)
- تقرير Procurement Summary يعمل؟ (نعم/لا)

---

#### UAT-A3: عرض حسابات المقاولين

**الهدف:** التأكد من أن نظام المقاولين المالي يعمل بشكل صحيح

**الخطوات:**
1. الانتقال إلى Contractor Management > Contractor Account
2. تصفية: project = PROJ-0002
3. مراجعة حساب مقاول واحد
4. فتح تقرير Contractor Account Statement
5. فتح تقرير Contractor Exposure Summary
6. فتح تقرير Retention Register Report

**نتيجة متوقعة:**
- 12 حساب مقاول ظاهر
- المبالغ_certified و retained صحيحة
- كشف الحساب يعرض جميع القيود

**حقل Pass/Fail:**
- عدد حسابات المقاولين = 12؟ (نعم/لا)
- كشف الحساب يعرض بيانات؟ (نعم/لا)

---

#### UAT-A4: عرض Measurement Book و IPC

**الهدف:** التأكد من مسار القياس → الشهادة يعمل

**الخطوات:**
1. الانتقال إلى Measurement Book
2. تصفية: project = PROJ-0002
3. فتح كتاب قياس واحد (MB-2026-00001 أو أي كتاب verified)
4. مراجعة: total_accepted_qty, total_measured_amount
5. فتح IPC-2026-00002 (Paid) — تفصيلي
6. مراجعة الأعمدة: boq_qty, previous_certified_qty, current_certified_qty, total_certified_qty, remaining_qty, gross_amount, retention_amount, net_payable
7. فتح تقرير IPC Register

**نتيجة متوقعة:**
- Measurement Book يعرض القياسات
- IPC يربط بالـ Work Items صحيحة
- الـ Retention محسوب (10% default)
- التقرير يعرض 4 IPCs

**حقل Pass/Fail:**
- IPCs مرتبطة بـ Work Items صحيحة؟ (نعم/لا)
- تقرير IPC Register يعمل؟ (نعم/لا)

---

### المجموعة ب: المخزون العقاري والربحية

#### UAT-B1: عرض المشروع العقاري والهيكل

**الهدف:** التأكد من هيكل المخزون صحيح

**الخطوات:**
1. الانتقال إلى Real Estate Project
2. فتح REP-2026-00001 (مرتبط بـ PROJ-0002)
3. مراجعة: total_units, available_units, reserved_units, sold_units, blocked_units
4. فتح Building (BLD-PROJ-000-001)
5. فتح Floor
6. فتح Unit (عرض أول 10 وحدات)

**نتيجة متوقعة:**
- 24 وحدة ظاهرة
- التوزيع: Available / Reserved / Sold / Blocked
- كل وحدة لها نوع ومساحة وسعر

**حقل Pass/Fail:**
- عدد الوحدات = 24؟ (نعم/لا)
- الوحدات مرتبطة بالمبنى والطابق؟ (نعم/لا)

---

#### UAT-B2: عرض Unit Cost Allocation

**الهدف:** التأكد من حساب ربحية الوحدات يعمل

**الخطوات:**
1. الانتقال إلى Unit Cost Allocation
2.新建 > Unit Cost Allocation
3. اختيار: real_estate_project = REP-2026-00001
4. اختيار: cost_source = BOQ Total
5. اختيار: allocation_basis = By Area
6. Save and Calculate
7. مراجعة: source_amount, total_allocated_amount, lines
8. Apply
9. فتح تقرير Unit Profitability Report

**نتيجة متوقعة:**
- source_amount يساوي BOQ total
- كل وحدة لها allocated_cost
- expected_margin و profitability_status ظاهر

**حقل Pass/Fail:**
- source_amount صحيح؟ (نعم/لا)
- كل الوحدات لها allocated_cost؟ (نعم/لا)
- التقرير يعمل؟ (نعم/لا)

---

#### UAT-B3: عرض تتبع الأبعاد المحاسبية

**الهدف:** التأكد من الأبعاد تصل للـ GL

**الخطوات:**
1. الانتقال إلى GL Dimension Traceability
2. تصفية: project = PROJ-0002
3. مراجعة الأبعاد: project, unit, cost_code, wbs_element
4. فتح تقرير Unit Financial Ledger
5. فتح تقرير Work Item Financial Ledger

**نتيجة متوقعة:**
- الأبعاد مفعلة ومسماة
- البيانات تظهر بشكل صحيح

**حقل Pass/Fail:**
- الأبعاد تظهر في التقرير؟ (نعم/لا)
- Unit dimension ظاهر؟ (نعم/لا)

---

### المجموعة ج: المبيعات والإيجارات

#### UAT-C1: عرض الحجز وتحويله

**الهدف:** التأكد من دورة الحجز تعمل

**الخطوات:**
1. الانتقال إلى Unit Reservation
2. تصفية: project = PROJ-0002
3. مراجعة: 17 حجز (Converted + Reserved + Expired + Cancelled)
4. فتح حجز RES-PROJ-0002-004 (Reserved)
5. مراجعة: unit, reservation_type, status, customer

**نتيجة متوقعة:**
- 17 حجز ظاهر
- الحالة المحولة (Converted) مرتبطة بعقد بيع
- الوحدة المحجوزة (Reserved) تظهر Reserved status

**حقل Pass/Fail:**
- عدد الحجوزات = 17؟ (نعم/لا)
- الحجز المحول مرتبط بعقد؟ (نعم/لا)

---

#### UAT-C2: عرض عقود البيع والأقساط

**الهدف:** التأكد من عقود البيع تعمل

**الخطوات:**
1. الانتقال إلى Sales Contract
2. فتح SC-PROJ-0002-001 (Approved)
3. مراجعة: contract_number, customer, unit, sale_price, contract_status
4. مراجعة جدول الأقساط: Sales Installment Schedule
5. مراجعة: total_installment_amount, collection_status
6. فتح SC-PROJ-0002-002 و SC-PROJ-0002-003

**نتيجة متوقعة:**
- 3 عقود ظاهرة (جميعها Approved)
- بيانات الوحدة مأخوذة تلقائياً من الوحدة
- الأقساط محددة ومجدولة

**حقل Pass/Fail:**
- عدد العقود = 3؟ (نعم/لا)
- كل عقد له أقساط؟ (نعم/لا)
- الوحدة أصبحت Sold على العقد Approved؟ (نعم/لا)

---

#### UAT-C3: عرض عقد إيجار PROJ-0002 وجدول الإيجار

**الهدف:** التأكد من أن دورة الإيجار التشغيلية جاهزة للـ UAT داخل PROJ-0002.

**الخطوات:**
1. الانتقال إلى Lease Contract
2. فتح `LC-2026-00003`
3. مراجعة: unit, customer, lease_start_date, lease_end_date, monthly_rent, lease_status
4. مراجعة جدول Rent Schedule
5. فتح Active Leases Report مع فلتر `REP-2026-00002`
6. فتح Rent Schedule Report مع فلتر `LC-2026-00003`
7. فتح Rental Value Summary مع فلتر `REP-2026-00002`

**نتيجة متوقعة:**
- العقد Active
- الوحدة `BLD-PROJ-000-001-S-G-02` حالتها Rented
- الحجز `RES-2026-00006` حالته Converted
- Rent Schedule يحتوي 12 صفاً بإجمالي `948,000`
- لا توجد فاتورة إيجار أو Payment Entry لهذا العقد ضمن هذا الاختبار

**حقل Pass/Fail:**
- عقد الإيجار Active؟ (نعم/لا)
- جدول الإيجار 12 صفاً؟ (نعم/لا)
- الوحدة Rented؟ (نعم/لا)
- لم يتم إنشاء Rent Invoice أو Payment Entry؟ (نعم/لا)

---

### المجموعة د: CRM والمطابقة

#### UAT-D1: عرض متطلبات العملاء

**الهدف:** التأكد من خط أنابيب CRM يعمل

**الخطوات:**
1. الانتقال إلى Customer Requirement
2. مراجعة: 5 متطلبات (REQ-2026-00001 وما بعده)
3. مراجعة: requirement_type, preferred_project, budget_min, budget_max, status
4. فتح تقرير Customer Requirement Register

**نتيجة متوقعة:**
- 5 متطلبات ظاهرة
- مصنفة حسب النوع (Buy/Rent/Investment)

**حقل Pass/Fail:**
- عدد المتطلبات = 5؟ (نعم/لا)
- التقرير يعمل؟ (نعم/لا)

---

#### UAT-D2: عرض Smart Matching

**الهدف:** التأكد من محرك المطابقة يعمل

**الخطوات:**
1. الانتقال إلى Match Result
2. مراجعة:_match_result (إن وجد) مع scored items
3. فتح Matching Settings
4. مراجعة: weights (location, price, area, type, feature), minimum_score
5. فتح تقرير Recommended Units Report

**نتيجة متوقعة:**
- Matching Settings يعرض الأوزان
- minimum_score = 60
- التقرير يعمل

**حقل Pass/Fail:**
- إعدادات المطابقة موجودة؟ (نعم/لا)
- weights صحيحة؟ (نعم/لا)
- التقرير يعمل؟ (نعم/لا)

---

### المجموعة هـ: التقارير والإدارة التنفيذية

#### UAT-E1: عرض CFO Dashboard

**الهدف:** التأكد من لوحة CFO تعمل

**الخطوات:**
1. الانتقال إلى Executive Presentation Center
2. فتح CFO Project Control Summary
3. تصفية: project = PROJ-0002
4. مراجعة: budget, committed, invoiced, certified, variance

**نتيجة متوقعة:**
- الملخص يظهر بيانات PROJ-0002
- المخاطر والتنبيهات ظاهرة

**حقل Pass/Fail:**
- الملخص يعرض بيانات؟ (نعم/لا)
- تنبيهات المخاطر ظاهرة؟ (نعم/لا)

---

#### UAT-E2: عرض Cash Flow Forecast

**الهدف:** التأكد من توقع التدفق النقدي يعمل

**الخطوات:**
1. الانتقال إلى Executive Control Center
2. فتح Project Cash Flow Forecast
3.新建 > Cash Flow Forecast
4. اختيار: project = PROJ-0002
5. اختيار: period_type = Monthly
6. Generate
7. مراجعة: periods, inflows, outflows, running_balance, cash_risk_status

**نتيجة متوقعة:**
- الفترات تظهر (شهرية)
- inflows تظهر بيانات
- cash_risk_status محسوب

**حقل Pass/Fail:**
- forecast يعمل ويعرض بيانات؟ (نعم/لا)
- cash_risk_status ظاهر؟ (نعم/لا)

---

#### UAT-E3: عرض EVM Metrics

**الهدف:** التأكد من مؤشرات EVM تعمل

**الخطوات:**
1. الانتقال إلى Project EVM Metrics
2.新建 > EVM Metrics
3. اختيار: project = PROJ-0002
4. Calculate
5. مراجعة: BAC, EV, AC, CPI, SPI, EAC, overall_evm_status

**نتيجة متوقعة:**
- القيم محسوبة من Work Items
- CPI و SPI ظاهرين
- overall_evm_status: On Track / Watch / At Risk

**حقل Pass/Fail:**
- EVM metrics محسوبة؟ (نعم/لا)
- CPI و SPI ظاهرين؟ (نعم/لا)
- status صحيح؟ (نعم/لا)

---

#### UAT-E4: عرض Financial Snapshot

**الهدف:** التأكد من الملخص المالي يعمل

**الخطوات:**
1. الانتقال إلى Project Financial Snapshot
2.新建 > Financial Snapshot
3. اختيار: project = PROJ-0002
4. Generate
5. مراجعة: boq_total, committed, invoiced, certified, risk_status

**نتيجة متوقعة:**
- جميع القيم محسوبة
- risk_status ظاهر

**حقل Pass/Fail:**
- Snapshot يعمل؟ (نعم/لا)
- risk_status ظاهر؟ (نعم/لا)

---

### المجموعة و: الصيانة والوثائق

#### UAT-F1: عرض طلبات الصيانة

**الهدف:** التأكد من نظام الصيانة يعمل

**الخطوات:**
1. الانتقال إلى Property Maintenance Request
2. مراجعة: 4 طلبات (PMR-2026-00001 through PMR-2026-00004)
3. مراجعة: unit, issue_type, status, estimated_cost, actual_cost
4. فتح تقرير Open Maintenance Requests
5. فتح تقرير Maintenance Cost Summary

**نتيجة متوقعة:**
- 4 طلبات ظاهرة
- الأنواع: Electrical / Plumbing / AC / Civil
- التكلفة تتبع (إدارية فقط)

**حقل Pass/Fail:**
- عدد الطلبات = 4؟ (نعم/لا)
- التقرير يعمل؟ (نعم/لا)

---

#### UAT-F2: عرض الوثائق العقارية

**الهدف:** التأكد من نظام الوثائق يعمل

**الخطوات:**
1. الانتقال إلى Property Document
2. مراجعة: 3 وثائق (PDOC-2026-00001 through PDOC-2026-00003)
3. مراجعة: document_type, status, expiry_date
4. فتح تقرير Expiring Documents Report

**نتيجة متوقعة:**
- 3 وثائق ظاهرة
- الأنواع: Title Deed / Drawing / License

**حقل Pass/Fail:**
- عدد الوثائق = 3؟ (نعم/لا)
- التقرير يعمل؟ (نعم/لا)

---

## 3. معايير القبول (Acceptance Criteria)

### معايير النجاح العامة

| المعيار | الشرح |
|---|---|
| كل سيناريو يعمل كما هو متوقع | لا أخطاء غير متوقعة |
| التقارير تُظهر البيانات الصحيحة | الأرقام متوافقة مع المصدر |
| الأبعاد المحاسبية تصل للـ GL | Unit dimension ظاهر |
| Workflows متصلة بشكل صحيح | كل خطوة تغذي الخطوة التالية |
| الواجهة بالعربية واضحة |Labels مفهومة |

### معايير الفشل (Blockers)

| الخطأ | التأثير |
|---|---|
| شاشة لا تحمل البيانات | UAT محظور |
| تقرير يعطي خطأ | UAT محظور |
| تناقض بين الشاشة والتقرير | يحتاج تحقيق |
| Workflow لا ينتقل للخطوة التالية | يحتاج إصلاح |

---

## 4. ملخص Pass/Fail

| السيناريو | النتيجة | الملاحظات |
|---|---|---|
| UAT-A1: BOQ | Pass / Fail | |
| UAT-A2: Work Items | Pass / Fail | |
| UAT-A3: Contractor Accounts | Pass / Fail | |
| UAT-A4: Measurement + IPC | Pass / Fail | |
| UAT-B1: Real Estate Inventory | Pass / Fail | |
| UAT-B2: Unit Cost Allocation | Pass / Fail | |
| UAT-B3: GL Dimension Traceability | Pass / Fail | |
| UAT-C1: Unit Reservation | Pass / Fail | |
| UAT-C2: Sales Contract | Pass / Fail | |
| UAT-C3: Lease Contract + Rent Schedule | Pass / Fail | LC-2026-00003 |
| UAT-D1: Customer Requirement | Pass / Fail | |
| UAT-D2: Smart Matching | Pass / Fail | |
| UAT-E1: CFO Dashboard | Pass / Fail | |
| UAT-E2: Cash Flow Forecast | Pass / Fail | |
| UAT-E3: EVM Metrics | Pass / Fail | |
| UAT-E4: Financial Snapshot | Pass / Fail | |
| UAT-F1: Maintenance | Pass / Fail | |
| UAT-F2: Property Documents | Pass / Fail | |

**نسبة النجاح المستهدفة:** 100% على السيناريوهات الحرجة (A1, A4, B1, B2, C2, E1)

---

## 5. المسؤوليات

| المهمة | المسؤول |
|---|---|
| تنفيذ الاختبارات | المستخدم المعني (Projects Manager / Sales Manager / CFO) |
| التوثيق | مدير النظام |
| إصلاح المشاكل الحرجة | فريق التطوير |
| الموافقة النهائية | العميل |
