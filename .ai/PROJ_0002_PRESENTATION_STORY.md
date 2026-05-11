# قصة عرض PROJ-0002 للمرحلة الأولى

## 1. لماذا PROJ-0002 هو مشروع العرض الرئيسي

تم إثراء `PROJ-0002` ليكون المسار الرئيسي في عرض المرحلة الأولى. أصبح المشروع يحتوي على بيانات مترابطة من التخطيط إلى التنفيذ والرقابة المالية والمخزون العقاري والبيع التأسيسي، بحيث يستطيع العميل متابعة القصة من بند BOQ حتى فاتورة بيع مسودة بدون ترحيل محاسبي.

## 2. السجلات الرئيسية التي تفتح أثناء العرض

- Project: `PROJ-0002` — مشروع برج الياسمين السكني.
- Real Estate Project: `REP-2026-00002`.
- Construction BOQ: `BOQ-PROJ-0002-001`.
- Measurement Books: `MB-2026-00005`, `MB-2026-00006`, `MB-2026-00007`, `MB-2026-00008`.
- IPCs: `IPC-2026-00002`, `IPC-2026-00003`, `IPC-2026-00004`, `IPC-2026-00005`.
- Draft Purchase Invoices from IPC: `ACC-PINV-2026-00004` إلى `ACC-PINV-2026-00007`.
- CFO: `PFS-2026-00002`, `PCF-2026-00002`, `EVM-2026-00002`.
- Unit Cost Allocation: `UCA-2026-00005`.
- Reservations: `RES-PROJ-0002-001` إلى `RES-PROJ-0002-010`.
- Sales Contracts: `SC-PROJ-0002-001`, `SC-PROJ-0002-002`, `SC-PROJ-0002-003`.
- Draft Sales Invoices: `ACC-SINV-2026-00002`, `ACC-SINV-2026-00003`, `ACC-SINV-2026-00004`.

## 3. تسلسل العرض المقترح

1. ابدأ من Executive Presentation Center مع فلترة التقارير على `PROJ-0002` قدر الإمكان.
2. افتح `BOQ-PROJ-0002-001` لشرح البنود والكميات والتكلفة المخططة، ثم استخدم زر Refresh Execution Summary عند الحاجة لتحديث ملخص التنفيذ من Work Items.
3. افتح Project Purchase Control Summary كالشاشة الأوضح لشرح Planned / Expected / Actual / Remaining / Variance.
4. افتح Work Item Procurement Summary لشرح Requested / Ordered / Received / Invoiced / Consumed / Remaining.
5. افتح BOQ Procurement Pipeline وProcurement Budget Control لشرح الانحرافات.
6. افتح Measurement Books `MB-2026-00005` إلى `MB-2026-00008` لشرح القياس الميداني.
7. افتح IPC Register ثم أحد المستخلصات `IPC-2026-00002` لشرح Previous / Current / Total / Remaining والاحتجاز.
8. افتح Contractor Account Statement وContractor Exposure Summary لشرح ذمم المقاول والاحتجاز.
9. افتح Project Financial Snapshot Report وCash Flow Forecast وEVM Metrics لشرح النظرة التنفيذية.
10. افتح `REP-2026-00002` ثم Unit Inventory Report لشرح المبنى والوحدات والحالات.
11. افتح Unit Profitability Report وProject Unit Cost Matrix لشرح توزيع التكلفة والربحية.
12. افتح Unit Reservation Register لشرح الحجز النشط والمنتهي والملغي والمحول.
13. افتح `SC-PROJ-0002-001` ثم Installment Schedule Report لشرح عقد البيع وجدول الأقساط.
14. افتح `ACC-SINV-2026-00002` كفاتورة بيع مسودة مرتبطة بقسط، مع توضيح أنها غير مرحلة.

## 4. شرح Expected / Actual / Remaining

- بند مكتمل: `CWI-2026-00008` حديد التسليح، المخطط `48,000` والمطلوب/المستلم/المستهلك/المقاس/المعتمد `48,000`، والانحراف `0%`.
- بند تجاوز: `CWI-2026-00006` خرسانة الأسقف، المخطط `680`، المطلوب `850`، المستهلك `816`، والانحراف المالي `20%`.
- بند جزئي/متبقي واضح: `CWI-2026-00003` أعمال الردم والتسوية، المخطط `1,800`، المقاس والمعتمد `1,170`، والمتبقي `630`.
- بند خرسانة أساسات عالي المخاطر: `CWI-2026-00060` يوضح أن القياس والاعتماد تجاوزا المخطط، لذلك يعرضه التقرير كـ Overrun وليس كبند جزئي.
- قياسات ومستخلصات: المستخلصات الأربعة تربط القياس بالاعتماد المالي والاحتجاز.

## 5. التقارير التي يجب فتحها

- Project Purchase Control Summary.
- Work Item Procurement Summary.
- BOQ Procurement Pipeline.
- Procurement Budget Control.
- Measurement to IPC Traceability.
- IPC Register.
- Contractor Account Statement.
- Contractor Exposure Summary.
- Project Financial Snapshot Report.
- Project Cash Flow Forecast Report.
- Project EVM Metrics Report.
- Unit Inventory Report.
- Unit Profitability Report.
- Unit Reservation Impact.
- Sales Contract Register.
- Installment Schedule Report.
- Sales Invoice from Installments Report.
- GL Dimension Traceability.
- Project Unit Cost Matrix.

