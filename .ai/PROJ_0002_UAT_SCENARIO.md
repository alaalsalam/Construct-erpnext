---
name: PROJ_0002_UAT_SCENARIO
description: Step-by-step UAT scenario using PROJ-0002 project data
type: reference
---

# دليل سيناريو اختبار قبول المستخدم — PROJ-0002
# PROJ-0002 UAT Scenario Guide
**Project:** مشروع برج الياسمين السكني (PROJ-0002)
**Purpose:** Demonstrate end-to-end system capabilities to client
**Duration:** ~90 minutes presentation

---

## الهدف من السيناريو

استخدام بيانات مشروع برج الياسمين (PROJ-0002) لإظهار قدرة النظام الكاملة من التخطيط الإنشائي إلى المبيعات والإيجارات. الهدف هو أن يفهم العميل:
1. كيف يعمل النظام بشكل متكامل
2. كيف تتصل الوحدات النمطية ببعضها
3. ما هي التقارير المتاحة
4. ما هو جاهز وما هو مؤجل

---

## المتطلبات الأساسية

- تسجيل الدخول كمستخدم System Manager أو Projects Manager
- الموقع: construction.yemenfrappe.com
- اللغة: العربية (RTL)
- المشروع: PROJ-0002 (مشروع برج الياسمين السكني)

---

## الجزء الأول: التخطيط الإنشائي والمقاولين (25 دقيقة)

### الخطوة 1.1: عرض المشروع والقاعدة المالية

**الهدف:** إظهار خط الأساس المالي للمشروع

**المسار:**
```
Project > PROJ-0002 (مشروع برج الياسمين السكني)
```

**ما يجب إظهاره:**
- اسم المشروع والحالة (Open)
- النسبة المكتملة (percent_complete)
- تاريخ البدء والانتهاء

**النتيجة المتوقعة:**
- المشروع يحمل اسم "مشروع برج الياسمين السكني"
- الحالة "Open"

---

### الخطوة 1.2: عرض BOQ وتتبع التنفيذ

**الهدف:** إظهار إدارة بنود الكميات وتتبع التنفيذ

**المسار:**
```
Construction Control Workspace > Construction BOQ
→ BOQ-PROJ-0002-001
```

**ما يجب إظهاره:**
- نوع BOQ (Original / Amendment)
- إجمالي المبالغ (total_amount)
- عدد بنود عناصر العمل (work_items_generated)
- أعمدة التنفيذ: requested / ordered / received / invoiced / consumed / measured / certified
- الفرق بين المخطط والفعلي (variance)

**التقارير المرتبطة:**
```
Reports & Analytics > BOQ Variance Analysis
→ BOQ-PROJ-0002-001
```

```
Reports & Analytics > BOQ Cost Analysis
→ BOQ-PROJ-0002-001
```

**ما يُثبته للعميل:**
- خط الأساس واضح
- التنفيذ مرئي لحظة بلحظة
- الفرق بين المخطط والفعلي واضح

---

### الخطوة 1.3: عرض عناصر العمل (Work Items)

**الهدف:** إظهار الرابط المركزي بين التخطيط والعمليات

**المسار:**
```
Construction Control > Construction Work Item
→ عرض قائمة العناصر
→ Filter by: project = PROJ-0002
```

**ما يجب إظهاره:**
- 72 عنصر عمل موزعة على أكواد التكلفة المختلفة
- أعمدة التتبع: procurement_status, measurement_status, certification_status
- أعمدة الكميات: planned / requested / ordered / received / invoiced / consumed / measured / certified
- أعمدة المالية: planned_amount / actual_cost / variance_amount

**ما يُثبته للعميل:**
- كل بند BOQ أصبح عنصر عمل قابل للتتبع
- كميات المواد تتبع من BOQ إلى الشراء إلى الاستهلاك إلى القياس إلى الشهادة

---

### الخطوة 1.4: عرض اتفاقيات المقاولين وحساباتهم

**الهدف:** إظهار النظام المالي الفرعي للمقاولين

**المسار:**
```
Contractor Management Workspace > Contractor Account
→ Filter by: project = PROJ-0002
```

**ما يجب إظهاره:**
- 12 حساب مقاول (لكل مقاول/مشروع)
- المبالغ: total_certified_amount, total_retention_held, total_advance_paid, outstanding_balance

**التقارير المرتبطة:**
```
Contractor Management > Contractor Account Statement
→ Contractor Account name
→ Show ledger entries
```

```
Contractor Management > Contractor Exposure Summary
→ project = PROJ-0002
```

