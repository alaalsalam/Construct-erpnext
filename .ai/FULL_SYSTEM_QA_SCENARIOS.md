# سيناريوهات QA للنظام الكامل

## 1. التحكم بالمشروع

- فتح `PROJ-0002`.
- فتح `BOQ-PROJ-0002-001`.
- مراجعة بنود العمل والروابط إلى Cost Code و WBS و Item و UOM.
- تشغيل Project Purchase Control Summary والتأكد من المخطط، المتوقع، الفعلي، المتبقي، والانحراف.

## 2. المشتريات والمخازن

- فتح تقارير Work Item Procurement Summary و BOQ Procurement Pipeline.
- التأكد من ظهور الكميات المطلوبة والمطلوبة شراءً والمستلمة والمفوترة والمستهلكة.
- التأكد من عدم وجود إنشاء مستندات محاسبية غير مقصود.

## 3. القياسات والمستخلصات

- فتح Measurement Book و Measurement Entries لـ PROJ-0002.
- فتح IPCs المرتبطة.
- التأكد من السابق والحالي والإجمالي والمتبقي والمحتجزات.

## 4. اتفاقيات المقاولين

- فتح اتفاقيات المقاولين لـ PROJ-0002.
- التأكد من ربط Work Items والقياسات والمستخلصات.
- تشغيل Contractor Agreement Item Progress و Contractor Agreement to IPC Traceability.

## 5. التحليلات التنفيذية

- فتح Executive Presentation Center.
- فتح Project Financial Snapshot و Cash Flow Forecast و EVM Metrics.
- التأكد من أن الجداول تظهر مع المؤشرات بدون إخفاء البيانات.

## 6. التطوير العقاري

- فتح REP-2026-00002 والوحدات والملاك والملكية.
- تشغيل Unit Inventory و Unit Profitability و Project Unit Cost Matrix.

## 7. المبيعات والتحصيل

- فتح Sales Contracts لـ PROJ-0002.
- مراجعة الأقساط والفواتير.
- التأكد من أن `ACC-SINV-2026-00002` مرحّلة وأن Payment Entry الجزئية مرتبطة بها.
- التأكد من أن Unit Dimension موجود في GL Entry.

## 8. الإيجار والتحصيل

- فتح `LC-2026-00001`.
- مراجعة Rent Schedule والفاتورة الإيجارية والتحصيل الجزئي.
- تشغيل Tenant Statement و Rent Collection Report.

## 9. CRM والمطابقة

- فتح Customer Requirements.
- تشغيل Smart Matching و Backlog Matching reports.
- التأكد من أن المطابقة لا تنشئ حجوزات تلقائياً.

## 10. الصيانة والمستندات والبوابة والإشعارات

- فتح Maintenance Requests.
- فتح Property Documents.
- فتح Portal Access Profiles.
- فتح Pending Reminder Actions.
- التأكد من عدم تفعيل بوابة عامة أو إرسال إشعارات خارجية.

## قرار QA

النظام جاهز لاختبار UAT من العميل بشرط توضيح أن بعض الأجزاء هي Foundation/Readiness وليست تشغيل إنتاج كامل قبل اعتماد الصلاحيات والطباعة والسياسات المحاسبية.

