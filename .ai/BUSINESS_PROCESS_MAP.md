---
name: BUSINESS_PROCESS_MAP
description: High-level business process map with module-to-module transitions
type: reference
---

# خريطة العمليات التجارية
# Business Process Map — Real Estate Development ERP

---

## 1. نظرة عامة: العمليات الرئيسية

النظام يدير 4 سلاسل عمليات متصلة:

```
سلاسل العمليات الأربع:
├── سلسلة الإنشاء والتعاقد (Construction & Contractor Chain)
├── سلسلة المخزون والربحية (Inventory & Profitability Chain)
├── سلسلة المبيعات والإيجار (Sales & Rental Chain)
└── سلسلة إدارة العملاء (CRM & Matching Chain)
```

---

## 2. سلسلة الإنشاء والتعاقد

### 2.1 عملية التخطيط الإنشائي

```
┌─────────────┐     ┌─────────────┐     ┌─────────────────────┐     ┌────────────────────┐
│   Project   │────▶│  Construction│────▶│ Construction BOQ Item│────▶│Construction Work  │
│  (ERPNext)  │     │     BOQ     │     │   (72 items in      │     │      Item          │
│             │     │  (submit)   │     │   PROJ-0002)        │     │  (operational hub) │
└─────────────┘     └─────────────┘     └─────────────────────┘     └─────────┬──────────┘
                                                                              │
        ┌──────────────────────────────────────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────────┐
│  Construction Work Item (the central link) │
│  ─────────────────────────────────────────  │
│  procurement_status: Requested/Ordered/... │
│  measurement_status: Not Measured/...      │
│  certification_status: Not Certified/...   │
│  planned_quantity vs actuals                │
└───────────┬───────────────┬─────────────────┘
            │               │
            ▼               ▼
    ┌───────────────┐ ┌─────────────────┐
    │  Procurement  │ │   Measurement   │
    │  Control      │ │   Book          │
    │  (MR/PO/PR/PI)│ │   Entry         │
    └───────────────┘ └────────┬─────────┘
                               │
                               ▼
                    ┌───────────────────┐
                    │   Measurement      │
                    │   Entry           │
                    │   (verified)      │
                    └────────┬──────────┘
                             │
                             ▼
                   ┌──────────────────┐
                   │  IPC             │
                   │  (certified)     │
                   └────────┬─────────┘
                            │
        ┌───────────────────┼───────────────────────┐
        ▼                   ▼                       ▼
┌──────────────┐   ┌─────────────────┐   ┌──────────────────┐
│Contractor    │   │  Contractor      │   │   CFO Analytics  │
│Account       │   │  Ledger Entry    │   │  (certified amt) │
│(financial    │   │  (sub-ledger)    │   │                  │
│subledger)    │   │                  │   │                  │
└──────────────┘   └──────────────────┘   └──────────────────┘
        │                   │
        ▼                   ▼
┌──────────────┐   ┌─────────────────┐
│Retention     │   │  Purchase Invoice│
│Register      │   │  (from IPC)     │
│(held/released)│   └─────────────────┘
├──────────────┤
│Advance       │
│Register      │
├──────────────┤
│Guarantee     │
│Register      │
└──────────────┘
```

### 2.2 علاقات سلسلة الإنشاء

| الانتقال | الوصف |
|---|---|
| Project → BOQ | إنشاء BOQ على المشروع. ينشئ Work Items على الإرسال. |
| BOQ Item → Work Item | كل صف BOQ يولد عنصر عمل واحد. 1:1 relationship. |
| Work Item → Procurement | المشتريات تربط بالـ Work Item. Pipeline يتتبع على Work Item. |
| Work Item → Measurement | القياسات تربط بالـ Work Item. qty يتتبع على Work Item. |
| Measurement Entry → IPC | إدخال القياس (المقبول) يصبح خط IPC. |
| IPC → Contractor Account | إرسال IPC يحدث قيد في كشف المقاول. |
| IPC → Contractor Ledger | Ledger Entry يُنشأ تلقائياً لكل IPC. |
| IPC → Retention Register | Retention Register يُنشأ تلقائياً من IPC. |
| IPC → Purchase Invoice | IPC ينشئ Purchase Invoice (إنشاء يدوي). |

### 2.3 DocTypes في سلسلة الإنشاء ودورها