```
Contractor Management > Retention Register Report
→ project = PROJ-0002
```

```
Contractor Management > Guarantee Register Report
→ project = PROJ-0002
```

**ما يُثبته للعميل:**
- كل مقاول له حساب مالي مستقل
- الـ Retention محتجز ومتتبع
- السلف مصروفة ومستردة
- الضمانات مراقبة بآلياتها

---

### الخطوة 1.5: عرض دفتر القياسات وIPC

**الهدف:** إظهار مسار القياس إلى الشهادة

**المسار:**
```
Measurement & IPC Workspace > Measurement Book
→ Filter by: project = PROJ-0002
→ Book: MB-2026-00001 (or any verified book)
```

**ما يجب إظهاره:**
- 5 كتب قياس
- الحالات: Draft / Submitted / Verified / Locked
- Measurement Entry (20 إدخال)
- مجموع الكميات المقاسة

**المسار للـ IPC:**
```
Measurement & IPC Workspace > Interim Payment Certificate
→ Filter by: project = PROJ-0002
→ IPC-2026-00002 (Paid)
→ IPC-2026-00003 (Partially Paid)
→ IPC-2026-00004 (Invoice Created)
→ IPC-2026-00005 (Invoice Created)
```

**ما يجب إظهاره في IPC:**
- gross_amount, current_certified_amount, total_certified_amount
- retention_amount, deductions, net_payable
- الأعمدة: boq_qty / previous_certified_qty / current_certified_qty / total_certified_qty / remaining_qty

**التقارير:**
```
Measurement & IPC > IPC Register
→ project = PROJ-0002
```

```
Measurement & IPC > IPC Line Details
→ project = PROJ-0002
```

```
Measurement & IPC > Measurement to IPC Traceability
```

**ما يُثبته للعميل:**
- مسار كامل من القياس في الموقع إلى الشهادة المالية
- كل IPC مرتبط بـ Work Item و Measurement Entry
- الـ Retention محسوب تلقائياً

---

## الجزء الثاني: المخزون العقاري والربحية (20 دقيقة)

### الخطوة 2.1: عرض المشروع العقاري والعقارات

**الهدف:** إظهار الهيكل الهرمي للمخزون

**المسار:**
```
Real Estate Inventory Workspace > Real Estate Project
→ REP-2026-00001 (linked to PROJ-0002)
```

**ما يجب إظهاره:**
- إجمالي الوحدات: 24 وحدة
- التوزيع: Available / Reserved / Sold / Blocked
- النوع: 2 Bedroom / 3 Bedroom / Penthouse / Studio / Storage

**المسار لعرض المبنى والأدوار:**
```
Real Estate Inventory Workspace > Building
→ BLD-PROJ-000-001 (البرج A)
```

```
Real Estate Inventory Workspace > Floor
→ الطوابق الستة + الطوابق السفلية
```

```
Real Estate Inventory Workspace > Unit
→ عرض قائمة الوحدات (24 سجل)
→ Filter by: status
```

**ما يجب إظهاره للوحدات:**
- رقم الوحدة واسمها
- النوع والمساحة
- الحالة (Available/Reserved/Sold/Blocked)
- السعر المتوقع (expected_sale_price)
- الإيجار المتوقع (expected_monthly_rent)

**ما يُثبته للعميل:**
- هيكل واضح من المشروع إلى المبنى إلى الطابق إلى الوحدة
- كل وحدة لها حالة واضحة
- المخزون مرئي في لمحة

---

### الخطوة 2.2: عرض الملكية والتخصيص

**الهدف:** إظهار نظام الملكية وتخصيص التكلفة

**المسار:**
```
Real Estate Inventory Workspace > Property Owner
→ عرض المالكين
```

```
Real Estate Inventory Workspace > Property Ownership
→ عرض سجلات الملكية
```

**ما يجب إظهاره:**
- المالك ونوعه (Individual / Company)
- نسبة الملكية (ownership_percentage)
- حالة الملكية (Active / Transferred)

---

### الخطوة 2.3: تشغيل Unit Cost Allocation

**الهدف:** إظهار حساب ربحية الوحدات

**المسار:**
```
Real Estate Inventory Workspace > Unit Cost Allocation
→新建→ Unit Cost Allocation
→ real_estate_project = REP-2026-00001
→ cost_source = BOQ Total (or Certified Cost)
→ allocation_basis = By Area
→ Save & Calculate
→ Apply
```

**ما يجب إظهاره:**
- source_amount (مبلغ التكلفة)
- total_allocated_amount (المبلغ الموزع)
- Lines (allocation per unit)
- allocated_cost per unit
- expected_margin and profitability_status per unit

