# دليل عرض المنتج للعميل

## الملخص التنفيذي

النسخة الحالية من Real Estate Development ERP تثبت مساراً عملياً متكاملاً لإدارة تكلفة البناء وربطها بالمخزون العقاري والربحية، قبل الدخول في مراحل الحجز والبيع والتأجير.

النظام الحالي يوضح للعميل كيف تتحول الميزانية وجدول الكميات إلى بنود عمل، ثم إلى مشتريات ومخزون موقع، ثم قياسات ميدانية، ثم مستخلصات مقاول، ثم كشف مقاول ومحتجزات، ثم مؤشرات مالية وتنفيذية، ثم ربط التكلفة بالوحدات العقارية.

## قصة العرض

ابدأ بقصة واحدة مترابطة:

مشروع البرج السكني المتكامل هو مشروع تطوير عقاري تحت التنفيذ. تم إنشاء جدول كميات لأعمال الأساسات، وتحويله إلى بند عمل إنشائي. هذا البند تم ربطه بالمشتريات والمخزون، ثم تم قياس جزء من الأعمال ميدانياً، واعتماد مستخلص مقاول، ثم ظهرت الأرقام في كشف المقاول ولوحات المدير المالي. بعد ذلك تم إنشاء المخزون العقاري وتوزيع تكلفة المشروع على الوحدات لقراءة الربحية المتوقعة.

## الشاشات المقترحة بالترتيب

1. Executive Control Center

ما يثبته:
- وجود شاشة تنفيذية تجمع الملخص المالي، التدفق النقدي، مؤشرات القيمة المكتسبة، تعرضات المقاولين، وربحية الوحدات.
- الإدارة العليا لا تحتاج للتنقل بين كل المستندات التشغيلية لفهم وضع المشروع.

2. Construction Control -> Construction BOQ

افتح:
- ANK-BOQ-FOUNDATION-001

ما يثبته:
- جدول الكميات هو نقطة البداية لتخطيط التكلفة والكمية.
- البنود المعتمدة تتحول إلى Construction Work Item للتنفيذ والتتبع.

3. Construction Control -> Construction Work Item

افتح:
- CWI-2026-00001

ما يثبته:
- بند العمل هو الرابط التشغيلي بين التخطيط والمشتريات والقياسات والمستخلصات.
- تظهر عليه كميات المشتريات والقياسات والاعتماد بشكل منفصل.

4. Procurement & Site Warehouses

افتح التقارير:
- Work Item Procurement Summary
- BOQ Procurement Pipeline
- Site Warehouse Consumption

ما يثبته:
- طلب المواد وأمر الشراء وإيصال الشراء وفاتورة الشراء وقيد المخزون مرتبطة ببند العمل.
- يمكن قراءة الكمية المطلوبة والمطلوبة بالشراء والمستلمة والمفوترة والمستهلكة.

5. Measurement & IPC -> Measurement Book

افتح:
- MB-2026-00001

ما يثبته:
- القياس الميداني يأتي قبل المستخلص.
- القياسات يتم التحقق منها قبل أن تتحول إلى مستخلص مقاول.

6. Measurement & IPC -> Interim Payment Certificate

افتح:
- IPC-2026-00001

ما يثبته:
- المستخلص تم إنشاؤه من قياسات معتمدة، وليس إدخالاً يدوياً منفصلاً.
- certified_qty منفصلة عن measured_qty.
- فاتورة الشراء الناتجة تبقى مسودة حتى يكتمل مسار الاعتماد المالي.

7. Contractor Management

افتح:
- Contractor Account Statement
- Retention Register Report
- Contractor Exposure Summary
- Contractor Agreement Register
- Contractor Agreement Item Progress
- Contractor Agreement to IPC Traceability

ما يثبته:
- النظام يشرح المبلغ المعتمد، المحتجز، المفوتر، المدفوع، والمتبقي على المقاول.
- كشف المقاول طبقة تشغيلية للرقابة، ولا يستبدل دفتر الأستاذ العام في ERPNext.
- اتفاقية المقاول تربط نطاق التعاقد ببنود العمل، ثم بالقياسات والمستخلصات.

8. Executive Control Center -> Project Financial Snapshot

افتح:
- Project Financial Snapshot Report
- CFO Project Control Summary

ما يثبته:
- المدير المالي يرى الميزانية، الالتزامات، الفواتير، الاستهلاك، القياسات، المستخلصات، والمخاطر في مكان واحد.

9. Executive Control Center -> Cash Flow Forecast

افتح:
- Project Cash Flow Forecast Report
- Project Cash Requirement Summary

ما يثبته:
- توقع التدفق النقدي مبني على الالتزامات والفواتير والمستخلصات والمحتجزات الحالية.
- إيرادات البيع والتأجير غير مدخلة الآن لأنها ستأتي في مراحل لاحقة.

10. Executive Control Center -> EVM Metrics

افتح:
- Project EVM Metrics Report
- Project Performance Dashboard Report

ما يثبته:
- النظام يحسب BAC و EV و AC و PV و CPI و SPI و EAC و ETC و VAC بشكل قابل للشرح.
- لا يوجد تشغيل آلي ثقيل أو توقعات ذكية غير مبررة في هذه المرحلة.

11. Real Estate Inventory

افتح:
- Real Estate Project REP-2026-00001
- Unit Inventory Report
- Unit Availability Report

ما يثبته:
- المشروع العقاري يحتوي على مبنى وطوابق ووحدات.
- Unit كيان ثابت مستقل، ولا يحتوي على مستأجر.

12. Real Estate Inventory -> Unit Cost Allocation

افتح:
- UCA-2026-00001
- Unit Profitability Report
- Real Estate Project Profitability Summary

