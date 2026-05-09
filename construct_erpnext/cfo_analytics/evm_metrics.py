import frappe
from frappe.utils import flt, today


def get_evm_metrics(project, calculation_date=None, planned_progress_percent=None):
	calculation_date = calculation_date or today()
	bac = calculate_bac(project)
	ev = calculate_ev(project)
	ac = calculate_ac(project)
	planned_progress_percent = get_planned_progress_percent(project, planned_progress_percent)
	pv = calculate_pv(project, bac, planned_progress_percent, calculation_date)
	formulas = calculate_evm_formulas(bac, ev, ac, pv)
	refs = get_latest_references(project)
	metrics = {
		"company": frappe.db.get_value("Project", project, "company"),
		"project": project,
		"calculation_date": calculation_date,
		"budget_at_completion": bac,
		"earned_value": ev,
		"actual_cost": ac,
		"planned_value": pv,
		"planned_progress_percent": planned_progress_percent,
		"certification_progress_percent": formulas["actual_progress_percent"],
		**formulas,
		**refs,
	}
	metrics.update(calculate_evm_risk(metrics))
	metrics.update(build_narrative(metrics))
	return metrics


@frappe.whitelist()
def get_evm_data(project, calculation_date=None, planned_progress_percent=None):
	return get_evm_metrics(project, calculation_date, planned_progress_percent)


@frappe.whitelist()
def create_evm_snapshot(project, calculation_date=None, planned_progress_percent=None):
	return create_evm_metrics(project, calculation_date, planned_progress_percent)


def create_evm_metrics(project, calculation_date=None, planned_progress_percent=None):
	metrics = get_evm_metrics(project, calculation_date, planned_progress_percent)
	project_name = frappe.db.get_value("Project", project, "project_name") or project
	doc = frappe.get_doc({"doctype": "Project EVM Metrics", **metrics})
	doc.evm_title = f"مؤشرات القيمة المكتسبة ل{project_name}"
	doc.status = "Calculated"
	doc.insert(ignore_permissions=True)
	return doc.name


def calculate_bac(project):
	amount = frappe.db.sql(
		"""
		SELECT COALESCE(SUM(planned_amount), 0)
		FROM `tabConstruction Work Item`
		WHERE project = %s AND IFNULL(disabled, 0) = 0 AND status != 'Cancelled'
		""",
		project,
	)[0][0]
	if flt(amount):
		return flt(amount)
	amount = frappe.db.get_value(
		"Project Financial Snapshot",
		{"project": project, "status": ["!=", "Archived"]},
		"boq_total_amount",
		order_by="snapshot_date desc, creation desc",
	)
	return flt(amount)


def calculate_ev(project):
	amount = frappe.db.sql(
		"""
		SELECT COALESCE(SUM(certified_amount), 0)
		FROM `tabConstruction Work Item`
		WHERE project = %s AND IFNULL(disabled, 0) = 0 AND status != 'Cancelled'
		""",
		project,
	)[0][0]
	if flt(amount):
		return flt(amount)
	amount = frappe.db.sql(
		"""
		SELECT COALESCE(SUM(gross_amount), 0)
		FROM `tabInterim Payment Certificate`
		WHERE project = %s AND docstatus < 2 AND status NOT IN ('Draft', 'Rejected')
		""",
		project,
	)[0][0]
	return flt(amount)


def calculate_ac(project):
	snapshot_ac = frappe.db.get_value(
		"Project Financial Snapshot",
		{"project": project, "status": ["!=", "Archived"]},
		"procurement_invoiced_amount",
		order_by="snapshot_date desc, creation desc",
	)
	if flt(snapshot_ac):
		return flt(snapshot_ac)
	amount = frappe.db.sql(
		"""
		SELECT COALESCE(SUM(invoiced_amount), 0)
		FROM `tabConstruction Work Item`
		WHERE project = %s AND IFNULL(disabled, 0) = 0 AND status != 'Cancelled'
		""",
		project,
	)[0][0]
	if flt(amount):
		return flt(amount)
	amount = frappe.db.sql(
		"""
		SELECT COALESCE(SUM(DISTINCT pi.grand_total), 0)
		FROM `tabPurchase Invoice` pi
		WHERE pi.docstatus = 1
			AND (
				pi.project = %(project)s
				OR EXISTS (
					SELECT 1 FROM `tabPurchase Invoice Item` pii
					WHERE pii.parent = pi.name AND pii.project = %(project)s
				)
			)
		""",
		{"project": project},
	)[0][0]
	return flt(amount)


