from calendar import monthrange

import frappe
from frappe.utils import add_days, add_months, flt, getdate, today


def get_cash_flow_forecast(project, start_date, end_date, period_type="Monthly", opening_balance=0):
	periods = []
	running_balance = flt(opening_balance)

	for period in build_periods(start_date, end_date, period_type):
		row = calculate_period_sources(project, period["period_start"], period["period_end"])
		row.update(period)
		row["total_inflow"] = (
			flt(row.get("expected_sales_inflow"))
			+ flt(row.get("expected_rent_inflow"))
			+ flt(row.get("expected_other_inflow"))
		)
		row["total_outflow"] = (
			flt(row.get("purchase_order_outflow"))
			+ flt(row.get("purchase_invoice_outflow"))
			+ flt(row.get("ipc_outflow"))
			+ flt(row.get("retention_release_outflow"))
			+ flt(row.get("advance_outflow"))
			+ flt(row.get("other_outflow"))
		)
		row["net_cash_flow"] = flt(row["total_inflow"]) - flt(row["total_outflow"])
		running_balance += flt(row["net_cash_flow"])
		row["running_balance"] = running_balance
		row["cash_deficit"] = 1 if running_balance < 0 else 0
		row["deficit_amount"] = abs(running_balance) if running_balance < 0 else 0
		periods.append(row)

	total_inflow = sum(flt(row["total_inflow"]) for row in periods)
	total_outflow = sum(flt(row["total_outflow"]) for row in periods)
	lowest_balance = min([flt(opening_balance)] + [flt(row["running_balance"]) for row in periods])
	cash_deficit_amount = sum(flt(row["deficit_amount"]) for row in periods)
	if not cash_deficit_amount and lowest_balance < 0:
		cash_deficit_amount = abs(lowest_balance)

	risk = calculate_cash_risk(periods, total_outflow, lowest_balance)
	company = frappe.db.get_value("Project", project, "company")
	return {
		"company": company,
		"project": project,
		"forecast_date": today(),
		"period_type": period_type,
		"start_date": getdate(start_date),
		"end_date": getdate(end_date),
		"opening_balance": flt(opening_balance),
		"total_expected_inflow": total_inflow,
		"total_expected_outflow": total_outflow,
		"net_cash_flow": total_inflow - total_outflow,
		"lowest_projected_balance": lowest_balance,
		"cash_deficit_amount": cash_deficit_amount,
		"cash_risk_status": risk,
		"executive_summary": (
			"يوضح هذا التوقع الاحتياجات النقدية المتوقعة للمشروع بناءً على "
			"المستخلصات، الفواتير، والمحتجزات، مع إبراز فترات العجز النقدي المحتملة."
		),
		"key_risks": build_key_risks(risk, periods),
		"recommendations": build_recommendations(risk),
		"periods": periods,
	}


@frappe.whitelist()
def get_forecast_data(project, start_date, end_date, period_type="Monthly", opening_balance=0):
	return get_cash_flow_forecast(project, start_date, end_date, period_type, opening_balance)


@frappe.whitelist()
def create_forecast(project, start_date, end_date, period_type="Monthly", opening_balance=0):
	return create_cash_flow_forecast(project, start_date, end_date, period_type, opening_balance)


def create_cash_flow_forecast(project, start_date, end_date, period_type="Monthly", opening_balance=0):
	data = get_cash_flow_forecast(project, start_date, end_date, period_type, opening_balance)
	project_name = frappe.db.get_value("Project", project, "project_name") or project
	doc = frappe.get_doc({"doctype": "Project Cash Flow Forecast", **data})
	doc.forecast_title = f"توقع التدفق النقدي ل{project_name}"
	doc.status = "Generated"
	doc.insert(ignore_permissions=True)
	return doc.name


def build_periods(start_date, end_date, period_type):
	start = getdate(start_date)
	end = getdate(end_date)
	periods = []
	current = start
	while current <= end:
		if period_type == "Weekly":
			period_end = min(add_days(current, 6), end)
		elif period_type == "Quarterly":
			period_end = min(add_days(add_months(current, 3), -1), end)
		else:
			month_end = current.replace(day=monthrange(current.year, current.month)[1])
			period_end = min(month_end, end)
		periods.append(
			{
				"period_start": current,
				"period_end": period_end,
				"period_label": f"{current} - {period_end}",
			}
		)
		current = add_days(period_end, 1)
	return periods


def calculate_period_sources(project, period_start, period_end):
	inflows = calculate_inflows(project, period_start, period_end)
	po = calculate_purchase_order_outflow(project, period_start, period_end)
	pi = calculate_purchase_invoice_outflow(project, period_start, period_end)
	ipc = calculate_ipc_outflow(project, period_start, period_end)
	retention = calculate_retention_release_outflow(project, period_start, period_end)
	return {
		**inflows,
		"purchase_order_outflow": po["amount"],
		"purchase_invoice_outflow": pi["amount"],
		"ipc_outflow": ipc["amount"],
		"retention_release_outflow": retention["amount"],
		"advance_outflow": 0,
		"other_outflow": 0,
		"purchase_order_count": po["count"],
		"purchase_invoice_count": pi["count"],
		"ipc_count": ipc["count"],
		"retention_count": retention["count"],
		"remarks": build_period_remarks(po, pi, ipc, retention),
	}