| DocType | الدور في العملية |
|---|---|
| Construction BOQ | الأساس — يحدد الكميات والأسعار والتكلفة الإجمالية |
| Construction BOQ Item | صف الـ BOQ — يحدد بند واحد بتكلفة ومصدر |
| Construction Work Item | المحور المركزي — يربط التخطيط بالعمليات |
| Cost Code | التصنيف — يفرق التكلفة (Material/Labor/Equipment/Subcontract) |
| WBS Element | الهيكل — ينظم العمل في مراحل |
| ProcurementControlSettings | التحكم — يفرض ربط المشتريات بالـ Work Item |
| MeasurementBook | التنظيم — يجمع القياسات في فترة واحدة |
| MeasurementEntry | القياس الفعلي — يسجل الكمية المقاسة في الموقع |
| InterimPaymentCertificate | الشهادة — يوثق العمل المعتمد مالياً |
| InterimPaymentCertificateLine | خط الشهادة — يربط القياس بالـ Work Item والـ BOQ |
| IPCDeduction | الحسومات — يشرح الـ deductions (retention/advance/penalty/wht) |
| ContractorAccount | الملف المالي — يجمع كل المعاملات المالية للمقاول |
| ContractorLedgerEntry | القيد الفرعي — يسجل كل معاملة (immutable) |
| RetentionRegister | تتبع الـ Retention — يحتجز ويُطلق |
| AdvanceRegister | تتبع السلف — يصرف ويُسترد |
| GuaranteeRegister | تتبع الضمانات — يراقب تاريخ الانتهاء |

---

## 3. سلسلة المخزون والربحية

```
┌─────────────┐     ┌────────────────┐     ┌──────────────┐     ┌──────────────┐
│   Project   │────▶│ Real Estate    │────▶│   Building   │────▶│    Floor     │
│  (ERPNext)  │     │    Project     │     │              │     │              │
└─────────────┘     └───────┬────────┘     └──────────────┘     └──────┬───────┘
                            │                                          │
                            ▼                                          ▼
                    ┌────────────────┐                    ┌────────────────┐
                    │      Unit       │◀───────────────────│ Property Owner │
                    │   (24 units)   │                    │                │
                    └───────┬─────────┘                    └───────┬────────┘
                            │                                      │
                            ▼                                      ▼
                    ┌────────────────┐                    ┌────────────────┐
                    │ Property       │                    │Property        │
                    │ Ownership      │                    │Ownership       │
                    │ (percentage)  │                    │(link)          │
                    └───────┬────────┘                    └────────────────┘
                            │
                            ▼
                    ┌────────────────────────────────┐
                    │     Unit Cost Allocation       │
                    │  (from Project Financial       │
                    │   Snapshot or BOQ total)       │
                    └───────────────┬──────────────────┘
                                    │
                                    ▼
                            ┌──────────────────┐
                            │ Unit             │
                            │ Profitability    │
                            │ (allocated_cost, │
                            │  expected_margin,│
                            │  profitability) │
                            └──────────────────┘
                                    │
                                    ▼
                            ┌──────────────────┐
                            │ Unit can be:     │
                            │ Reserved → Sold  │
                            │ Reserved → Rented│
                            └──────────────────┘
```

### 3.1 علاقات سلسلة المخزون

| الانتقال | الوصف |
|---|---|
| Project → Real Estate Project | REP تربط المشروع الإنشائي بالمشروع العقاري |
| Real Estate Project → Building | كل مبنى ينتمي لمشروع واحد |
| Building → Floor | كل دور ينتمي لمبنى واحد |
| Floor → Unit | كل وحدة تنتمي لدور واحد |
| Unit → Property Owner | المالك منفصل عن الوحدة (N:M relationship) |
| Property Owner → Property Ownership | يحدد نسبة الملكية ونوعها |
| Unit → Unit Cost Allocation | التكلفة توزع من المشروع على الوحدات |
| Unit Cost Allocation → Unit | عند التطبيق، الـ Unit تستقبل allocated_cost |

### 3.2 DocTypes في سلسلة المخزون ودورها

| DocType | الدور في العملية |
|---|---|
| Real Estate Project | الجذر — يربط ERPNext Project بالمخزون العقاري |
| Building | التجميع — يجمع الأدوار والوحدات في مبنى |
| Floor | التجميع — يجمع الوحدات في دور |
| Unit | الأصل — الوحدة القابلة للبيع/الإيجار. محور كل شيء. |
| Unit Type | التصنيف — يحدد نوع الوحدة (2 Bedroom / 3 Bedroom / Penthouse) |
| Property Owner | الطرف — ملف المالك المستقل عن ERPNext parties |
| Property Ownership | الرابط — يربط المالك بالوحدة بنسبة ومدة |
| Unit Reservation | المعاملة — تحجز الوحدة مؤقتاً |
| Unit Cost Allocation | التوزيع — يوزع تكلفة المشروع على الوحدات |
| Unit Cost Allocation Line | صف التوزيع — يربط الوحدة بالمبلغ الموزع |