## 6. ملاحظات مهمة

- تم إنشاء تقرير Project Purchase Control Summary ليكون شاشة العرض الأساسية لشرح المخطط، المتوقع، الفعلي، المتبقي، والانحراف لفلتر `PROJ-0002`.
- BOQ-PROJ-0002-001 يحتوي 72 صفاً مرتبطة بـ72 Work Items. لم يتم حذف أو دمج الصفوف لأن هناك مشتريات وقياسات ومستخلصات مرتبطة بها؛ لذلك يفضل استخدام التقرير الجديد للعرض التنفيذي السريع، ثم فتح BOQ للتفاصيل.
- توجد فواتير مشتريات مسودة من IPC، لكن لا توجد Payment Entries.
- توجد فواتير بيع مسودة فقط، ولا توجد Sales Invoice submitted أو GL Entry من مسار البيع.
- لا يوجد Journal Entry ولا GL backfill.
- التحصيل الكامل، الإيجار الكامل، العمولات، CRM، البوابات، وWhatsApp تبقى Phase 2.

## 7. القرار

`PROJ-0002` أصبح مشروع العرض الرئيسي الموصى به للمرحلة الأولى. البيانات جاهزة للعرض مع توضيح أن الفواتير والدفعات والترحيل المحاسبي الكامل مؤجلة إلى المرحلة التالية.

## 8. تحديث التسليم النهائي

- `BOQ-PROJ-0002-001` أصبح Approved عبر سير العمل الطبيعي.
- 72/72 من بنود BOQ مرتبطة بـ Work Item وWBS وCost Code وUOM وItem.
- Project Purchase Control Summary يعرض Item من صف BOQ عند عدم وجود Item على Work Item، لذلك أصبح مناسباً كأوضح شاشة للعميل.
- القرار النهائي: `PROJ-0002` جاهز للتسليم والعرض كقصة المرحلة الأولى.

## 9. تحديث Connections وGrid Views

تم تحسين تجربة التنقل داخل النماذج بحيث تظهر Connections مفيدة مثل شاشات ERPNext القياسية.

أهم ما تم تحسينه:

- Project `PROJ-0002` يعرض روابط BOQ وWork Items والمشتريات والمخزون والقياسات وIPC والمقاولين وCFO والعقار والحجوزات وعقود البيع.
- BOQ `BOQ-PROJ-0002-001` يعرض روابط Work Items وMaterial Requests وPurchase Orders وPurchase Receipts وPurchase Invoices وStock Entries وMeasurement Entries وIPCs.
- Sales Invoice `ACC-SINV-2026-00002` يعرض روابط Sales Contract وUnit Reservation وUnit وReal Estate Project من صف الفاتورة.
- Unit وReal Estate Project وSales Contract أصبحت تعرض روابط الحجز والبيع والفواتير المسودة بشكل أوضح.
- جداول BOQ Items وIPC Lines وInstallments وUnit Cost Allocation Lines أصبحت تعرض الأعمدة المهمة مباشرة في Grid View.

أثناء العرض، افتح Connections من الشريط الجانبي لإثبات أن المستندات ليست منفصلة، بل مترابطة عبر نفس المشروع والوحدة وبند العمل.

## 10. تحديث ربط Project بكل العلاقات المهمة

- شاشة Project `PROJ-0002` أصبحت نقطة الدخول التشغيلية الرئيسية، وليست مجرد تعريف مشروع.
- من Connections داخل Project يمكن فتح:
  - WBS Element للتخطيط.
  - Construction BOQ وConstruction Work Item وMeasurement Book وMeasurement Entry وInterim Payment Certificate.
  - Material Request وPurchase Order وPurchase Receipt وPurchase Invoice وStock Entry.
  - Contractor Account وContractor Ledger Entry وRetention Register وAdvance Register وGuarantee Register.
  - Project Financial Snapshot وProject Cash Flow Forecast وProject EVM Metrics.
  - Real Estate Project وBuilding وUnit وUnit Cost Allocation وUnit Reservation وSales Contract وSales Invoice المسودة.
- مسار العرض الموصى به الآن: ابدأ من Project `PROJ-0002`، افتح Connections لإظهار الترابط الكامل، ثم انتقل للتقارير التفصيلية عند شرح المخطط/الفعلي/المتبقي.

## 11. تحديث جدول BOQ داخل الشاشة

- جدول بنود `BOQ-PROJ-0002-001` أصبح يعرض الأعمدة المهمة مباشرة في Grid View:
  - Work Item.
  - Description.
  - Planned Qty.
  - Wastage %.
  - Expected Qty.
  - Actual Qty.
  - Remaining Qty.
  - Variance %.
  - Execution Status.
- حقل `Actual Qty` محسوب تلقائياً من أعلى كمية فعلية مرتبطة بالبند من المشتريات أو المخزون أو القياس أو الاعتماد.
- أثناء العرض، استخدم الجدول نفسه لإظهار:
  - المخطط: `Planned Qty`.
  - المتوقع بعد الهالك: `Expected Qty`.
  - الفعلي: `Actual Qty`.
  - المتبقي: `Remaining Qty`.
  - الانحراف: `Variance %` و`Execution Status`.
