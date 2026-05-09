import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, today

from construct_erpnext.cfo_analytics.evm_metrics import get_evm_metrics


class ProjectEVMMetrics(Document):
	def validate(self):
		if not self.project:
			frappe.throw(_("Project is required."))
		if not self.calculation_date:
			self.calculation_date = today()
		if flt(self.planned_progress_percent) < 0 or flt(self.planned_progress_percent) > 100:
			frappe.throw(_("Planned Progress Percent must be between 0 and 100."))
		self.populate_metrics()

	def populate_metrics(self):
		metrics = get_evm_metrics(
			self.project,
			self.calculation_date,
			self.planned_progress_percent,
		)
		for field, value in metrics.items():
			if self.meta.has_field(field):
				self.set(field, value)
		if not self.evm_title:
			project_name = frappe.db.get_value("Project", self.project, "project_name") or self.project
			self.evm_title = f"مؤشرات القيمة المكتسبة ل{project_name}"
		if self.status == "Draft":
			self.status = "Calculated"