---

## 4. سلسلة المبيعات والإيجار

### 4.1 دورة البيع

```
Unit (Available)
      │
      ▼
Unit Reservation (Sale type, Reserved)
      │
      ▼ (on Contract Submit)
Sales Contract (Approved)
      │
      ├─── Sale Price / Down Payment
      │
      ▼
Sales Installment Schedule
      │
      ├── Installment 1: Down Payment
      ├── Installment 2: Construction Milestone
      ├── Installment 3: Handover
      │
      ▼ (Phase 2 — not yet active)
Sales Invoice ──► Payment Entry
      │
      ▼
Unit (Sold)
```

### 4.2 DocTypes في سلسلة البيع ودورها

| DocType | الدور في العملية |
|---|---|
| Unit Reservation | المعاملة — تحجز الوحدة للمشتري. تحول إلى عقد عند التحويل. |
| Sales Contract | العقد — يربط المشتري بالوحدة. يُحدث Unit status. |
| Sales Installment Schedule | الجدول — يحدد الأقساط (مبلغ/تاريخ/نوع). المرحلة الأولى: قابل للإرسال فقط. |
| SalesContractSettings | التحكم — يحدد قواعد التحقق والتسلسل |
| SalesInvoiceCollectionSettings | التحكم — يحدد قواعد إنشاء الفواتير (مؤجل) |
| SalesInvoiceUtils | الأداة — لإنشاء الفواتير (مؤجل) |
| CollectionsUtils | الأداة — لتتبع التحصيل (مؤجل) |

### 4.3 دورة الإيجار

```
Unit (Available)
      │
      ▼
Unit Reservation (Rent type, Reserved)
      │
      ▼ (on Contract Submit)
Lease Contract (Approved)
      │
      ├─── Monthly Rent
      │
      ▼
Rent Schedule
      │
      ├── Rent 1: YYYY-MM-01
      ├── Rent 2: YYYY-MM-01
      ├── ...
      │
      ▼ (Phase 2 — not yet active)
Rent Invoice ──► Payment Entry
      │
      ▼
Unit (Rented) — Tenant stored on Lease Contract, NOT on Unit
```

### 4.4 DocTypes في سلسلة الإيجار ودورها

| DocType | الدور في العملية |
|---|---|
| Unit Reservation | المعاملة — تحجز الوحدة للمستأجر (النوع Rent) |
| Lease Contract | العقد — يربط المستأجر بالوحدة. Tenant على العقد فقط. |
| Rent Schedule | الجدول — يُولد تلقائياً من monthly_rent + billing_frequency |
| LeaseContractSettings | التحكم — يحدد قواعد التحقق والتسلسل |
| RentInvoiceCollectionSettings | التحكم — يحدد قواعد إنشاء فواتير الإيجار (مؤجل) |

---

## 5. سلسلة CRM والمطابقة

```
Lead / Customer
      │
      ▼
Customer Requirement (Buy / Rent / Investment)
      │
      ├── Preferred Project
      ├── Unit Type
      ├── Budget Range
      ├── Area Range
      │
      ▼
Viewing Appointment (optional — if customer wants to see)
      │
      ▼
Real Estate Follow Up (optional — ongoing engagement)
      │
      ▼
Smart Matching (scored algorithm)
      │
      ├── Weights: Location (10), Price (35), Area (25), Type (20), Feature (10)
      └── Minimum Score: 60
      │
      ▼
Match Result (ranked units)
      │
      ├── Matched: Unit Reserved → Sales/Rental Flow
      │
      └── Not Matched (score < 60):
              │
              ▼
          Backlog Request
              │
              ▼ (when unit becomes available)
          Backlog Matching
```

### 5.1 DocTypes في سلسلة CRM ودورها

| DocType | الدور في العملية |
|---|---|
| Customer Requirement | القائد — يحدد حاجة العميل (شراء/إيجار/استثمار) |
| Viewing Appointment | النشاط — يوثق معاينات العقارات |
| Real Estate Follow Up | النشاط — يوثق متابعة العميل |
| Matching Settings | التحكم — يحدد أوزان المطابقة |
| Match Result | المخرج — يعرض الوحدات المصنفة حسب الدرجة |
| Match Result Item | صف النتيجة — يعرض وحدة واحدة بدرجتها |
| Backlog Request | المخرج البديل — يلتقط الطلب غير المطابق |
| Backlog Match Attempt | تتبع — يوثق محاولة المطابقة للـ Backlog |

