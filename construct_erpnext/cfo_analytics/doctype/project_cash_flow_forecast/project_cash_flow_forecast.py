import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate, today

from construct_erpnext.cfo_analytics.cash_flow_forecast import get_cash_flow_forecast


class ProjectCashFlowForecast(Document):
	def validate(self):
		if not self.project:
			frappe.throw(_("Project is required."))
		if not self.period_type:
			frappe.throw(_("Period Type is required."))
		if not self.start_date or not self.end_date:
			frappe.throw(_("Start Date and End Date are required."))
		if getdate(self.start_date) > getdate(self.end_date):
			frappe.throw(_("Start Date cannot be after End Date."))
		self.populate_forecast()

	def populate_forecast(self):
		data = get_cash_flow_forecast(
			self.project,
			self.start_date,
			self.end_date,
			self.period_type,
			self.opening_balance,
		)
		for field, value in data.items():
			if field == "periods":
				continue
			if self.meta.has_field(field):
				self.set(field, value)
		self.set("periods", [])
		for row in data.get("periods", []):
			self.append("periods", row)
		if not self.forecast_date:
			self.forecast_date = today()
		if not self.forecast_title:
			project_name = frappe.db.get_value("Project", self.project, "project_name") or self.project
			self.forecast_title = f"توقع التدفق النقدي ل{project_name}"
		if self.status == "Draft":
			self.status = "Generated"