def get_planned_progress_percent(project, planned_progress_percent=None):
	if planned_progress_percent is not None and planned_progress_percent != "":
		return flt(planned_progress_percent)
	activity_progress = frappe.db.sql(
		"""
		SELECT AVG(physical_advancement_pct)
		FROM `tabActivity Schedule`
		WHERE project = %s AND IFNULL(physical_advancement_pct, 0) > 0
		""",
		project,
	)[0][0]
	if flt(activity_progress):
		return flt(activity_progress)
	project_progress = frappe.db.get_value("Project", project, "percent_complete")
	return flt(project_progress)


def calculate_pv(project, bac, planned_progress_percent, calculation_date):
	return flt(bac) * flt(planned_progress_percent) / 100


def calculate_evm_formulas(bac, ev, ac, pv):
	bac = flt(bac)
	ev = flt(ev)
	ac = flt(ac)
	pv = flt(pv)
	cpi = ev / ac if ac > 0 else 0
	spi = ev / pv if pv > 0 else 0
	eac = bac / cpi if cpi > 0 else bac
	etc = eac - ac
	vac = bac - eac
	tcpi = (bac - ev) / (bac - ac) if (bac - ac) > 0 else 0
	actual_progress = ev / bac * 100 if bac > 0 else 0
	return {
		"cost_variance": ev - ac,
		"schedule_variance": ev - pv,
		"cost_performance_index": cpi,
		"schedule_performance_index": spi,
		"estimate_at_completion": eac,
		"estimate_to_complete": etc,
		"variance_at_completion": vac,
		"forecast_overrun_amount": abs(vac) if vac < 0 else 0,
		"to_complete_performance_index": tcpi,
		"actual_progress_percent": actual_progress,
	}


def calculate_evm_risk(metrics):
	cpi = flt(metrics.get("cost_performance_index"))
	spi = flt(metrics.get("schedule_performance_index"))
	ac = flt(metrics.get("actual_cost"))
	pv = flt(metrics.get("planned_value"))
	if cpi >= 1:
		cost = "Green"
	elif cpi >= 0.9:
		cost = "Yellow"
	elif ac > 0:
		cost = "Red"
	else:
		cost = "Green"
	if spi >= 1:
		schedule = "Green"
	elif spi >= 0.9:
		schedule = "Yellow"
	elif pv > 0:
		schedule = "Red"
	else:
		schedule = "Green"
	if "Red" in (cost, schedule):
		overall = "At Risk"
	elif "Yellow" in (cost, schedule):
		overall = "Watch"
	else:
		overall = "On Track"
	return {
		"cost_status": cost,
		"schedule_status": schedule,
		"overall_evm_status": overall,
	}


def get_latest_references(project):
	return {
		"project_financial_snapshot": frappe.db.get_value(
			"Project Financial Snapshot",
			{"project": project, "status": ["!=", "Archived"]},
			"name",
			order_by="snapshot_date desc, creation desc",
		),
		"cash_flow_forecast": frappe.db.get_value(
			"Project Cash Flow Forecast",
			{"project": project, "status": ["!=", "Archived"]},
			"name",
			order_by="forecast_date desc, creation desc",
		),
	}


def build_narrative(metrics):
	summary = (
		"يوضح هذا المؤشر مقارنة القيمة المكتسبة من الأعمال المعتمدة "
		"بالتكلفة الفعلية والقيمة المخططة حتى تاريخ القياس."
	)
	risks = []
	if metrics.get("cost_status") == "Red":
		risks.append("مؤشر كفاءة التكلفة أقل من الحد المقبول ويشير إلى ضغط تكلفة.")
	elif metrics.get("cost_status") == "Yellow":
		risks.append("مؤشر كفاءة التكلفة قريب من الحد الأدنى ويحتاج إلى متابعة.")
	if metrics.get("schedule_status") == "Red":
		risks.append("القيمة المكتسبة أقل من القيمة المخططة بصورة مؤثرة.")
	elif metrics.get("schedule_status") == "Yellow":
		risks.append("القيمة المكتسبة قريبة من القيمة المخططة مع حاجة للمتابعة.")
	if not risks:
		risks.append("لا توجد مؤشرات انحراف جوهرية حسب قواعد EVM الحالية.")
	recommendation = (
		"مراجعة بنود التكلفة ذات الصرف العالي، ومقارنة الاعتماد المرحلي "
		"مع البرنامج الزمني قبل تحديث توقعات نهاية المشروع."
	)
	return {
		"executive_summary": summary,
		"key_risks": "\n".join(risks),
		"recommendations": recommendation,
	}