ما يثبته:
- تكلفة المشروع تم توزيعها على الوحدات بطريقة قابلة للمراجعة.
- تظهر تكلفة كل وحدة وسعر البيع المتوقع والهامش وحالة الربحية.

13. Reports & Analytics -> Financial Dimensions

افتح:
- GL Dimension Traceability
- Work Item Financial Ledger
- Unit Financial Ledger
- Project Unit Cost Matrix

ما يثبته:
- تم تفعيل الأبعاد المحاسبية لبند العمل وكود التكلفة والوحدة.
- القيود التاريخية السابقة لتفعيل الأبعاد لا يتم تعديلها أو ترحيلها من جديد.
- المعاملات المستقبلية ستحمل الأبعاد من خلال حقول ERPNext.

14. Sales & Rental -> Unit Reservation Foundation

افتح:
- Unit Reservation RES-2026-00001
- Unit A-101
- Active Unit Reservations
- Unit Reservation Impact

ما يثبته:
- الحجز موجود كطبقة تجارية مؤقتة قبل عقد البيع أو عقد التأجير.
- عند اعتماد الحجز، تتحول حالة الوحدة إلى Reserved.
- النظام يمنع وجود حجز نشط مكرر لنفس الوحدة.
- عند الإلغاء أو انتهاء الصلاحية، يتم تحرير الوحدة إلى Available فقط إذا كان ذلك آمناً.
- مبلغ الحجز في هذه المرحلة معلوماتي فقط ولا ينشئ فاتورة أو سند دفع أو قيد محاسبي.

ما لم يكن منفذاً في مرحلة الحجز فقط، وأصبح Sales Contract جاهزاً لاحقاً:
- Lease Contract.
- Collections.
- Commission.
- CRM Matching.
- Portal features.

## ما هو جاهز الآن

- تخطيط تكلفة البناء من خلال BOQ.
- تحويل BOQ إلى بنود عمل تشغيلية.
- ربط بنود العمل بالمشتريات والمخزون.
- قياسات ميدانية قابلة للتحقق.
- توليد مستخلصات مقاول من القياسات.
- كشف مقاول ومحتجزات وضمانات.
- ملخص مالي للمدير المالي.
- توقع تدفق نقدي مبني على معاملات حالية.
- مؤشرات قيمة مكتسبة.
- مخزون عقاري من مشروع ومباني وطوابق ووحدات.
- توزيع تكلفة الوحدات وربحية الوحدات.
- أبعاد محاسبية للتتبع المالي المستقبلي.
- حجز وحدة عقارية مع منع الحجز المكرر وتحديث حالة الوحدة.
- تجربة تنقل ثنائية اللغة عبر مصدر إنجليزي وترجمة عربية.

## تحديث تقارير العرض والمؤشرات

تم تحسين تقارير العرض التنفيذية بإضافة بطاقات ملخص أعلى التقارير ومؤشرات لونية للحالات والمخاطر.

أثناء العرض استخدم الترتيب التالي بعد فتح Executive Presentation Center:

1. Project Purchase Control Summary لشرح المخطط والمتوقع والفعلي والمتبقي.
2. Work Item Procurement Summary لشرح المشتريات والمخزون.
3. IPC Register لشرح المستخلصات والمدفوع والمتبقي.
4. Contractor Exposure Summary لشرح تعرض المقاولين.
5. Project Financial Snapshot Report لشرح الصورة المالية.
6. Project Cash Flow Forecast Report لشرح التدفق النقدي.
7. Project EVM Metrics Report لشرح الأداء.
8. Unit Profitability Report لشرح ربحية الوحدات.
9. Unit Reservation Impact لشرح أثر الحجوزات.
10. Sales Collection Report وSales Invoice from Installments Report لشرح أساس البيع والفوترة المسودة.

اشرح الألوان ببساطة:

- أخضر: طبيعي أو ضمن المسار.
- برتقالي: يحتاج متابعة أو مدفوع/مفوتر جزئياً.
- أحمر: تجاوز أو خطر أو متأخر.
- رمادي: مسودة أو لم يبدأ أو مؤجل.

## Presentation UX and Dashboard Flow

ابدأ العرض من:

- Executive Presentation Center

هذه الشاشة هي المدخل الأفضل للعميل لأنها تجمع القصة الكاملة في مسار واحد: من تكلفة البناء إلى الربحية والحجز والتتبع المالي.

### قصة العرض في 10 شاشات

1. Executive Presentation Center
ما تقوله للعميل:
هذه هي لوحة العرض التنفيذية. الأرقام في الأعلى تلخص الميزانية، الالتزامات، المستخلصات، مخاطر التدفق النقدي، الوحدات، والربحية المتوقعة. كل رقم يقود إلى تقرير تفصيلي.

2. Project Overview
افتح:
- Project Financial Snapshot
- Project Financial Snapshot Report
ما تقوله:
هذه الشاشة تربط الميزانية والمشتريات والقياسات والمستخلصات والمحتجزات في ملخص مالي واحد للمشروع.

3. Construction Cost Control
افتح:
- Construction BOQ
- Construction Work Item
- Construction BOQ Cost Analysis
ما تقوله:
هنا يبدأ التحكم. جدول الكميات يحدد نطاق العمل، ثم يتحول إلى بنود عمل تشغيلية يمكن تتبعها في كل مرحلة لاحقة.

4. Procurement & Site Consumption
افتح:
- Work Item Procurement Summary
- BOQ Procurement Pipeline
- Site Warehouse Consumption
ما تقوله:
كل طلب شراء أو أمر شراء أو استلام أو استهلاك يمكن ربطه ببند العمل وكود التكلفة، وهذا يمنع فقدان أثر التكلفة.

