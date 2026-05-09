import frappe
from frappe.utils import flt, today


SNAPSHOT_FIELDS = (
	"company",
	"project",
	"snapshot_date",
	"boq_total_amount",
	"boq_material_amount",
	"boq_labor_amount",
	"boq_equipment_amount",
	"boq_subcontract_amount",
	"boq_overhead_amount",
	"requested_amount",
	"committed_amount",
	"received_amount",
	"procurement_invoiced_amount",
	"consumed_amount",
	"measured_amount",
	"measured_progress_percent",
	"certified_gross_amount",
	"certified_net_amount",
	"retention_held_amount",
	"retention_released_amount",
	"contractor_outstanding_amount",
	"contractor_paid_amount",
	"budget_vs_committed_variance",
	"budget_vs_invoiced_variance",
	"budget_vs_certified_variance",
	"consumed_vs_measured_variance",
	"procurement_progress_percent",
	"measurement_progress_percent",
	"certification_progress_percent",
	"cost_risk_status",
	"cash_risk_status",
	"overall_status",
	"executive_summary",
	"key_risks",
	"recommendations",
)


def pct(numerator, denominator):
	return flt(numerator) / flt(denominator) * 100 if flt(denominator) else 0


def get_project_financial_snapshot(project, snapshot_date=None):
	snapshot_date = snapshot_date or today()
	metrics = {
		"project": project,
		"snapshot_date": snapshot_date,
		"company": frappe.db.get_value("Project", project, "company"),
	}
	metrics.update(calculate_boq_totals(project))
	metrics.update(calculate_procurement_totals(project))
	metrics.update(calculate_measurement_totals(project))
	metrics.update(calculate_ipc_totals(project))
	metrics.update(calculate_contractor_totals(project))

	boq_total = flt(metrics.get("boq_total_amount"))
	metrics["budget_vs_committed_variance"] = boq_total - flt(metrics.get("committed_amount"))
	metrics["budget_vs_invoiced_variance"] = boq_total - flt(metrics.get("procurement_invoiced_amount"))
	metrics["budget_vs_certified_variance"] = boq_total - flt(metrics.get("certified_gross_amount"))
	metrics["consumed_vs_measured_variance"] = flt(metrics.get("measured_amount")) - flt(metrics.get("consumed_amount"))
	metrics["procurement_progress_percent"] = pct(metrics.get("committed_amount"), boq_total)
	metrics["measurement_progress_percent"] = pct(metrics.get("measured_amount"), boq_total)
	metrics["certification_progress_percent"] = pct(metrics.get("certified_gross_amount"), boq_total)
	metrics["measured_progress_percent"] = metrics["measurement_progress_percent"]
	metrics.update(calculate_risk_status(metrics))
	metrics.update(build_narrative(metrics))
	return {field: metrics.get(field) for field in SNAPSHOT_FIELDS}


@frappe.whitelist()
def get_snapshot_data(project):
	return get_project_financial_snapshot(project)


@frappe.whitelist()
def create_snapshot(project, snapshot_date=None):
	return create_project_financial_snapshot(project, snapshot_date)


def create_project_financial_snapshot(project, snapshot_date=None):
	metrics = get_project_financial_snapshot(project, snapshot_date)
	doc = frappe.get_doc({"doctype": "Project Financial Snapshot", **metrics})
	project_name = frappe.db.get_value("Project", project, "project_name") or project
	doc.snapshot_title = f"الملخص المالي ل{project_name}"
	doc.status = "Generated"
	doc.insert(ignore_permissions=True)
	return doc.name


def calculate_boq_totals(project):
	row = frappe.db.sql(
		"""
		SELECT
			COALESCE(SUM(planned_amount), 0) AS total,
			COALESCE(SUM(CASE WHEN item_category = 'Material' THEN planned_amount ELSE 0 END), 0) AS material,
			COALESCE(SUM(CASE WHEN item_category = 'Labor' THEN planned_amount ELSE 0 END), 0) AS labor,
			COALESCE(SUM(CASE WHEN item_category = 'Equipment' THEN planned_amount ELSE 0 END), 0) AS equipment,
			COALESCE(SUM(CASE WHEN item_category = 'Subcontract' THEN planned_amount ELSE 0 END), 0) AS subcontract,
			COALESCE(SUM(CASE WHEN item_category IN ('Overhead', 'Contingency', 'Other') THEN planned_amount ELSE 0 END), 0) AS overhead
		FROM `tabConstruction Work Item`
		WHERE project = %(project)s AND IFNULL(disabled, 0) = 0 AND status != 'Cancelled'
		""",
		{"project": project},
		as_dict=True,
	)[0]
	return {
		"boq_total_amount": flt(row.total),
		"boq_material_amount": flt(row.material),
		"boq_labor_amount": flt(row.labor),
		"boq_equipment_amount": flt(row.equipment),
		"boq_subcontract_amount": flt(row.subcontract),
		"boq_overhead_amount": flt(row.overhead),
	}


