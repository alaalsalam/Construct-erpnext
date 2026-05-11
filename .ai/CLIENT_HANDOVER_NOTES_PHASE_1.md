# ملاحظات تسليم داخلية - المرحلة الأولى

## 1. الجاهز للعرض

المرحلة الأولى جاهزة للعرض حول `PROJ-0002` كسيناريو رئيسي. المسار يغطي التخطيط عبر BOQ، الربط مع عناصر العمل، المشتريات، المخزون، القياسات، IPC، المقاولين، CFO، المخزون العقاري، ربحية الوحدات، الحجوزات، عقود البيع، وجدولة الأقساط مع فواتير بيع مسودة.

## 2. ما يجب عدم تقديمه كمنجز نهائي

- التحصيل الكامل.
- فواتير بيع مرحلة ومقدمة للترحيل النهائي.
- Payment Entry.
- Journal Entry.
- دورة الإيجار الكاملة.
- العمولات.
- CRM والمطابقة الذكية.
- البوابات.
- WhatsApp / Meta.
- أتمتة محاسبية إنتاجية كاملة.

هذه ليست نواقص في العرض، بل نطاق المرحلة الثانية.

## 3. كيف نشرح Expected / Actual / Remaining

ابدأ من `BOQ-PROJ-0002-001` ثم افتح تقرير `Project Purchase Control Summary`.

الشرح المقترح:

- Planned Qty: الكمية المخططة في BOQ.
- Expected Qty: الكمية المتوقعة بعد الهالك أو التعديل التشغيلي.
- Requested / Ordered / Received / Consumed: أثر المشتريات والمخزون.
- Measured / Certified: أثر القياسات وIPC.
- Remaining: المتبقي من الكمية أو القيمة.
- Variance: الفرق بين المخطط والفعلي.

## 4. السجلات الرئيسية التي يجب فتحها

- Project: `PROJ-0002`
- Real Estate Project: `REP-2026-00002`
- BOQ: `BOQ-PROJ-0002-001`
- Normal Work Item: `CWI-2026-00008`
- Overrun Work Item: `CWI-2026-00006`
- Partial / Remaining Work Item: `CWI-2026-00003`
- Measurement Books: `MB-2026-00005` إلى `MB-2026-00008`
- IPCs: `IPC-2026-00002` إلى `IPC-2026-00005`
- Unit Cost Allocation: `UCA-2026-00005`
- Reservations: `RES-PROJ-0002-001` إلى `RES-PROJ-0002-010`
- Sales Contracts: `SC-PROJ-0002-001` إلى `SC-PROJ-0002-003`
- Draft Sales Invoices: `ACC-SINV-2026-00002` إلى `ACC-SINV-2026-00004`

## 5. مسار العرض المقترح

1. Executive Presentation Center
2. PROJ-0002 Financial Snapshot / KPI cards
3. `BOQ-PROJ-0002-001`
4. Project Purchase Control Summary
5. أمثلة Work Items:
   - `CWI-2026-00008` طبيعي
   - `CWI-2026-00006` تجاوز
   - `CWI-2026-00003` جزئي ومتبقي
6. Measurement Books
7. IPCs
8. Contractor Exposure
9. CFO Reports
10. `REP-2026-00002`
11. `UCA-2026-00005`
12. Unit Profitability
13. Reservations
14. Sales Contracts
15. Draft Sales Invoices
16. Phase 2 roadmap

## 6. ملاحظات تشغيلية

- لا يتم إرسال الفواتير المسودة كترحيل نهائي.
- لا يتم إنشاء Payment Entry أثناء العرض.
- لا يتم تشغيل GL backfill.
- عند سؤال العميل عن الإيجار أو التحصيل الكامل، يتم توضيح أنها مرحلة ثانية مخططة.