5. Measurement & IPC
افتح:
- Measurement Book
- Interim Payment Certificate
- Measurement to IPC Traceability
ما تقوله:
القياسات تأتي قبل المستخلص. لا يتم إنشاء مستخلص المقاول من فراغ، بل من قياسات معتمدة ومتحقق منها.

6. Contractor Ledger
افتح:
- Contractor Account
- Contractor Account Statement
- Retention Register Report
ما تقوله:
هذه طبقة رقابة على المقاول تعرض المعتمد والمحتجز والمدفوع والمستحق دون أن تستبدل محاسبة ERPNext.

7. CFO Snapshot
افتح:
- CFO Project Control Summary
- Contractor Financial Exposure
ما تقوله:
هنا يرى المدير المالي صورة المشروع: الالتزامات، الفواتير، المستخلصات، المحتجزات، والتعرض المالي للمقاولين.

8. Cash Flow and EVM
افتح:
- Project Cash Flow Forecast Report
- Project EVM Metrics Report
- EVM Forecast Summary
ما تقوله:
التدفق النقدي يوضح الاحتياجات القادمة، ومؤشرات القيمة المكتسبة تشرح هل الأداء المالي والزمني يسير كما هو متوقع.

9. Real Estate Inventory
افتح:
- Real Estate Project
- Unit Inventory Report
- Unit Availability Report
ما تقوله:
الوحدة العقارية كيان ثابت مستقل. لا نخزن المستأجر داخل الوحدة؛ عقود البيع والتأجير ستأتي لاحقاً وتربط العميل أو المستأجر بالوحدة.

10. Unit Profitability and Reservation
افتح:
- Unit Cost Allocation
- Unit Profitability Report
- Unit Reservation
- Unit Reservation Impact
ما تقوله:
تكلفة المشروع موزعة على الوحدات، والهامش المتوقع ظاهر لكل وحدة. الحجز يحمي الوحدة مؤقتاً قبل عقد البيع أو التأجير ولا ينشئ قيوداً محاسبية.

### الجاهز الآن في العرض

- مسار تنفيذي واضح من BOQ إلى الربحية.
- بطاقات KPI تنفيذية للعرض السريع.
- تقارير تفصيلية خلف كل رقم.
- واجهة ثنائية اللغة عبر ترجمة عربية منظمة.
- حجز الوحدة كأول خطوة تجارية قبل العقود.

### التالي بعد العرض

- مراجعة جاهزية تجربة العرض مع أصحاب المصلحة.
- البدء في Sales Contract و Installment Plan foundation بعد اعتماد تجربة الحجز والعرض التنفيذي.

## Form and Workspace UX Completion

### كيف تتنقل في المساحات الجديدة

ابدأ دائماً من Executive Presentation Center عند العرض التنفيذي، لأنه يرتب الرحلة من الأعلى إلى الأسفل:

1. Executive Overview.
2. Project Financial Control.
3. Construction Cost Control.
4. Procurement & Site Warehouses.
5. Measurement & IPC.
6. Contractor Financial Control.
7. CFO Forecasting.
8. Real Estate Inventory.
9. Unit Profitability.
10. Unit Reservation.
11. Deep Financial Traceability.

بعد ذلك انتقل إلى المساحة المتخصصة عند الحاجة:

- Construction Control لشرح BOQ و Work Items.
- Procurement & Site Warehouses لشرح الشراء والمخزون.
- Measurement & IPC لشرح القياسات والمستخلصات.
- Contractor Management لشرح المقاولين والمحتجزات.
- Real Estate Inventory لشرح المشروع العقاري والوحدات.
- Sales & Rental لشرح أن الحجز جاهز وأن العقود والأقساط تأتي لاحقاً.
- Reports & Analytics لعرض كل التقارير مجمعة حسب الوظيفة.

### كيف تشرح النماذج للعميل

- ابدأ من القسم الأول في كل نموذج لأنه يحتوي البيانات الأساسية.
- انتقل إلى الأقسام المالية أو التشغيلية حسب موضوع الشاشة.
- وضّح أن الحقول المحسوبة مثل totals و progress و risk indicators تُحدّث تلقائياً من المستندات المرتبطة.
- في Unit، اشرح أن الوحدة كيان ثابت وأن المستأجر غير مخزن داخلها.
- في Unit Reservation، اشرح أن الحجز مؤقت ولا ينشئ فاتورة أو سند دفع.

### ما يجب عرضه لكل مسار

- BOQ: Construction BOQ ثم Construction Work Item ثم Construction BOQ Cost Analysis.
- Procurement: Work Item Procurement Summary ثم BOQ Procurement Pipeline ثم Site Warehouse Consumption.
- Measurement: Measurement Book ثم Measurement Entry ثم Work Item Measurement Progress.
- IPC: Interim Payment Certificate ثم Measurement to IPC Traceability ثم IPC Register.
- Contractor: Contractor Account ثم Contractor Account Statement ثم Retention Register Report.
- CFO: Project Financial Snapshot Report ثم Cash Flow Forecast ثم EVM Metrics.
- Real Estate: Real Estate Project ثم Unit Inventory Report ثم Unit Availability Report.
- Profitability: Unit Cost Allocation ثم Unit Profitability Report.
- Reservation: Unit Reservation ثم Active Unit Reservations ثم Unit Reservation Impact.

### ما لا يجب تقديمه كمنجز

- Lease Contract.
- Rent Schedule.
- Collections.
- CRM Matching.
- Portal features.

## ما لم يتم تنفيذه عمداً بعد