def calculate_purchase_order_outflow(project, period_start, period_end):
	# Count only the uninvoiced portion of submitted Purchase Orders linked to the project.
	rows = frappe.db.sql(
		"""
		SELECT poi.parent, GREATEST(COALESCE(poi.amount, 0) - COALESCE(poi.billed_amt, 0), 0) AS pending_amount
		FROM `tabPurchase Order Item` poi
		INNER JOIN `tabPurchase Order` po ON po.name = poi.parent
		WHERE po.docstatus = 1
			AND COALESCE(poi.project, po.project) = %(project)s
			AND COALESCE(poi.schedule_date, po.schedule_date, po.transaction_date) BETWEEN %(period_start)s AND %(period_end)s
			AND GREATEST(COALESCE(poi.amount, 0) - COALESCE(poi.billed_amt, 0), 0) > 0
		""",
		{"project": project, "period_start": period_start, "period_end": period_end},
		as_dict=True,
	)
	return {"amount": sum(flt(row.pending_amount) for row in rows), "count": len({row.parent for row in rows})}


def calculate_purchase_invoice_outflow(project, period_start, period_end):
	# Submitted Purchase Invoices are preferred over IPCs for the same payable.
	rows = frappe.db.sql(
		"""
		SELECT DISTINCT pi.name, COALESCE(pi.outstanding_amount, 0) AS outstanding_amount
		FROM `tabPurchase Invoice` pi
		WHERE pi.docstatus = 1
			AND COALESCE(pi.due_date, pi.posting_date) BETWEEN %(period_start)s AND %(period_end)s
			AND COALESCE(pi.outstanding_amount, 0) > 0
			AND (
				pi.project = %(project)s
				OR EXISTS (
					SELECT 1
					FROM `tabPurchase Invoice Item` pii
					WHERE pii.parent = pi.name AND pii.project = %(project)s
				)
				OR EXISTS (
					SELECT 1
					FROM `tabInterim Payment Certificate` ipc
					WHERE ipc.purchase_invoice = pi.name AND ipc.project = %(project)s
				)
			)
		""",
		{"project": project, "period_start": period_start, "period_end": period_end},
		as_dict=True,
	)
	return {"amount": sum(flt(row.outstanding_amount) for row in rows), "count": len(rows)}


def calculate_ipc_outflow(project, period_start, period_end):
	# If an IPC has a submitted Purchase Invoice, PI outstanding is counted instead.
	rows = frappe.db.sql(
		"""
		SELECT ipc.name, COALESCE(ipc.outstanding_amount, ipc.net_payable - ipc.paid_amount, ipc.net_payable, 0) AS outstanding_amount
		FROM `tabInterim Payment Certificate` ipc
		LEFT JOIN `tabPurchase Invoice` pi ON pi.name = ipc.purchase_invoice
		WHERE ipc.project = %(project)s
			AND ipc.docstatus < 2
			AND ipc.status IN ('Approved', 'Invoice Created', 'Partially Paid')
			AND COALESCE(ipc.expected_next_payment_date, ipc.period_end) BETWEEN %(period_start)s AND %(period_end)s
			AND COALESCE(ipc.outstanding_amount, ipc.net_payable - ipc.paid_amount, ipc.net_payable, 0) > 0
			AND (ipc.purchase_invoice IS NULL OR pi.docstatus IS NULL OR pi.docstatus != 1)
		""",
		{"project": project, "period_start": period_start, "period_end": period_end},
		as_dict=True,
	)
	return {"amount": sum(flt(row.outstanding_amount) for row in rows), "count": len(rows)}


def calculate_retention_release_outflow(project, period_start, period_end):
	rows = frappe.db.sql(
		"""
		SELECT name, COALESCE(remaining_retention_amount, retention_amount - released_amount, retention_amount, 0) AS amount
		FROM `tabRetention Register`
		WHERE project = %(project)s
			AND status IN ('Held', 'Eligible for Release')
			AND release_due_date BETWEEN %(period_start)s AND %(period_end)s
			AND COALESCE(remaining_retention_amount, retention_amount - released_amount, retention_amount, 0) > 0
		""",
		{"project": project, "period_start": period_start, "period_end": period_end},
		as_dict=True,
	)
	return {"amount": sum(flt(row.amount) for row in rows), "count": len(rows)}


def calculate_inflows(project, period_start, period_end):
	# Sales and rental collections will be wired after Real Estate Sales/Rental modules exist.
	return {
		"expected_sales_inflow": 0,
		"expected_rent_inflow": 0,
		"expected_other_inflow": 0,
	}


def calculate_cash_risk(periods, total_outflow, lowest_projected_balance):
	if any(row.get("cash_deficit") for row in periods):
		return "Red"
	if flt(total_outflow) and flt(lowest_projected_balance) <= flt(total_outflow) * 0.1:
		return "Yellow"
	return "Green"


def build_period_remarks(po, pi, ipc, retention):
	parts = []
	if po["amount"]:
		parts.append("Uninvoiced submitted Purchase Orders")
	if pi["amount"]:
		parts.append("Submitted Purchase Invoice outstanding")
	if ipc["amount"]:
		parts.append("IPC payable without submitted Purchase Invoice")
	if retention["amount"]:
		parts.append("Retention release due")
	return "; ".join(parts)


def build_key_risks(risk, periods):
	if risk == "Red":
		return "يوجد عجز نقدي متوقع في فترة واحدة أو أكثر ضمن نطاق التوقع."
	if risk == "Yellow":
		return "الرصيد المتوقع قريب من الحد الأدنى الآمن مقارنة بإجمالي التدفقات الخارجة."
	return "لا توجد مؤشرات عجز نقدي حسب البيانات الحالية."


def build_recommendations(risk):
	if risk == "Red":
		return "مراجعة مواعيد دفع المستخلصات والفواتير، وتحديد مصدر تمويل قبل تاريخ الاستحقاق."
	if risk == "Yellow":
		return "مراقبة الرصيد النقدي ومراجعة الالتزامات المفتوحة قبل اعتماد دفعات جديدة."
	return "الاستمرار في تحديث التوقع عند اعتماد مستخلصات أو فواتير جديدة."