**التقارير:**
```
Real Estate Inventory > Unit Profitability Report
```

```
Real Estate Inventory > Building Profitability Summary
```

```
Reports & Analytics > Real Estate Project Profitability Summary
```

**ما يُثبته للعميل:**
- تكلفة المشروع موزعة على الوحدات
- هامش ربح كل وحدة واضح
- الوحدات المربحة والغير مربحة ظاهرة

---

### الخطوة 2.4: عرض تتبع الأبعاد المحاسبية

**الهدف:** إظهار مسار الأبعاد من الوحدة إلى GL

**المسار:**
```
Executive Control Center > GL Dimension Traceability
→ project = PROJ-0002
```

**ما يجب إظهاره:**
- كيف يصل البُعد (project + unit) إلى GL entries
- الأبعاد المفعلة (project، cost_code، wbs_element، unit)

**التقارير:**
```
Reports & Analytics > Unit Financial Ledger
→ unit = BLD-PROJ-000-001-S-01-03 (sold unit)
```

**ما يُثبته للعميل:**
- كل تكلفة مرتبطة بوحدة محددة
- مسار التدقيق واضح

---

## الجزء الثالث: المبيعات والإيجارات (20 دقيقة)

### الخطوة 3.1: عرض الحجز والعقد

**الهدف:** إظهار دورة البيع من الحجز إلى العقد

**المسار:**
```
Real Estate Inventory > Unit Reservation
→ Filter by: project = PROJ-0002
→ RES-PROJ-0002-001 (Converted)
→ RES-PROJ-0002-004 (Reserved)
```

**ما يجب إظهاره:**
- أنواع الحجز: Sale / Rent
- الحالات: Draft / Reserved / Converted / Expired / Cancelled
- معلومات العميل والوحدة

**المسار لعقد البيع:**
```
Sales & Rental Workspace > Sales Contract
→ SC-PROJ-0002-001 (شركة الإعمار للتطوير — Approved)
→ SC-PROJ-0002-002 (السيدة فاطمة الزهراء — Approved)
→ SC-PROJ-0002-003 (مؤسسة النور التجارية — Approved)
```

**ما يجب إظهاره في العقد:**
- معلومات العقد (رقم، تاريخ، حالة)
- بيانات الوحدة (مأخوذة تلقائياً من الوحدة)
- بيانات المشتري
- السعر وأقساط الدفع
- جدول الأقساط (Sales Installment Schedule)
- amount collected vs outstanding

**ما يجب إظهاره للعميل:**
- الحجز تحول إلى عقد
- الوحدة أصبحت Sold عند إرسال العقد
- الأقساط محددة ومجدولة
- التحصيل متتبع

---

### الخطوة 3.2: عرض الأقساط والتقارير

**الهدف:** إظهار تتبع الأقساط وإدارة التحصيل

**المسار:**
```
Sales & Rental > Sales Contract
→ SC-PROJ-0002-001
→ الأقساط (Sales Installment Schedule child table)
```

**ما يجب إظهاره:**
- القسط (installment_number)
- النوع (Booking / Down Payment / Construction Milestone / Handover)
- المبلغ (amount)
- الحالة (Pending / Due / Partial / Paid / Overdue)
- حالة الفاتورة (invoice_status)
- المبلغ المدفوع والمتبقي

**التقارير:**
```
Reports & Analytics > Sales Collection Status
→ project = PROJ-0002
```

```
Sales & Rental > Buyer Statement (if report exists)
```

**ما يُثبته للعميل:**
- كل قسط مرتبط بالعميل والوحدة
- حالة التحصيل واضحة
- التقارير تساعد في متابعة التحصيل

---

### الخطوة 3.3: عرض عقد الإيجار (عرض توضيحي)

**الهدف:** إظهار قدرة النظام على إدارة الإيجارات (حتى لو لا يوجد عقد منشأ)

**التوضيح للعميل:**
> "في PROJ-0002 لا يوجد عقد إيجار منشأ حالياً. النظام جاهز بالكامل. سأعرض لك الإعدادات."

**المسار:**
```
Sales & Rental Workspace > Lease Contract Settings
→ عرض الإعدادات
```

```
Sales & Rental Workspace > Rent Invoice Collection Settings
→ عرض الإعدادات
```

**ما يجب إظهاره:**
- إعدادات Billing Frequency (Monthly / Quarterly / Semi Annual / Annual)
- إعدادات الأمان (عدم التكرار، إلزامية المستأجر)
- آلية التحويل من الحجز إلى العقد