- Lease Contract.
- Collections.
- Commission.
- CRM Matching.
- Portal features.

## التموضع الصادق أمام العميل

هذه المرحلة تثبت أساس التحكم في تكلفة البناء وربطها بالمخزون العقاري وربحية الوحدات، وتضيف الحجز ثم عقد البيع وجدول الأقساط كطبقة تشغيلية غير محاسبية. النظام جاهز لشرح رحلة التكلفة والقياس والمستخلصات والتحليلات المالية والحجز وعقد البيع، لكنه لم يدخل بعد في فواتير البيع والتحصيل أو عقود التأجير.

## المخاطر والحدود المعروفة

- قيود GL التاريخية التي أُنشئت قبل تفعيل Accounting Dimensions لا تحتوي على أبعاد جديدة، ولم يتم تعديلها أو إعادة ترحيلها.
- بعد Unit في GL يحتاج إلى معاملات حقيقية خاصة بالوحدة في مراحل البيع أو التأجير أو تكلفة مخصصة للوحدة.
- فاتورة الشراء الناتجة من IPC تبقى مسودة إذا لم يكتمل مسار Invoice Authorization.
- مؤشرات CFO و EVM الحالية حتمية وقابلة للشرح، لكنها تحتاج اعتماد حدود المخاطر من الإدارة المالية قبل التشغيل النهائي.
- حجز A-101 نشط ومقصود للعرض؛ يجب أخذه في الاعتبار عند تجربة سيناريوهات حجز أخرى.
- إلغاء الحجز من حالة Draft لا يتم عبر Workflow لأن Frappe v15 لا يسمح بالإلغاء قبل الاعتماد؛ يمكن تعديل أو حذف الحجز المسودة بصلاحياته الطبيعية.

## الخلاصة

يمكن عرض المنتج بثقة كمنصة تنفيذية وتشغيلية للتحكم في تكلفة البناء والمقاولين وربحية المخزون العقاري وحجز الوحدات. بعد هذا العرض، الخطوة المنطقية التالية هي مراجعة جاهزية الحجز ثم البدء في Sales Contract foundation.

## Final UX Hardening Route

بعد تقوية النماذج ومساحات العمل، استخدم هذا المسار المختصر في العرض:

1. Executive Presentation Center
   - اعرض بطاقات KPI أولاً: BOQ Total، Committed Amount، Certified Amount، Net Payable، Retention Held، Contractor Outstanding، Cash Flow Risk، EVM CPI/SPI، Total Units، Available Units، Reserved Units، Expected Gross Margin.
   - اشرح أن هذه بطاقات قراءة فقط مبنية على بيانات موجودة ولا تنشئ قيوداً أو مستندات.

2. End-to-End Flow
   - افتح الروابط بالترتيب: Construction BOQ، Construction Work Item، Measurement Book، Interim Payment Certificate، Unit، Unit Reservation.
   - الهدف هو إثبات أن النظام يربط التخطيط والتنفيذ والقياس والمستخلص والمخزون العقاري والحجز.

3. Construction Work Item
   - استخدم التبويبات الجديدة لشرح Planned Scope، Procurement Tracking، Measurement Tracking، Certification Tracking، Financial Summary.

4. Interim Payment Certificate
   - استخدم التبويبات الجديدة لشرح مصدر القياس، بنود المستخلص، الملخص المالي، الفاتورة/السداد، وسير الاعتماد.

5. Unit
   - استخدم التبويبات الجديدة لشرح التسلسل المكاني، التفاصيل المادية، الحالة، التوقعات المالية، توزيع التكلفة والربحية.

6. Unit Reservation
   - استخدم التبويبات الجديدة لشرح بيانات الحجز، بيانات الوحدة، بيانات العميل أو المهتم، البيانات التجارية، ومراجع التحويل المستقبلية.

### ملاحظات العرض

- الترجمة العربية أصبحت أوسع وتشمل وصف الحقول المهمة، لكن يفضل إجراء click-through سريع بحساب مستخدم عربي قبل اجتماع العميل.
- Dashboard Charts ما زالت مؤجلة، لذلك اعتمد على بطاقات KPI والتقارير التفصيلية.
- Sales Contract + Installment foundation أصبح جاهزاً الآن؛ لا تعرض Sales Invoice أو Collections أو Lease Contract أو Rent Schedule كميزات مكتملة.

## Sales Contract + Installment Foundation

### ما الذي أصبح جاهزاً

- يمكن الآن تحويل الحجز إلى عقد بيع تشغيلي.
- عقد البيع يحتوي على جدول أقساط داخلي، بدون إنشاء فاتورة بيع أو سند قبض.
- عند اعتماد العقد ووصوله إلى الحالة Active، تتحول الوحدة إلى Sold ويتحول الحجز إلى Converted.
- النظام يمنع وجود عقد بيع نشط آخر لنفس الوحدة.
- التقارير الجديدة تعرض سجل عقود البيع، جدول الأقساط، خط مبيعات الوحدات، ملخص قيمة المبيعات، والتحويل من الحجز للبيع.

### شاشة العرض المقترحة

1. افتح Sales & Rental.
2. افتح Unit Reservation لشرح أن الحجز هو مرحلة مؤقتة.
3. افتح Sales Contract SC-2026-00001.
4. اعرض تبويب Installment Plan ووضح الأقساط الأربعة:
   - دفعة مقدمة.
   - الدفعة الثانية.
   - دفعة الاستلام.
   - الدفعة النهائية.
5. افتح Unit A-101 ووضح أن الحالة أصبحت Sold.
6. افتح Reserved to Sold Conversion Report لإثبات أثر التحويل.

### ما لم يتم تنفيذه بعد

