import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class WBSElement(Document):
	def validate(self):
		self.validate_progress_weight()
		self.validate_unique_wbs_code_per_project()
		self.validate_parent_project()

	def validate_progress_weight(self):
		if flt(self.progress_weight) < 0 or flt(self.progress_weight) > 100:
			frappe.throw(_("Progress Weight must be between 0 and 100."))

	def validate_unique_wbs_code_per_project(self):
		existing = frappe.db.exists(
			"WBS Element",
			{
				"project": self.project,
				"wbs_code": self.wbs_code,
				"name": ["!=", self.name],
			},
		)
		if existing:
			frappe.throw(
				_("WBS Code {0} already exists for Project {1}.").format(
					self.wbs_code, self.project
				)
			)

	def validate_parent_project(self):
		if not self.parent_wbs_element:
			return

		parent_project = frappe.db.get_value(
			"WBS Element", self.parent_wbs_element, "project"
		)
		if parent_project and parent_project != self.project:
			frappe.throw(_("Parent WBS Element must belong to the same Project."))
