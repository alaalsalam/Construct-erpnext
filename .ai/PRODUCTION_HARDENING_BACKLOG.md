---
name: PRODUCTION_HARDENING_BACKLOG
description: Phase 2 production hardening backlog — permissions, print, data, performance, security
type: project
---

# قائمة تقسية الإنتاج — مرحلة ما قبل الإنتاج
# Production Hardening Backlog
**Date:** 2026-05-15
**Priority:** High — before go-live

---

## مقدمة

هذا المستند يحدد العمل المتبقي لتحويل النظام من مرحلة العرض التوضيحي إلى مرحلة الإنتاج. العناصر مرتبة حسب الأولوية. الهدف هو ضمان أمان وموثوقية وقابلية التوسع للنظام.

---

## 1. الأذونات والصلاحيات (Permissions)

**الأولوية:** Critical

### 1.1 مراجعة Role Groups

| المهمة | الوصف | المسؤول |
|---|---|---|
| مراجعة Role Groups | مراجعة كل Role Group (مثل "Project Manager Bundle") والتأكد من أن الأدوار صحيحة | System Manager |
| التحقق من الأدوار | التأكد من أن كل مستخدم له الأدوار المناسبة لدوره | System Manager |
| توثيق الصلاحيات | توثيق صلاحيات كل دور في جدول | System Manager |

### 1.2 تفعيل Access Scope

| المهمة | الوصف | المسؤول |
|---|---|---|
| تفعيل AccessScope | تفعيل نظام AccessScope لكل مستخدم مشروع | System Manager |
| اختبار Scope | اختبار أن Scope يقيّد الوصول بشكل صحيح | System Manager |
| Policy document | إنشاء policy يشرح متى يُستخدم Scope | System Manager |

### 1.3 صلاحيات الوحدات النمطية

| الوحدة النمطية | الدور | الصلاحيات المطلوبة |
|---|---|---|
| Construction BOQ | Projects Manager | CRUD + Submit + Cancel |
| Construction Work Item | Projects Manager | Read + Write |
| Contractor Account | Projects Manager + Accounts Manager | Read + Write |
| Measurement Book | QS Engineer | Create + Write + Submit |
| IPC | QS Engineer + Projects Manager | Submit + Cancel |
| Real Estate Project | Projects Manager + Sales Manager | Read + Write |
| Unit | Sales Manager | Read + Write |
| Sales Contract | Sales Manager | Create + Write + Submit + Cancel |
| Lease Contract | Sales Manager | Create + Write + Submit + Cancel |
| Customer Requirement | Sales Manager | CRUD |
| Match Result | Sales Manager | Read + Write |
| Property Maintenance | Projects Manager | CRUD |
| CFO Analytics | Accounts Manager + CFO | Read + Report |
| Audit Trail | Audit Administrator | Read + Export |

---

## 2. تنسيقات الطباعة (Print Formats)

**الأولوية:** High

### 2.1 تنسيقات المرحلة الأولى

| المستند | التنسيق | الحالة | ملاحظات |
|---|---|---|---|
| Construction BOQ | BOQ Print Format | غير مفعل | يحتاج تفعيل |
| Construction Work Item | Work Item Print Format | غير مفعل | يحتاج تفعيل |
| Measurement Book | Measurement Book Print | غير مفعل | يحتاج تفعيل |
| IPC | IPC Certificate Print | غير مفعل | يحتاج تفعيل |
| Sales Contract | Sales Contract Print | غير مفعل | يحتاج تفعيل |
| Lease Contract | Lease Contract Print | غير مفعل | يحتاج تفعيل |
| Unit | Unit Card Print | غير مفعل | يحتاج تفعيل |
| Contractor Account Statement | Statement Print | غير مفعل | يحتاج تفعيل |
| Retention Register | Retention Report Print | غير مفعل | يحتاج تفعيل |

### 2.2 checklist التفعيل

- [ ] تفعيل كل print format
- [ ] مراجعة التخطيط (header, footer, logo, watermark)
- [ ] التأكد من RTL support (العربية)
- [ ] التأكد من page breaks صحيحة
- [ ] اختبار على printer فعلي
- [ ] طباعة نموذجية لكل تنسيق

---

## 3. استيراد البيانات (Data Import)

**الأولوية:** High

### 3.1 Import Templates

| DocType | Template | ملاحظات |
|---|---|---|
| Construction BOQ | Import BOQ from Excel | بنود BOQ + amounts |
| Construction Work Item | Import Work Items | من Excel |
| Unit | Import Units | مشروع + مبنى + دور + وحدة + نوع |
| Real Estate Project | Import REP | معلومات المشروع |
| Customer Requirement | Import Requirements | CRM data |
| Broker | Import Brokers | بيانات الوسطاء |