---

## 6. سلسلة الصيانة والوثائق

```
Unit
  │
  ▼
Property Maintenance Request
  │
  ├── Requester Type: Owner / Tenant / Buyer / Internal
  ├── Issue Type: Electrical / Plumbing / AC / Civil / ...
  └── Cost: estimated vs actual (management only — no GL)
  │
  ▼
Property Maintenance Task (child of request)
  │
  ▼ (optional)
Property Document (linked to project/unit/owner/contract)
  │
  ├── Document Type: Title Deed / Contract / Drawing / License / Other
  ├── Status: Active / Expired / Under Review / Archived
  └── Expiry Date: triggers expiring documents report
```

### 6.1 DocTypes في سلسلة الصيانة والوثائق

| DocType | الدور في العملية |
|---|---|
| Property Maintenance Request | القائد — يوثق مشكلة الصيانة. Requester غير مرتبط بـ Property Ownership. |
| Property Maintenance Task | الفرعي — المهمة الواحدة ضمن طلب الصيانة |
| Property Document | المرن — يربط بأي سجل (project/unit/owner/customer/supplier/contracts) |
| Contract Attachment Register | المتخصص — يربط الوثائق بالعقود فقط |

---

## 7. سلسلة CFO والإدارة التنفيذية

```
الأعلى: التقارير والإدارة
         │
         ▼
┌──────────────────────────────────────────────┐
│            CFO Analytics Layer               │
│                                              │
│  Project Financial Snapshot                   │
│    ← Work Items (BOQ, procurement, measure)  │
│    ← IPC (certified amounts)                 │
│    ← Contractor Account (outstanding)         │
│    ← Retention Register (held/released)      │
│                                              │
│  Project EVM Metrics                          │
│    ← Work Items (BAC/EV/AC/PV)               │
│    ← IPC / Purchase Invoice                   │
│                                              │
│  Project Cash Flow Forecast                   │
│    ← Purchase Order (uninvoiced)             │
│    ← Purchase Invoice (outstanding)          │
│    ← IPC (outstanding)                       │
│    ← Retention Register (release due)         │
└──────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────┐
│          9 Workspaces                         │
│                                              │
│  0.1 Executive Presentation Center             │
│  0.2 Executive Control Center                  │
│  0.3 Construction Control                      │
│  0.4 Procurement & Site Warehouses            │
│  0.5 Measurement & IPC                         │
│  0.6 Contractor Management                     │
│  0.7 Real Estate Inventory                     │
│  0.8 Sales & Rental                            │
│  0.9 Reports & Analytics                       │
└──────────────────────────────────────────────┘
```

---

## 8. ملخص التبعيات الرئيسية

| من DocType | إلى DocType | نوع العلاقة | التفعيل |
|---|---|---|---|
| Construction BOQ | Construction Work Item | 1:many (on submit) | تلقائي |
| Work Item | Measurement Entry | 1:many (يدوي) | المستخدم |
| Measurement Entry | IPC | 1:many (on create IPC) | المستخدم |
| IPC | Contractor Ledger | 1:many (on submit) | تلقائي |
| IPC | Retention Register | 1:1 (on submit) | تلقائي |
| IPC | Purchase Invoice | 1:1 (يدوي) | المستخدم |
| Purchase Invoice | Payment Entry | 1:many (يدوي) | المستخدم |
| Unit Reservation | Sales Contract | 1:1 (on convert) | تلقائي |
| Sales Contract | Unit | 1:1 (on submit) | تلقائي |
| Unit Reservation | Lease Contract | 1:1 (on convert) | تلقائي |
| Lease Contract | Unit | 1:1 (on submit) | تلقائي |
| Customer Requirement | Match Result | 1:1 (on run matching) | تلقائي |
| Match Result | Customer Requirement | 1:1 (status update) | تلقائي |
| Unit Cost Allocation | Unit | 1:many (on apply) | المستخدم |
| Property Document | Unit / Project / Owner / etc. | Polymorphic | المستخدم |

---

## 9. ما لا يفعله النظام (Not in Scope for Phase 1)

| الوظيفة | السبب |
|---|---|
| Sales Invoice auto-creation | مؤجل للخطوة القادمة |
| Payment Entry auto-creation | مؤجل |
| Rent Invoice auto-creation | مؤجل |
| GL entries from Contract/Installment | مؤجل |
| Portal user provisioning | وضع الأساس فقط |
| External email/SMS sending | وضع الأساس فقط |
| GL backfill for historical data | مؤجل |
| Subcontract doctype | يستخدم ERPNext Subcontract |