**ما يُثبته للعميل:**
- النظام جاهز لعقود الإيجار
- Rent Schedule يُولد تلقائياً
- المستأجر مخزن على العقد (وليس على الوحدة)

---

## الجزء الرابع: CRM والمطابقة (15 دقيقة)

### الخطوة 4.1: عرض متطلبات العملاء

**الهدف:** إظهار خط أنابيب المبيعات العقاري

**المسار:**
```
Reports & Analytics > Customer Requirement Register
→ 5 متطلبات عملاء
```

**ما يجب إظهاره:**
- نوع المتطلب (Buy / Rent / Investment)
- المشروع المفضل والوحدة
- الميزانية (budget_min / budget_max)
- المساحة المطلوبة
- الحالة (New / Qualified / Matched / Reserved / Won / Lost / Backlog)

**ما يُثبته للعميل:**
- كل عميل محتمل له سجل
- المتطلبات مصنفة ومقيمة

---

### الخطوة 4.2: عرض المعاينات والمتابعات

**الهدف:** إظهار تتبع الأنشطة البيعية

**المسار:**
```
Reports & Analytics > Viewing Schedule Report
```

```
Reports & Analytics > Follow Up Report
```

**ما يجب إظهاره:**
- جدول المعاينات القادمة
- نتائج المتابعات
- القنوات (Call / Email / Visit / Message)

---

### الخطوة 4.3: عرض Smart Matching

**الهدف:** إظهار محرك المطابقة الذكية

**المسار:**
```
Reports & Analytics > Recommended Units Report
→ requirement = REQ-2026-00001 (or any matched requirement)
```

**ما يجب إظهاره:**
- Match Result مع scored items
- الوحدات المتاحة مرتبة حسب الدرجة
- الـ score محسوب على 5 أبعاد:
  - location (project match)
  - price (budget match)
  - area (size match)
  - type (unit type match)
  - features (required features)

**إعدادات المطابقة:**
```
Reports & Analytics > Matching Settings
→ عرض الأوزان (location=10, price=35, area=25, type=20, feature=10)
→ minimum_score = 60
```

**ما يُثبته للعميل:**
- المطابقة تلقائية وموضوعية
- الفريق يركز على العميل بدل البحث

---

### الخطوة 4.4: عرض Backlog Request

**الهدف:** إظهار الطلبات غير المطابقة

**المسار:**
```
Reports & Analytics > Backlog Report
```

**ما يجب إظهاره:**
- الطلبات التي لم تجد وحدة مناسبة
- أسباب عدم المطابقة
- المتابعة المطلوبة

---

## الجزء الخامس: التقارير والإدارة التنفيذية (10 دقيقة)

### الخطوة 5.1: عرض CFO Dashboard

**الهدف:** إظهار لوحة تحكم CFO الشاملة

**المسار:**
```
Executive Presentation Center
→ CFO Project Control Summary
→ project = PROJ-0002
```

**ما يجب إظهاره:**
- ملخص مالي شامل
- Budget vs Committed vs Invoiced vs Certified
- المخاطر والتنبيهات

**ما يُثبته للعميل:**
- CFO يرى كل شيء في مكان واحد

---

### الخطوة 5.2: عرض التدفق النقدي

**الهدف:** إظهار توقعات التدفق النقدي

**المسار:**
```
Executive Control Center
→ Project Cash Flow Forecast
→ project = PROJ-0002
```

**ما يجب إظهاره:**
- Periods (Monthly / Quarterly)
- inflow (PO uninvoiced + PI outstanding + IPC payable + retention)
- outflow (future outflows)
- running_balance
- cash_risk_status (Green / Yellow / Red)
- lowest_projected_balance

**ما يُثبته للعميل:**
- متى ستكون الحاجة للنقد
-哪里在哪里需要准备资金

---

### الخطوة 5.3: عرض EVM Metrics

**الهدف:** إظهار مؤشراتEarned Value Management

**المسار:**
```
Executive Presentation Center
→ Project EVM Metrics
→ project = PROJ-0002
```

**ما يجب إظهاره:**
- BAC (Budget at Completion)
- EV (Earned Value) — من certified_amount
- AC (Actual Cost) — من invoiced_amount
- PV (Planned Value)
- CV, SV (Cost/Schedule Variance)
- CPI, SPI (Performance Indices)
- EAC, ETC, VAC
- overall_evm_status (On Track / Watch / At Risk)

**التقارير:**
```
Reports & Analytics > EVM Forecast Summary
```