### 3.2 التحقق

- [ ] إنشاء import templates لكل doctype
- [ ] اختبار import على بيانات تجريبية
- [ ] توثيق خطوات الاستيراد (PDF/SOP)
- [ ] اختبار edge cases (duplicate, missing fields, invalid data)
- [ ] وضع حدود على حجم الملف
- [ ] اختبار rollback عند الفشل

---

## 4. الأداء (Performance)

**الأولوية:** Medium

### 4.1 مراقبة الأداء

| المهمة | الوصف |
|---|---|
| Stress test | اختبار الحمل على بيانات PROJ-0002 (72 work items) + بيانات أكبر |
| SQL queries | مراجعة الـ queries البطيئة في CFO analytics و Reports |
| Index check | التأكد من وجود indexes على: project, contractor, unit, status |
| Page load times | قياس وقت تحميل الشاشات الرئيسية |

### 4.2 تحسينات محتملة

| الموضع | التحسين |
|---|---|
| Project Financial Snapshot | تحسين SQL aggregation |
| Cash Flow Forecast | تحسين period calculation |
| Unit Cost Allocation | تحسين batch processing |
| Reports | إضافة pagination للجداول الكبيرة |

---

## 5. الأمان (Security)

**الأولوية:** Critical

### 5.1 مراجعة الأمان

| المهمة | الوصف |
|---|---|
| تفعيل Audit Trail Config | تفعيل تتبع التغييرات على DocTypes الحرجة |
| مراجعة User Permissions | التأكد من أن كل مستخدم له الصلاحيات المناسبة |
| تشفير البيانات الحساسة | مراجعة أي بيانات تحتاج تشفير إضافي |
| مراجعة API permissions | التأكد من أن whitelisted functions محمية |

### 5.2 DocTypes للمراقبة

| DocType | الحقول المراقبة |
|---|---|
| Contractor Ledger Entry | all fields (immutable) |
| Sales Contract | sale_price, customer, status |
| Lease Contract | monthly_rent, customer, status |
| Unit | status, expected_sale_price, allocated_cost |
| Financial Snapshot | all calculated values |

### 5.3 اختبار الأمان

- [ ] اختبار authorization rule (Access Scope)
- [ ] اختبار防止 SQL injection
- [ ] اختبار XSS prevention
- [ ] اختبار CSRF protection
- [ ] مراجعة API key permissions

---

## 6. النسخ الاحتياطي (Backup)

**الأولوية:** Critical

### 6.1 خطة النسخ

| المهمة | الوصف |
|---|---|
| تفعيل النسخ التلقائي | 매일/weekend/monthly backups |
| موقع النسخ | /backups على خادم منفصل أو cloud |
| اختبار الاستعادة | التأكد من أن النسخ قابلة للاستعادة |
| توثيق خطة الطوارئ | ماذا نفعل إذا فشل الـ backup |

### 6.2 checklist النسخ

- [ ] تفعيل scheduled backup
- [ ] اختبار استعادة من أحدث نسخة
- [ ] توثيق خطوة الاستعادة
- [ ] تحديد مسؤول النسخ
- [ ] جدول النسخ الشهري

---

## 7. المراقبة (Monitoring)

**الأولوية:** High

### 7.1 التنبيهات

| السيناريو | التنبيه | القناة |
|---|---|---|
| Server down | تنبيه فوري | Email/SMS |
| Disk full | تنبيه قبل 20% | Email |
| Slow query | تنبيه للأدمن | Log |
| IPC rejected | تنبيه للـ Projects Manager | In-app |
| Unit status change | تنبيه للـ Sales Manager | In-app |

### 7.2 التقارير الدورية

| التقرير | التكرار | المرسل إلى |
|---|---|---|
| CFO Dashboard | أسبوعي | CFO |
| Cash flow forecast | أسبوعي | CFO |
| Overdue installments | أسبوعي | Sales Manager |
| Expiring documents | شهري | Projects Manager |
| Maintenance cost | شهري | Projects Manager |

### 7.3 Logs

- [ ] تفعيل error log للـ CFO analytics
- [ ] تفعيل access log للـ sensitive doctypes
- [ ] مراجعة log retention policy

---

## 8. التدريب (Training)

**الأولوية:** High

### 8.1 دليل المستخدم

| الوحدة النمطية | محتوى الدليل |
|---|---|
| Construction BOQ | إنشاء BOQ، تتبع التنفيذ، تقارير |
| Contractor Management | إدارة المقاولين، كشف الحساب، Retention |
| Real Estate Inventory | إدارة المخزون، تخصيص التكلفة |
| Sales & Rental | دورة البيع، الأقساط، التقارير |
| CRM & Smart Matching | إدارة العملاء، المطابقة |
| CFO Analytics | التقارير، التدفق النقدي، EVM |

