import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate, today

from construct_erpnext.cfo_analytics.project_financials import get_project_financial_snapshot


class ProjectFinancialSnapshot(Document):
	def validate(self):
		if not self.project:
			frappe.throw(_("Project is required."))
		if not self.snapshot_date:
			self.snapshot_date = today()
		self.populate_metrics()

	def populate_metrics(self):
		metrics = get_project_financial_snapshot(self.project, self.snapshot_date)
		for field, value in metrics.items():
			if self.meta.has_field(field):
				self.set(field, value)
		if not self.snapshot_title:
			project_name = frappe.db.get_value("Project", self.project, "project_name") or self.project
			self.snapshot_title = _("Financial Snapshot - {0} - {1}").format(project_name, getdate(self.snapshot_date))
		if self.status == "Draft":
			self.status = "Generated"