def calculate_procurement_totals(project):
	row = frappe.db.sql(
		"""
		SELECT
			COALESCE(SUM(requested_qty * unit_rate), 0) AS requested_amount,
			COALESCE(SUM(committed_amount), 0) AS committed_amount,
			COALESCE(SUM(received_qty * unit_rate), 0) AS received_amount,
			COALESCE(SUM(invoiced_amount), 0) AS invoiced_amount,
			COALESCE(SUM(consumed_amount), 0) AS consumed_amount
		FROM `tabConstruction Work Item`
		WHERE project = %(project)s AND IFNULL(disabled, 0) = 0 AND status != 'Cancelled'
		""",
		{"project": project},
		as_dict=True,
	)[0]
	return {
		"requested_amount": flt(row.requested_amount),
		"committed_amount": flt(row.committed_amount),
		"received_amount": flt(row.received_amount),
		"procurement_invoiced_amount": flt(row.invoiced_amount),
		"consumed_amount": flt(row.consumed_amount),
	}


def calculate_measurement_totals(project):
	row = frappe.db.sql(
		"""
		SELECT COALESCE(SUM(measurement_amount), 0) AS measured_amount
		FROM `tabConstruction Work Item`
		WHERE project = %(project)s AND IFNULL(disabled, 0) = 0 AND status != 'Cancelled'
		""",
		{"project": project},
		as_dict=True,
	)[0]
	if not flt(row.measured_amount):
		row.measured_amount = frappe.db.sql(
			"""
			SELECT COALESCE(SUM(measured_amount), 0)
			FROM `tabMeasurement Entry`
			WHERE project = %s AND status IN ('Verified', 'Locked') AND docstatus < 2
			""",
			project,
		)[0][0]
	return {"measured_amount": flt(row.measured_amount)}


def calculate_ipc_totals(project):
	row = frappe.db.sql(
		"""
		SELECT
			COALESCE(SUM(gross_amount), 0) AS gross,
			COALESCE(SUM(net_payable), 0) AS net
		FROM `tabInterim Payment Certificate`
		WHERE project = %(project)s AND docstatus < 2 AND status != 'Rejected'
		""",
		{"project": project},
		as_dict=True,
	)[0]
	return {
		"certified_gross_amount": flt(row.gross),
		"certified_net_amount": flt(row.net),
	}


def calculate_contractor_totals(project):
	account = frappe.db.sql(
		"""
		SELECT
			COALESCE(SUM(total_paid_amount), 0) AS paid,
			COALESCE(SUM(outstanding_balance), 0) AS outstanding
		FROM `tabContractor Account`
		WHERE project = %(project)s AND status != 'Closed'
		""",
		{"project": project},
		as_dict=True,
	)[0]
	retention = frappe.db.sql(
		"""
		SELECT
			COALESCE(SUM(retention_amount), 0) AS held,
			COALESCE(SUM(released_amount), 0) AS released
		FROM `tabRetention Register`
		WHERE project = %(project)s AND status != 'Cancelled'
		""",
		{"project": project},
		as_dict=True,
	)[0]
	return {
		"retention_held_amount": flt(retention.held),
		"retention_released_amount": flt(retention.released),
		"contractor_outstanding_amount": flt(account.outstanding),
		"contractor_paid_amount": flt(account.paid),
	}


def calculate_risk_status(metrics):
	boq_total = flt(metrics.get("boq_total_amount"))
	committed = flt(metrics.get("committed_amount"))
	outstanding = flt(metrics.get("contractor_outstanding_amount"))
	certified_net = flt(metrics.get("certified_net_amount"))

	if boq_total and committed > boq_total:
		cost = "Red"
	elif boq_total and committed >= boq_total * 0.9:
		cost = "Yellow"
	else:
		cost = "Green"

	if certified_net and outstanding > certified_net * 0.75:
		cash = "Red"
	elif certified_net and outstanding > certified_net * 0.4:
		cash = "Yellow"
	else:
		cash = "Green"

	if "Red" in (cost, cash):
		overall = "At Risk"
	elif "Yellow" in (cost, cash):
		overall = "Watch"
	else:
		overall = "On Track"

	return {
		"cost_risk_status": cost,
		"cash_risk_status": cash,
		"overall_status": overall,
	}


def build_narrative(metrics):
	summary = (
		"يوضح هذا الملخص العلاقة بين الميزانية، الالتزامات، القياسات، "
		"المستخلصات، والمستحقات على المقاولين."
	)
	risks = []
	if metrics.get("cost_risk_status") == "Red":
		risks.append("الالتزامات تجاوزت قيمة جدول الكميات المعتمد.")
	elif metrics.get("cost_risk_status") == "Yellow":
		risks.append("الالتزامات تقترب من كامل قيمة جدول الكميات.")
	if metrics.get("cash_risk_status") == "Red":
		risks.append("المستحقات القائمة على المقاولين مرتفعة مقارنة بصافي المستخلصات.")
	elif metrics.get("cash_risk_status") == "Yellow":
		risks.append("توجد مستحقات قائمة تتطلب متابعة مالية.")
	if not risks:
		risks.append("لا توجد مؤشرات مخاطر جوهرية حسب القواعد الحالية.")
	recommendation = (
		"مراجعة الالتزامات المفتوحة، ومطابقة المستخلصات مع القياسات المعتمدة، "
		"ومتابعة أرصدة المقاولين قبل إصدار دفعات جديدة."
	)
	return {
		"executive_summary": summary,
		"key_risks": "\n".join(risks),
		"recommendations": recommendation,
	}