- Sales Invoice.
- Payment Entry / Collections.
- Lease Contract.
- Rent Schedule.
- Commission.
- CRM Matching.
- Portal.

## Sales Contract Readiness Review

### نتيجة المراجعة

تمت مراجعة عقد البيع `SC-2026-00001` قبل الانتقال إلى فواتير البيع والتحصيل. العقد نشط، الوحدة `A-101` أصبحت Sold، والحجز `RES-2026-00001` أصبح Converted، وجدول الأقساط مكون من أربع دفعات بإجمالي `1,200,000` مطابق لصافي قيمة العقد.

### ما يمكن قوله للعميل

- عقد البيع يثبت التحويل التجاري من حجز إلى بيع.
- هذه المرحلة لا تنشئ فاتورة بيع ولا سند قبض ولا قيد يومية.
- الأقساط حالياً جدول تشغيلي للعقد، وسيتم ربطها لاحقاً بفواتير البيع والتحصيلات.
- بعد الوحدة جاهز محاسبياً بحيث ينتقل لاحقاً إلى Sales Invoice Item ثم GL عند تنفيذ الفواتير.

### ما يأتي بعد ذلك

- تصميم Sales Invoice من الأقساط.
- تصميم Collections عبر Payment Entry.
- تحديث حالة الأقساط حسب الفواتير والتحصيل.
- ربط تقارير العملاء والمستحقات بالوحدات والعقود.

## Sales Invoice and Collections Foundation

### ما الذي أصبح جاهزاً

- يمكن الآن إنشاء فاتورة بيع مسودة من قسط أو أكثر داخل عقد البيع.
- فاتورة البيع ترتبط بعقد البيع وبالقسط وبالوحدة العقارية.
- بعد الوحدة ينتقل إلى بند فاتورة البيع حتى يصبح جاهزاً للتتبع المحاسبي عند ترحيل الفاتورة مستقبلاً.
- النظام يمنع إنشاء فاتورة نشطة مكررة لنفس القسط.
- تقارير التحصيل تعرض قيمة العقود، المفوتر، المحصل، المتبقي، والأقساط المتأخرة.

### شاشة العرض المقترحة

1. افتح Sales Contract `SC-2026-00001`.
2. اعرض جدول الأقساط ووضح أن أول قسط مرتبط بفاتورة `ACC-SINV-2026-00001`.
3. افتح Sales Invoice `ACC-SINV-2026-00001` ووضح أنها Draft.
4. اعرض بند الفاتورة ووضح أن الوحدة `A-101` والمشروع وعقد البيع انتقلت إلى البند.
5. افتح Sales Collection Report لعرض المفوتر `300,000`، المحصل `0`، والمتبقي `300,000`.
6. افتح Unit Revenue Report لإثبات رؤية الإيراد حسب الوحدة.

### ما يجب توضيحه للعميل

- هذه المرحلة لا ترحل الفاتورة تلقائياً ولا تنشئ سند قبض تلقائياً.
- Payment Entry سيبقى مستند التحصيل الرسمي في ERPNext.
- عند ترحيل فاتورة البيع لاحقاً عبر الضوابط الطبيعية، ستصبح الوحدة بعداً محاسبياً قابلاً للتتبع في GL.
- Lease Contract وRent Schedule والعمولات والبوابة ما زالت مراحل لاحقة.

### ملاحظة جاهزية CMD-24

تم إيقاف الانتقال إلى Lease Contract مؤقتاً لأن مراجعة الجاهزية الحية لفواتير البيع والتحصيل لم تكتمل بسبب توقف MariaDB على الخادم بحالة `oom-kill`. يجب استعادة قاعدة البيانات وإعادة اختبار الفاتورة المسودة والتقارير والبطاقات قبل عرض هذا الجزء كجاهز نهائياً.

## Lease Contract and Rent Schedule Foundation

### ما الذي أصبح جاهزاً

- يمكن الآن تحويل حجز إيجار إلى عقد إيجار تشغيلي.
- المستأجر موجود داخل عقد الإيجار كعميل/طرف، وليس داخل الوحدة.
- عقد الإيجار يحتوي على جدول إيجار شهري تشغيلي.
- عند اعتماد/تفعيل عقد الإيجار، تتحول الوحدة إلى Rented ويتحول الحجز إلى Converted.
- النظام يمنع وجود عقد إيجار نشط آخر لنفس الوحدة.
- هذه المرحلة لا تنشئ فاتورة إيجار ولا سند قبض ولا قيد يومية.

### شاشة العرض المقترحة

1. افتح Sales & Rental.
2. افتح Lease Contract `LC-2026-00001`.
3. اعرض تبويب Unit Details ووضح أن الوحدة هي `A-G01`.
4. اعرض تبويب Tenant Details ووضح أن المستأجر محفوظ في العقد وليس في الوحدة.
5. اعرض تبويب Rent Schedule ووضح وجود 12 قسط إيجار شهري بإجمالي `4,200,000`.
6. افتح Unit `A-G01` ووضح أن الحالة أصبحت Rented.
7. افتح Reservation `RES-2026-00005` ووضح أنه أصبح Converted.
8. افتح Rental Value Summary أو Active Leases Report لعرض أثر التأجير.

### ما يجب توضيحه للعميل

- عقد الإيجار هو طبقة تشغيلية قبل الفوترة والتحصيل.
- Rent Schedule لا يعني أن هناك فاتورة أو ذمة مدينة تم إنشاؤها.
- Rent Invoice وPayment Entry سيتم تصميمهما في المرحلة القادمة باستخدام ERPNext Sales Invoice وPayment Entry.
- لا يوجد Tenant field على Unit، وهذا قرار معماري مقصود حتى تبقى الوحدة أصل/مخزون مستقر.

