# مراجعة جاهزية فواتير البيع والتحصيل قبل عقود التأجير

التاريخ: 2026-05-10
الموقع: construction.yemenfrappe.com
الفرع: feature/sales-invoice-collections-readiness-review
الأمر: CMD-24 - Sales Invoice and Collections Readiness Review

## 1. الملخص التنفيذي

تم بدء مراجعة جاهزية Sales Invoice and Collections بعد إكمال أساس فواتير البيع والتحصيل في CMD-23.

النتيجة التنفيذية: المراجعة لا يمكن اعتمادها كناجحة حالياً لأن قاعدة البيانات MariaDB على الخادم موقوفة بحالة `oom-kill` وترفض الاتصال على `127.0.0.1`. لذلك لم يكن ممكناً تنفيذ التحقق الحي من الفاتورة المسودة، التقارير، البطاقات، ومساحات العمل على الموقع.

القرار: غير آمن للانتقال إلى Lease Contract and Rent Schedule foundation قبل استعادة MariaDB وإعادة تشغيل مراجعة الجاهزية الحية.

## 2. ما هو جاهز من ناحية الكود والملفات

- DocType `Sales Invoice Collection Settings` موجود في ملفات التطبيق.
- `Sales Contract` يحتوي حقول إجماليات الفوترة والتحصيل.
- `Sales Installment Schedule` يحتوي حقول حالة الفاتورة والتحصيل.
- خدمات `sales_invoice_utils` و `collections_utils` موجودة وتُترجم برمجياً بدون أخطاء.
- تقارير التحصيل الخمسة موجودة في ملفات التطبيق:
  - Sales Invoice from Installments Report
  - Sales Collection Report
  - Overdue Sales Installments
  - Unit Revenue Report
  - Sales Contract Collection Summary
- روابط التقارير والبطاقات موجودة في ملفات مساحات العمل.
- `ar.csv` صالح كملف CSV ويحتوي 1847 صفاً.
- ترجمات Sales Invoice Collection Settings وتقارير التحصيل وبطاقات التحصيل موجودة.

## 3. ما لم يمكن التحقق منه حياً

بسبب توقف MariaDB، لم يمكن التحقق مباشرة من:

- وجود `Sales Invoice Collection Settings` داخل قاعدة بيانات الموقع.
- فتح عقد البيع `SC-2026-00001` من قاعدة البيانات.
- فتح فاتورة البيع المسودة `ACC-SINV-2026-00001`.
- تأكيد ارتباط الفاتورة بالعقد والوحدة والمشروع العقاري والحجز.
- تأكيد ارتباط أول قسط بالفاتورة المسودة.
- تأكيد قيم:
  - `total_invoiced_amount`
  - `total_collected_amount`
  - `total_outstanding_amount`
  - `collection_status`
- تحميل التقارير من قاعدة البيانات.
- تحميل مساحات العمل والبطاقات من قاعدة البيانات.
- التأكد الحي من عدم وجود GL Entry أو Payment Entry مرتبط بالفاتورة.

## 4. جاهزية الأبعاد المحاسبية

حسب تنفيذ CMD-23 والملفات الحالية:

- يتم نسخ `unit` إلى `Sales Invoice Item` عند توليد الفاتورة من القسط.
- يتم نسخ `project` و `cost_center` حيثما كانا متاحين.
- يتم حفظ مراجع `sales_contract` و `sales_installment_reference` و `real_estate_project` و `unit_reservation` على بند الفاتورة حيث توجد الحقول.

لكن التحقق الحي من هذه القيم على `ACC-SINV-2026-00001` لم يكتمل بسبب توقف قاعدة البيانات.

## 5. حالة الفاتورة المسودة

حسب سجل CMD-23، تم إنشاء:

- Sales Invoice: `ACC-SINV-2026-00001`
- الحالة: Draft
- العقد: `SC-2026-00001`
- الوحدة: `A-101`
- قيمة الفاتورة: `300,000`
- المحصل: `0`
- المتبقي: `300,000`

