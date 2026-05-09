import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


CATEGORY_TOTAL_FIELDS = {
	"Material": "total_material_cost",
	"Labor": "total_labor_cost",
	"Equipment": "total_equipment_cost",
	"Subcontract": "total_subcontract_cost",
	"Overhead": "total_overhead_cost",
	"Contingency": "total_contingency_cost",
}


class ConstructionBOQ(Document):
	def validate(self):
		self.validate_required_values()
		self.sync_status_fields()
		self.calculate_items_and_totals()

	def validate_required_values(self):
		if not self.project:
			frappe.throw(_("Project is required."))
		if not self.boq_number:
			frappe.throw(_("BOQ Number is required."))

	def sync_status_fields(self):
		if not self.status and not self.workflow_state:
			self.status = "Draft"
			self.workflow_state = "Draft"
		elif self.workflow_state and self.workflow_state != self.status:
			self.status = self.workflow_state
		elif self.status and not self.workflow_state:
			self.workflow_state = self.status

	def calculate_items_and_totals(self):
		totals = {fieldname: 0 for fieldname in CATEGORY_TOTAL_FIELDS.values()}
		total_amount = 0

		for row in self.items or []:
			self.validate_boq_item(row)
			row.amount = flt(row.quantity) * flt(row.unit_rate)
			row.final_quantity = flt(row.quantity) + (
				flt(row.quantity) * flt(row.wastage_percent) / 100
			)
			row.final_amount = (
				flt(row.amount)
				+ (flt(row.amount) * flt(row.wastage_percent) / 100)
				+ (flt(row.amount) * flt(row.markup_percent) / 100)
			)

			total_amount += flt(row.final_amount)
			total_field = CATEGORY_TOTAL_FIELDS.get(row.item_category)
			if total_field:
				totals[total_field] += flt(row.final_amount)

		for fieldname, amount in totals.items():
			self.set(fieldname, amount)

		self.total_amount = total_amount
		self.variance_amount = flt(self.total_amount) - flt(self.total_actual_cost)
		self.variance_percent = (
			flt(self.variance_amount) / flt(self.total_amount) * 100
			if flt(self.total_amount)
			else 0
		)

	def validate_boq_item(self, row):
		if flt(row.quantity) < 0:
			frappe.throw(_("Row {0}: Quantity cannot be negative.").format(row.idx))
		if flt(row.unit_rate) < 0:
			frappe.throw(_("Row {0}: Unit Rate cannot be negative.").format(row.idx))
		if flt(row.wastage_percent) < 0:
			frappe.throw(_("Row {0}: Wastage Percent cannot be negative.").format(row.idx))
		if flt(row.markup_percent) < 0:
			frappe.throw(_("Row {0}: Markup Percent cannot be negative.").format(row.idx))

		if row.cost_code:
			cost_code = frappe.db.get_value(
				"Cost Code", row.cost_code, ["is_group", "disabled"], as_dict=True
			)
			if cost_code and cost_code.is_group:
				frappe.throw(
					_("Row {0}: Group Cost Code {1} cannot be used for BOQ costing.").format(
						row.idx, row.cost_code
					)
				)
			if cost_code and cost_code.disabled:
				frappe.throw(
					_("Row {0}: Disabled Cost Code {1} cannot be used.").format(
						row.idx, row.cost_code
					)
				)

		if row.wbs_element:
			wbs = frappe.db.get_value(
				"WBS Element", row.wbs_element, ["project", "wbs_code", "disabled"], as_dict=True
			)
			if wbs and wbs.project != self.project:
				frappe.throw(
					_("Row {0}: WBS Element must belong to Project {1}.").format(
						row.idx, self.project
					)
				)
			if wbs and wbs.disabled:
				frappe.throw(
					_("Row {0}: Disabled WBS Element {1} cannot be used.").format(
						row.idx, row.wbs_element
					)
				)
			if wbs and not row.wbs_code:
				row.wbs_code = wbs.wbs_code

	def on_submit(self):
		if self.status in ("Approved", "Locked") or self.workflow_state in (
			"Approved",
			"Locked",
		):
			self.generate_work_items()

	def before_cancel(self):
		if self.work_items_generated and frappe.db.exists(
			"Construction Work Item", {"construction_boq": self.name}
		):
			frappe.throw(
				_(
					"Cannot cancel this BOQ because Construction Work Items were generated. "
					"Cancel or disable downstream work items first."
				)
			)

	def generate_work_items(self):
		created = 0
		for row in self.items or []:
			if not row.description:
				continue

			if frappe.db.exists(
				"Construction Work Item",
				{"construction_boq": self.name, "boq_item_row_id": row.name},
			):
				continue

			work_item = frappe.get_doc(
				{
					"doctype": "Construction Work Item",
					"project": self.project,
					"construction_boq": self.name,
					"boq_item_row_id": row.name,
					"wbs_element": row.wbs_element,
					"wbs_code": row.wbs_code,
					"cost_code": row.cost_code,
					"item_code": row.item_code,
					"description": row.description,
					"item_category": row.item_category,
					"planned_quantity": flt(row.final_quantity),
					"uom": row.uom,
					"unit_rate": flt(row.unit_rate),
					"planned_amount": flt(row.final_amount),
					"budget_level": row.budget_level,
					"cost_center": row.cost_center or self.cost_center,
					"status": "Planned",
					"source_boq_revision": self.revision_no,
				}
			)
			work_item.insert(ignore_permissions=True)
			created += 1

		if created and not self.work_items_generated:
			self.db_set("work_items_generated", 1, update_modified=False)

		return created