## Lease Contract Readiness Review

### نتيجة المراجعة

تمت مراجعة عقد الإيجار `LC-2026-00001` قبل الانتقال إلى فواتير الإيجار والتحصيل. العقد نشط، الوحدة `A-G01` أصبحت `Rented`، والحجز `RES-2026-00005` أصبح `Converted`، وجدول الإيجار يحتوي على 12 صفاً شهرياً بإجمالي `4,200,000` مطابق لإجمالي قيمة العقد.

### ما يمكن قوله للعميل

- عقد الإيجار يثبت التحويل التجاري من حجز إيجار إلى عقد إيجار نشط.
- المستأجر محفوظ داخل عقد الإيجار، وليس داخل الوحدة.
- جدول الإيجار تشغيلي فقط حالياً ولا ينشئ فاتورة أو سند قبض.
- بعد الوحدة جاهز للانتقال لاحقاً إلى Sales Invoice Item ثم GL عند تنفيذ Rent Invoice وCollections.

### ما يأتي بعد ذلك

- إنشاء Rent Invoice من صفوف Rent Schedule.
- ربط التحصيل عبر Payment Entry.
- تحديث حالة صفوف الإيجار حسب الفواتير والتحصيل.
- تقارير تحصيل الإيجارات والمتأخرات وربط الإيراد بالوحدة.

## Phase 1 Client Presentation Closure

### المسار المختصر النهائي للعرض

1. Executive Presentation Center.
2. Construction BOQ.
3. Construction Work Item.
4. Procurement reports.
5. Measurement Book.
6. Interim Payment Certificate.
7. Contractor Account and Retention reports.
8. Project Financial Snapshot.
9. Project Cash Flow Forecast.
10. Project EVM Metrics.
11. Real Estate Project and Unit.
12. Unit Cost Allocation and Unit Profitability Report.
13. GL Dimension Traceability and Project Unit Cost Matrix.
14. Unit Reservation.
15. Sales Contract and Installment Schedule.
16. Draft Sales Invoice from installment.
17. Phase 2 roadmap.

### ما يجب تأكيده أثناء العرض

- Phase 1 تثبت التحكم في تكلفة البناء وربطها بالمخزون العقاري والربحية وبداية البيع.
- فاتورة البيع المعروضة مسودة فقط ولا توجد قيود GL أو سندات قبض.
- روابط Lease/Rent الموجودة في بعض المساحات موسومة كـ Phase 2 / Upcoming ولا يتم تقديمها كدورة مكتملة.
- التحصيل الكامل، التأجير الكامل، CRM، Matching، Portal، WhatsApp، والعمولات مؤجلة إلى Phase 2.

### الجملة الختامية المقترحة

هذه المرحلة تقدم أساساً تنفيذياً وتشغيلياً واضحاً من جدول الكميات حتى فاتورة بيع مسودة مرتبطة بوحدة وقسط، والهدف من اجتماع العميل هو جمع الملاحظات قبل تخطيط Phase 2.

## Recommended Records to Open During Presentation

### 1. Executive overview

- Workspace: Executive Presentation Center.
- Projects:
  - `PROJ-0001` — مشروع البرج السكني المتكامل.
  - `PROJ-0002` — مشروع برج الياسمين السكني.
  - `PROJ-0003` — مشروع الواجهة التجارية المركزية.
  - `PROJ-0004` — مجمع النور المختلط الاستخدام.
- Reports:
  - Project Financial Snapshot Report.
  - Project Cash Flow Forecast Report.
  - Project EVM Metrics Report.

### 2. BOQ

- `ANK-BOQ-FOUNDATION-001` — BOQ معتمد للمسار الكامل.
- `BOQ-PROJ-0002-001` — BOQ غني للبنود والكميات والتكاليف.
- `BOQ-PROJ-0003-001` — BOQ غني لمشروع تجاري.
- `BOQ-PROJ-0004-001` — BOQ غني لمشروع مختلط الاستخدام.
- Report: Construction BOQ Cost Analysis.

### 3. Procurement

- Material Requests: `MAT-MR-2026-00001` إلى `MAT-MR-2026-00050`.
- العرض الأفضل حالياً: Work Item Procurement Summary وBOQ Procurement Pipeline.
- يوجد مثال قديم/محدود لمسار مكتمل:
  - Purchase Order: `PUR-ORD-2026-00003`.
  - Purchase Receipt: `MAT-PRE-2026-00001`.
  - Purchase Invoice: `ACC-PINV-2026-00001`.
  - Stock Entry: `MAT-STE-2026-00001`.
- يجب توضيح أن بيانات العرض الجديدة لا تحتوي مسار PO/PR/PI/Stock كامل لكل مشروع.

### 4. Measurement

- Measurement Book: `MB-2026-00001` — Verified.
- Measurement Entry: `ME-2026-00001` linked to `CWI-2026-00001`.
- Measurement Books إضافية للعرض العام:
  - `MB-2026-00002`.
  - `MB-2026-00003`.
  - `MB-2026-00004`.
- Report: Measurement to IPC Traceability.

### 5. IPC

- Interim Payment Certificate: `IPC-2026-00001`.
- Draft Purchase Invoice from IPC: `ACC-PINV-2026-00002`.
- Report: IPC Register.
- يجب توضيح أن المثال التشغيلي الكامل للـ IPC موجود في مشروع `PROJ-0001` فقط.

### 6. Contractor

- Contractor Accounts:
  - `CA-2026-00001` — يظهر رصيداً قائماً `787,500`.
  - `CA-2026-00002`, `CA-2026-00003`, `CA-2026-00004` — حسابات جاهزة للمشاريع الأخرى.