### 8.2 سيناريوهات التدريب

1. إنشاء BOQ جديد من الصفر
2. إنشاء IPC من القياسات
3. حجز وحدة وتحويلها لعقد بيع
4. تشغيل Unit Cost Allocation
5. تشغيل Smart Matching لعميل جديد

### 8.3 checklist التدريب

- [ ] كتابة دليل المستخدم لكل وحدة
- [ ] تسجيل فيديوهات تدريب (اختياري)
- [ ] تدريب فريق العمل (2-3 sessions)
- [ ] توثيق الأسئلة الشائعة (FAQ)

---

## 9. المراجعة المحاسبية النهائية (Final Accounting Review)

**الأولوية:** Critical

### 9.1 الأبعاد المحاسبية

| المهمة | الوصف |
|---|---|
| مراجعة FinancialDimensionSettings | التأكد من أن الأبعاد مفعلة بشكل صحيح |
| اختبار purchase transactions | التأكد من أن الأبعاد تصل لـ GL |
| التأكد من Unit dimension | التأكد من أن Unit dimension يصل للـ Sales Invoice |

### 9.2 التقارير المحاسبية

| التقرير | الوصف |
|---|---|
| GL Dimension Traceability | يعرض الأبعاد لكل GL entry |
| Work Item Financial Ledger | كشف مالي لكل Work Item |
| Unit Financial Ledger | كشف مالي لكل وحدة |
| Contractor Account Statement | كشف حساب المقاول |

### 9.3 Journal Entry Review

- [ ] مراجعة القيود اليومية العكسية (reversals)
- [ ] التأكد من أن القيود متوازنة
- [ ] مراجعة حساباتRetention و Advance
- [ ] التأكد من عدم وجود قيود يتيمة

---

## 10. مراجعة التكامل (Integration Review)

**الأولوية:** High

### 10.1 تكامل ERPNext

| الوحدة | التكامل | الحالة |
|---|---|---|
| Procurement | ERPNext Purchase Order | Working — syncs to Work Items |
| Measurement | ERPNext Stock Entry | Working — consumed_qty updates |
| Sales | ERPNext Sales Invoice | مؤجل للخطوة التالية |
| Rental | ERPNext Sales Invoice (rent) | مؤجل |
| CRM | ERPNext Lead/Customer | Working — links preserved |
| Accounting | ERPNext GL | Working — via IPC |

### 10.2 Sync Hooks

| Hook | الوصف |
|---|---|
| work_item_sync | Procurement → Work Item quantities |
| boq_sync | BOQ ↔ Work Items (bidirectional) |
| ledger_utils | IPC → Contractor Ledger |
| measurement_utils | ME → Work Item measured_qty |
| ipc.py | IPC → Work Item certified_qty |
| inventory_utils | Unit → REP/Building/Floor counts |

### 10.3 checklist التكامل

- [ ] اختبار sync hooks بالكامل
- [ ] التأكد من أن no orphaned records
- [ ] مراجعة error handling في كل sync
- [ ] اختبار edge cases (cancelled docs, amendments)

---

## 11. ملخص الأولويات

### Critical (قبل go-live)
1. ✅ الأذونات والصلاحيات — مراجعة Role Groups + Access Scope
2. ✅ المراجعة المحاسبية — الأبعاد تصل للـ GL
3. ✅ الأمان — Audit Trail + User permissions
4. ✅ النسخ الاحتياطي — تفعيل + اختبار استعادة

### High (قبل go-live)
5. تنسيقات الطباعة — تفعيل الـ print formats الرئيسية
6. المراقبة — التنبيهات + التقارير الدورية
7. التدريب — دليل المستخدم + تدريب الفريق
8. استيراد البيانات — templates + SOP

### Medium (بعد go-live)
9. الأداء — stress test + query optimization
10. تكامل ERPNext — مراجعة الـ sync hooks
11. Backlog features — تفصيل الـ Backlog Matching

---

## 12. المسؤوليات

| المهمة | المسؤول | الموعد |
|---|---|---|
| الأذونات | System Manager | قبل UAT |
| الطباعة | Projects Manager | قبل go-live |
| استيراد البيانات | System Manager | قبل go-live |
| الأداء | Dev team | Sprint 1 after UAT |
| الأمان | System Manager + Dev | قبل go-live |
| النسخ الاحتياطي | DevOps | خلال week 1 |
| المراقبة | DevOps | Sprint 1 after UAT |
| التدريب | Sales/Projects Manager | Sprint 2 after UAT |
| المراجعة المحاسبية | Accounts Manager | قبل go-live |
| مراجعة التكامل | Dev team | Sprint 1 after UAT |