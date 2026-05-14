import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, getdate

from construct_erpnext.contractor_management.agreement_utils import (
	FINAL_AGREEMENT_STATUSES,
	link_work_items_to_agreement,
	recalculate_agreement_totals,
	sync_agreement_items_from_work_items,
	unlink_work_items_from_agreement,
	validate_work_item_assignment,
)


class Subcontract(Document):
	def validate(self):
		self.set_defaults()
		self.validate_dates()
		self.validate_scope()
		sync_agreement_items_from_work_items(self)
		recalculate_agreement_totals(self)

	def set_defaults(self):
		if not self.agreement_number:
			self.agreement_number = self.name if self.name and not self.is_new() else None
		if not self.agreement_date:
			self.agreement_date = getdate()
		if not self.agreement_type:
			self.agreement_type = "Unit Rate"
		if not self.contract_status:
			self.contract_status = "Draft"
		if not self.workflow_state:
			self.workflow_state = self.contract_status
		if self.workflow_state and self.workflow_state != self.contract_status:
			self.contract_status = self.workflow_state
		if not flt(self.retention_percent):
			self.retention_percent = 10

	def compute_remaining(self):
		self.remaining_amount = flt(self.negotiated_amount) - flt(self.paid_amount)

	def validate_dates(self):
		if self.start_date and self.end_date:
			if getdate(self.end_date) < getdate(self.start_date):
				frappe.throw(_("End Date cannot be before Start Date."))
		if self.start_date and self.expected_end_date:
			if getdate(self.expected_end_date) < getdate(self.start_date):
				frappe.throw(_("Expected End Date cannot be before Start Date."))

	def validate_scope(self):
		seen = set()
		for row in self.activities:
			if flt(row.agreed_quantity) < 0 or flt(row.agreed_rate) < 0:
				frappe.throw(_("Row {0}: agreed quantity and rate cannot be negative.").format(row.idx))
			if not row.construction_work_item:
				continue
			if row.construction_work_item in seen:
				frappe.throw(_("Construction Work Item {0} is repeated.").format(row.construction_work_item))
			seen.add(row.construction_work_item)
			project, construction_boq = frappe.db.get_value(
				"Construction Work Item",
				row.construction_work_item,
				["project", "construction_boq"],
			)
			if project != self.project:
				frappe.throw(
					_("Row {0}: Construction Work Item must belong to project {1}.").format(
						row.idx, self.project
					)
				)
			if self.construction_boq and construction_boq != self.construction_boq:
				frappe.throw(
					_("Row {0}: Construction Work Item must belong to BOQ {1}.").format(
						row.idx, self.construction_boq
					)
				)
			if self.contract_status not in FINAL_AGREEMENT_STATUSES:
				validate_work_item_assignment(row.construction_work_item, self.name)

	def on_submit(self):
		if self.contract_status in ("Draft", "Under Review", "Authorized", "Approved"):
			self.db_set("contract_status", "Active", update_modified=False)
			self.db_set("workflow_state", "Active", update_modified=False)
		if not self.agreement_number:
			self.db_set("agreement_number", self.name, update_modified=False)
		link_work_items_to_agreement(self)

	def on_cancel(self):
		for row in self.activities:
			if not row.construction_work_item:
				continue
			ipc = frappe.db.exists(
				"Interim Payment Certificate Line",
				{"construction_work_item": row.construction_work_item},
			)
			if ipc:
				frappe.throw(
					_("Cannot cancel Contractor Agreement because linked IPC lines exist for Work Item {0}.").format(
						row.construction_work_item
					)
				)
		unlink_work_items_from_agreement(self)
		self.db_set("contract_status", "Cancelled", update_modified=False)
		self.db_set("workflow_state", "Cancelled", update_modified=False)