هذه القيم تحتاج إعادة تأكيد حي بعد استعادة MariaDB.

## 6. حالة التحصيل

حسب سجل CMD-23:

- حالة العقد: `Partially Invoiced`
- إجمالي المفوتر: `300,000`
- إجمالي المحصل: `0`
- إجمالي المتبقي: `300,000`

لم يتم إنشاء Payment Entry في CMD-23، وهذا صحيح لأن الفاتورة بقيت Draft ولم يتم ترحيلها.

## 7. جاهزية التقارير

الملفات موجودة، لكن تحميل التقارير من الموقع لم يكتمل بسبب توقف MariaDB.

تقارير CMD-23 المطلوب إعادة اختبارها بعد الاستعادة:

- Sales Invoice from Installments Report
- Sales Collection Report
- Overdue Sales Installments
- Unit Revenue Report
- Sales Contract Collection Summary

كما يجب إعادة اختبار التقارير السابقة المهمة قبل الانتقال:

- Sales Contract Register
- Installment Schedule Report
- Unit Sales Pipeline
- Sales Value Summary
- Unit Profitability Report
- Unit Financial Ledger
- GL Dimension Traceability
- Project Unit Cost Matrix
- Project Financial Snapshot Report
- Project Cash Flow Forecast Report
- Project EVM Metrics Report

## 8. جاهزية مساحات العمل والبطاقات

تم التحقق من وجود الروابط في ملفات JSON، لكن لم يتم تحميلها من قاعدة البيانات بسبب توقف MariaDB.

يجب إعادة اختبار:

- Sales & Rental
- Executive Presentation Center
- Executive Control Center
- Real Estate Inventory
- Reports & Analytics
- بطاقات:
  - Total Invoiced Sales
  - Total Collected Sales
  - Outstanding Sales Amount
  - Overdue Installments Count
  - Overdue Installments Amount

## 9. جاهزية الترجمة

تم التحقق من أن `construct_erpnext/translations/ar.csv` يقرأ كملف CSV صالح.

الترجمات الموجودة تشمل:

- Sales Invoice Collection Settings
- Sales Invoice from Installments Report
- Sales Collection Report
- Overdue Sales Installments
- Unit Revenue Report
- Sales Contract Collection Summary
- Total Invoiced Sales
- Total Collected Sales
- Outstanding Sales Amount
- Overdue Installments Count
- Overdue Installments Amount

## 10. العناصر المؤجلة

- ترحيل Sales Invoice.
- إنشاء Payment Entry.
- توليد GL Entry من إيراد الوحدة.
- Lease Contract.
- Rent Schedule.
- Commission.
- CRM Matching.
- Portal.
- WhatsApp / Meta integration.
- GL backfill.

## 11. القيود المعروفة

- Sales Invoice ما زالت Draft.
- لا يوجد GL Entry لأن الفاتورة لم تُرحّل.
- لا يمكن اختبار Payment Entry قبل ترحيل الفاتورة عبر ضوابط ERPNext الطبيعية.
- MariaDB توقفت بحالة `oom-kill` أثناء مراجعة CMD-24، وهذا يمنع اعتماد الجاهزية.

## 12. القرار

غير آمن للانتقال إلى Lease Contract and Rent Schedule foundation حالياً.

سبب القرار ليس خللاً مؤكداً في تنفيذ CMD-23، بل عدم إمكانية إكمال التحقق الحي بسبب توقف قاعدة البيانات.

## 13. التوصية

استعادة خدمة MariaDB أولاً، ثم إعادة تشغيل مراجعة Sales Invoice and Collections readiness على الموقع.

بعد نجاح التحقق الحي من الفاتورة المسودة، بعد الوحدة، التقارير، البطاقات، وعدم وجود آثار محاسبية غير مقصودة، يمكن الانتقال إلى Lease Contract and Rent Schedule foundation.