- Retention Register: `RET-2026-00001`.
- Reports:
  - Contractor Account Statement.
  - Contractor Exposure Summary.
  - Retention Register Report.

### 7. CFO

- Financial Snapshots:
  - `PFS-2026-00001` — At Risk.
  - `PFS-2026-00002`, `PFS-2026-00003`, `PFS-2026-00004` — On Track.
- Cash Flow Forecasts:
  - `PCF-2026-00001` — Red.
  - `PCF-2026-00002`, `PCF-2026-00003`, `PCF-2026-00004` — Green.
- EVM Metrics:
  - `EVM-2026-00001` — At Risk.
  - `EVM-2026-00002`, `EVM-2026-00003`, `EVM-2026-00004` — On Track.

### 8. Real Estate Inventory

- Real Estate Projects:
  - `REP-2026-00001` linked to `PROJ-0001`.
  - `REP-2026-00002` linked to `PROJ-0002`.
  - `REP-2026-00003` linked to `PROJ-0003`.
  - `REP-2026-00004` linked to `PROJ-0004`.
- Buildings:
  - `A`.
  - `BLD-PROJ-000-001`.
  - `BLD-PROJ-000-002`.
  - `BLD-PROJ-000-003`.
- Unit status distribution: Available `22`, Reserved `8`, Sold `10`, Rented `3`.

### 9. Unit Profitability

- Unit Cost Allocations:
  - `UCA-2026-00001` — Applied.
  - `UCA-2026-00002`, `UCA-2026-00003`, `UCA-2026-00004` — Calculated.
- Reports:
  - Unit Profitability Report.
  - Real Estate Project Profitability Summary.
  - Building Profitability Summary.

### 10. Reservation

- Converted sale reservation: `RES-2026-00001` for Unit `A-101`.
- Converted rent reservation: `RES-2026-00005` for Unit `A-G01`، يذكر كجزء مؤجل/Phase 2 إذا ظهر.
- Draft presentation reservations:
  - `RES-BLD-PROJ-000-00-001` to `RES-BLD-PROJ-000-00-010`.
- Reports:
  - Unit Reservation Register.
  - Active Unit Reservations.
  - Unit Reservation Impact.

### 11. Sales Contract

- Sales Contract: `SC-2026-00001`.
- Unit: `A-101`.
- Customer: عميل مهتم بشراء وحدة سكنية.
- Net price: `1,200,000`.
- Installments: 4 rows of `300,000` each.
- First installment is linked to draft Sales Invoice `ACC-SINV-2026-00001`.

### 12. Draft Sales Invoice

- Draft Sales Invoice: `ACC-SINV-2026-00001`.
- Amount: `300,000`.
- Status: Draft.
- Invoice item carries:
  - Unit: `A-101`.
  - Project: `PROJ-0001`.
  - Sales Contract: `SC-2026-00001`.
  - Real Estate Project: `REP-2026-00001`.
  - Unit Reservation: `RES-2026-00001`.
- يجب التأكيد أن الفاتورة غير مرحّلة ولا يوجد Payment Entry أو GL Entry من مسار البيع في هذه المرحلة.

## PROJ-0002 Presentation Route — المسار الرئيسي الجديد

يفضل في العرض القادم استخدام `PROJ-0002` كقصة واحدة متصلة:

1. Executive Presentation Center: ابدأ بالنظرة التنفيذية وقل إن `PROJ-0002` هو مشروع العرض الرئيسي.
2. BOQ: افتح `BOQ-PROJ-0002-001` واشرح أن البنود أصبحت مرتبطة بـ72 Work Items، وأن شاشة BOQ تحتوي الآن على ملخص تنفيذ وقيم فعلية ومتبيقة وانحرافات.
3. Purchase Control: افتح Project Purchase Control Summary وفلتر على `PROJ-0002` لشرح Planned / Expected / Actual / Remaining / Variance في شاشة واحدة.
4. Procurement: افتح Work Item Procurement Summary وBOQ Procurement Pipeline لشرح المخطط، المطلوب، المطلوب شراؤه، المستلم، المفوتر، المستهلك، والمتبقي.
5. Measurement: افتح `MB-2026-00005` إلى `MB-2026-00008` لشرح قياسات الأساسات والهيكل والتشطيبات والدهانات.
6. IPC: افتح `IPC-2026-00002` إلى `IPC-2026-00005` لشرح Current / Previous / Remaining والاحتجاز وصافي المستحق.
7. Contractor: افتح Contractor Account Statement وContractor Exposure Summary لشرح رصيد المقاول والاحتجاز.
8. CFO: افتح `PFS-2026-00002`, `PCF-2026-00002`, `EVM-2026-00002`.
9. Real Estate Inventory: افتح `REP-2026-00002` وUnit Inventory Report.
10. Unit Profitability: افتح `UCA-2026-00005`, Unit Profitability Report, Project Unit Cost Matrix.
11. Reservation: افتح `RES-PROJ-0002-001` إلى `RES-PROJ-0002-010` لشرح Reserved / Converted / Expired / Cancelled.
12. Sales Contract: افتح `SC-PROJ-0002-001`, `SC-PROJ-0002-002`, `SC-PROJ-0002-003`.
13. Draft Sales Invoice: افتح `ACC-SINV-2026-00002`, `ACC-SINV-2026-00003`, `ACC-SINV-2026-00004`.

نقطة مهمة للعميل: لا توجد Payment Entries أو Journal Entries، ولا توجد Sales Invoice submitted. الهدف هو عرض foundation متصل وقابل للفهم قبل مرحلة التحصيل والترحيل الكامل.
## تحديث نهائي لمسار PROJ-0002 - جاهزية التسليم

