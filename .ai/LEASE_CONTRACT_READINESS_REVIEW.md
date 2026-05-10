# مراجعة جاهزية عقد الإيجار قبل فواتير الإيجار والتحصيل

## 1. الملخص

تم تنفيذ مراجعة CMD-26 لعقد الإيجار وجدول الإيجار بعد اكتمال مرحلة Lease Contract and Rent Schedule Foundation.

قرار المراجعة: جاهز للانتقال إلى مرحلة Rent Invoice and Collections foundation.

هذه المراجعة كانت مراجعة تحقق وتوثيق فقط. لم يتم إنشاء فاتورة إيجار، أو فاتورة بيع، أو سند قبض، أو قيد يومية، أو أي مستند محاسبي جديد.

## 2. ما تم اجتيازه

- Lease Contract Settings موجود.
- Lease Contract موجود.
- Rent Schedule موجود كجدول فرعي.
- Lease Contract Approval Workflow موجود ويحمّل بنجاح.
- عقد الإيجار `LC-2026-00001` موجود وحالته `Active`.
- الوحدة `A-G01` حالتها `Rented` و `marketing_status` أيضاً `Rented`.
- الحجز `RES-2026-00005` حالته `Converted` ويرتبط بعقد الإيجار `LC-2026-00001`.
- جدول الإيجار يحتوي على 12 صفاً شهرياً.
- إجمالي جدول الإيجار يساوي إجمالي قيمة العقد: `4,200,000`.
- منع عقد إيجار نشط مكرر لنفس الوحدة يعمل، وتم التحقق منه بدون حفظ مستند جديد.
- لا توجد فواتير إيجار أو سندات قبض أو قيود يومية أو قيود GL ناتجة عن عقد الإيجار.

## 3. ما هو مؤجل

- إنشاء Rent Invoice أو Sales Invoice من جدول الإيجار.
- إنشاء Payment Entry للتحصيل.
- تحديث حالة جدول الإيجار بناءً على الفواتير والتحصيلات.
- التحقق من انتقال بعد الوحدة إلى GL من خلال فاتورة إيجار مرحّلة.
- تقارير التحصيل الفعلي للإيجارات.
- أي عمولات، CRM Matching، Portal، WhatsApp/Meta، أو Handover/Registration.

## 4. جاهزية الأبعاد المحاسبية

- Accounting Dimension للـ `Unit` موجود.
- حقل `unit` موجود على `Sales Invoice Item`.
- حقل `unit` موجود على `GL Entry`.
- عقد الإيجار يحمل مرجع الوحدة التشغيلي `A-G01`.
- Rent Schedule يرث الوحدة من عقد الإيجار من خلال parent Lease Contract.
- لا توجد قيود GL لعقد الإيجار، وهذا متوقع لأن هذه المرحلة تشغيلية فقط.

في المرحلة القادمة، عند إنشاء فاتورة الإيجار باستخدام Sales Invoice، يجب نسخ الوحدة من Lease Contract إلى Sales Invoice Item حتى تنتقل كـ Accounting Dimension إلى GL بعد الترحيل الطبيعي.

## 5. جاهزية جدول الإيجار

- الجدول الشهري تم إنشاؤه بشكل حتمي من تاريخ بداية ونهاية العقد والتكرار الشهري.
- عدد الصفوف: 12.
- إجمالي الجدول: `4,200,000`.
- إجمالي العقد: `4,200,000`.
- لا توجد فواتير أو سندات مرتبطة بصفوف الجدول حالياً.

## 6. التقارير ومساحات العمل

التقارير التالية تم تحميلها بدون أخطاء:

- Lease Contract Register.
- Rent Schedule Report.
- Active Leases Report.
- Lease Expiry Report.
- Rental Value Summary.
- Sales Contract Register.
- Sales Collection Report.
- Unit Profitability Report.
- Unit Financial Ledger.
- GL Dimension Traceability.
- Project Unit Cost Matrix.
- Project Financial Snapshot Report.
- Project Cash Flow Forecast Report.
- Project EVM Metrics Report.

مساحات العمل التالية تم تحميلها وتحتوي روابط التأجير:

- Sales & Rental.
- Executive Presentation Center.
- Executive Control Center.
- Real Estate Inventory.
- Reports & Analytics.

## 7. جاهزية الترجمة وتجربة الاستخدام

- ملف `construct_erpnext/translations/ar.csv` يقرأ كملف CSV صالح وفق الصيغة الحالية التي تتضمن تعليقات وفواصل.
- ترجمات عقود الإيجار، جدول الإيجار، تقارير الإيجار، حالات سير الاعتماد، والإجراءات الأساسية موجودة.
- نموذج Lease Contract منظم بتبويبات وأقسام وأعمدة:
  - 8 Tab Breaks.
  - 9 Section Breaks.
  - 6 Column Breaks.

## 8. المخاطر

- Rent Schedule تشغيلي فقط حالياً ولا يمثل ذمة مدينة حتى يتم إنشاء فاتورة إيجار في المرحلة التالية.
- لا توجد قيود GL للإيجار حتى يتم ترحيل فاتورة Sales Invoice لاحقاً من مسار ERPNext الطبيعي.
- Payment Entry والتحصيل الفعلي مؤجلان حتى وجود فاتورة مرحّلة.
- يجب الاستمرار في مراقبة ذاكرة MariaDB بسبب حادثة OOM السابقة قبل أي عمليات migration أو تحقق ثقيلة.

## 9. القرار

آمن للانتقال إلى مرحلة Rent Invoice and Collections foundation.

الشرط المعماري للمرحلة القادمة:

- Rent Invoice يجب أن يُبنى من Rent Schedule داخل Lease Contract.
- Tenant/Customer يبقى داخل Lease Contract وليس داخل Unit.
- Unit يجب أن ينتقل إلى Sales Invoice Item كبعد محاسبي.
- Payment Entry يبقى مستند التحصيل الرسمي في ERPNext.