```
Reports & Analytics > Project Financial Snapshot
→ project = PROJ-0002
```

**ما يُثبته للعميل:**
- مقارنة بين المخطط والفعلي
- مؤشر أداء التكلفة والجدول
- توقعات النهاية

---

### الخطوة 5.4: عرض التقارير المالية التفصيلية

**المسار:**
```
Reports & Analytics > Work Item Financial Ledger
→ project = PROJ-0002
```

```
Reports & Analytics > Unit Financial Ledger
→ project = PROJ-0002
```

```
Reports & Analytics > GL Dimension Traceability
→ project = PROJ-0002
```

---

## الجزء السادس: الصيانة والوثائق (5 دقائق)

### الخطوة 6.1: عرض طلبات الصيانة

**الهدف:** إظهار إدارة صيانة الوحدات

**المسار:**
```
Reports & Analytics > Open Maintenance Requests
→ project = PROJ-0002 (or all)
```

**ما يجب إظهاره:**
- 4 طلبات صيانة (PMR-2026-00001 through PMR-2026-00004)
- أنواع المشاكل: Electrical / Plumbing / AC / Civil
- الحالات: New / Under Review / In Progress / Completed
- التكلفة: estimated_cost vs actual_cost

**ما يُثبته للعميل:**
- الصيانة مرتبطة بالوحدة
- التكلفة تتبع (إدارية فقط — لا GL entries)

---

### الخطوة 6.2: عرض الوثائق العقارية

**الهدف:** إظهار تتبع الوثائق وتواريخ الانتهاء

**المسار:**
```
Reports & Analytics > Property Document Register
```

```
Reports & Analytics > Expiring Documents Report
```

**ما يجب إظهاره:**
- 3 وثائق (PDOC-2026-00001 through PDOC-2026-00003)
- الأنواع: Title Deed / Drawing / License
- الحالة: Active
- تاريخ الانتهاء (للمتابعة)

**ما يُثبته للعميل:**
- الوثائق مرتبطة بالوحدات والمشاريع
- تنبيهات انتهاء الصلاحية

---

## الجزء السابع: البوابة والتنبيهات (5 دقائق)

### الخطوة 7.1: عرض جاهزية البوابة

**الهدف:** توضيح وضع الأساس للبوابة

**المسار:**
```
Reports & Analytics > Portal Access Register
```

```
Reports & Analytics > Portal Access by Party
```

**التوضيح للعميل:**
> "هذا وضع الأساس فقط. لا يتم إنشاء مستخدمين تلقائياً. التفعيل الفعلي للبوابة سيكون في المرحلة القادمة."

---

### الخطوة 7.2: عرض التنبيهات الآلية

**المسار:**
```
Reports & Analytics > Pending Reminder Actions
```

```
Reports & Analytics > Notification Readiness Report
```

**ما يجب إظهاره:**
- 6 سيناريوهات (Reservation Expiry / Installment Due / Rent Due / Lease Expiry / Document Expiry / Backlog Matched Unit)
- Automation Logs (سجلات التنبيهات المعلقة)

**التوضيح للعميل:**
> "هذا سجل التنبيهات المخطط لها. الإرسال الفعلي للرسائل سيكون في المرحلة القادمة."

---

## ملخص ماذا يُثبته كل جزء

| الجزء | ماذا يُثبته للعميل |
|---|---|
| Part 1 | التخطيط الإنشائي → مقاولون → شهادات — مسار كامل |
| Part 2 | المخزون العقاري → تخصيص التكلفة → ربحية الوحدات |
| Part 3 | الحجز → البيع → الأقساط — دورة المبيعات |
| Part 4 | CRM → مطابقة ذكية → Backlog — خط المبيعات |
| Part 5 | CFO Dashboard → Cash Flow → EVM — الإدارة التنفيذية |
| Part 6 | الصيانة → الوثائق — صيانة الأصول |
| Part 7 | البوابة → التنبيهات — جاهزية المرحلة التالية |

---

## التوصيات للعرض

1. **ابدأ بالمشروع العام:** ابدأ بـ PROJ-0002 ثم اتجه للتفاصيل
2. **أظهر التدفق وليس الشاشات الفردية:** أهم ما يُثبته هو كيف تتصل الوحدات
3. **أظهر التقارير لا الشاشات فقط:** التقارير هي ما يستخدمه المدير يومياً
4. **أوقف عند الـ gaps:** إذا سأل العميل عن Invoice/Payment — وضّح أنه مؤجل
5. **أظهر التنبيهات وليس الإرسال:** وضّح أن التنبيهات وضع أساس فقط