استخدم `PROJ-0002` كسيناريو العرض الرئيسي للمرحلة الأولى.

المسار النهائي:

1. افتح Executive Presentation Center لعرض الصورة العامة.
2. افتح مؤشرات وتقارير `PROJ-0002` المالية.
3. افتح `BOQ-PROJ-0002-001`، وهو الآن Approved، واشرح أن BOQ هو نقطة التخطيط المعتمدة.
4. افتح Project Purchase Control Summary مع فلتر `PROJ-0002` لشرح المخطط والمتوقع والفعلي والمتبقي والانحراف.
5. افتح أمثلة عناصر العمل:
   - `CWI-2026-00008`: حديد التسليح، حالة طبيعية ومعتمدة.
   - `CWI-2026-00006`: خرسانة الأسقف، مثال تجاوز.
   - `CWI-2026-00003`: أعمال الردم والتسوية، مثال تنفيذ جزئي ومتبقي.
6. افتح Measurement Books من `MB-2026-00005` إلى `MB-2026-00008`.
7. افتح IPCs من `IPC-2026-00002` إلى `IPC-2026-00005`.
8. افتح Contractor Exposure Summary وContractor Account Statement.
9. افتح تقارير CFO: Financial Snapshot وCash Flow وEVM.
10. افتح `REP-2026-00002` والوحدات.
11. افتح `UCA-2026-00005` وتقارير ربحية الوحدات.
12. افتح الحجوزات وعقود البيع وفواتير البيع المسودة.
13. اختم بخارطة المرحلة الثانية.

ملاحظة مهمة: فواتير البيع ما زالت مسودة، ولا توجد Payment Entry أو Journal Entry أو GL backfill ضمن المرحلة الأولى.

## تحديث CMD-27 - فوترة وتحصيل مبيعات فعلي جزئي

أصبح بإمكان العرض إظهار سيناريو تحصيل مبيعات فعلي واحد على `PROJ-0002`:

- افتح `ACC-SINV-2026-00002`: فاتورة مبيعات مرحلة ومرتبطة بعقد البيع `SC-PROJ-0002-001`.
- وضّح أن الفاتورة تحمل Unit dimension للوحدة `BLD-PROJ-000-001-S-01-03`.
- افتح `ACC-PAY-2026-00010`: سند قبض جزئي بمبلغ `1,210,000.00`.
- افتح Buyer Statement لعرض الفاتورة والتحصيل.
- افتح Sales Installment Collection Status لعرض حالة القسط `Partially Paid`.
- افتح GL Dimension Traceability أو Unit Financial Ledger لشرح أن GL يحمل بُعد الوحدة.

ملاحظة العرض: تم ترحيل فاتورة واحدة فقط وإنشاء سند قبض واحد فقط لغرض التحقق. باقي فواتير المبيعات في PROJ-0002 ما زالت مسودة حتى يعتمد الفريق المالي سياسة الترحيل الكامل.

## تحديث UX Connections وGrid Views

أثناء عرض `PROJ-0002`، استخدم Connections في يمين النماذج لإظهار الترابط:

- من Project `PROJ-0002`: افتح الروابط إلى BOQ، Work Items، Material Requests، IPCs، Contractor Accounts، Real Estate Project، Reservations، Sales Contracts، وSales Invoices.
- من `BOQ-PROJ-0002-001`: افتح Connections إلى Work Items والمشتريات والقياسات وIPCs.
- من `CWI-2026-00006`: أظهر كيف تظهر روابط Material Request وMeasurement Entry وIPC لهذا البند.
- من `IPC-2026-00002`: أظهر Measurement Entries وContractor Ledger وRetention.
- من `REP-2026-00002` أو Unit: أظهر الحجوزات وعقود البيع وفواتير البيع المسودة.

الجداول الداخلية أصبحت أوضح:

- BOQ Items تعرض WBS وCost Code وItem والكميات المخططة والمطلوبة والمستلمة والمستهلكة والمقاسة والمعتمدة والمتبقية والانحراف.
- Sales Installment Schedule تعرض القسط والتاريخ والمبلغ والفاتورة والمسدد والمتبقي.
- IPC Lines تعرض بند العمل والكميات السابقة والحالية والإجمالية والمتبقي والمبالغ والاحتجاز.
- Unit Cost Allocation Lines تعرض الوحدة والمساحة والنسبة والمبلغ والهامش وحالة الربحية.

## تحديث فوترة وتحصيل الإيجارات

أصبح بالإمكان عرض مسار إيجار مالي محدود ومثبت على عقد الإيجار المحتفظ به:

- افتح `LC-2026-00001` لعرض عقد الإيجار وجدول الإيجار.
- افتح `ACC-SINV-2026-00005`: فاتورة إيجار مرحلة بمبلغ `350,000.00`.
- وضّح أن بند الفاتورة يحمل Unit dimension للوحدة `A-G01`.
- افتح `ACC-PAY-2026-00011`: سند قبض إيجار جزئي بمبلغ `175,000.00`.
- افتح Tenant Statement لعرض الفاتورة والتحصيل.
- افتح Rent Collection Report وLease Collection Summary لعرض حالة `Partially Collected`.
- افتح GL Dimension Traceability عند الحاجة لتوضيح أن فاتورة الإيجار المرحلة تحمل بُعد الوحدة.

ملاحظة العرض: تم ترحيل فاتورة إيجار واحدة وإنشاء سند قبض واحد لغرض التحقق فقط. لا يتم ترحيل كل جدول الإيجار تلقائياً إلا بعد اعتماد سياسة التشغيل المالي.
