from frappe.model.document import Document
from frappe.utils import flt


class MatchingSettings(Document):
	def validate(self):
		self.minimum_score = flt(self.minimum_score or 60)
		self.location_weight = flt(self.location_weight or 0)
		self.price_weight = flt(self.price_weight or 0)
		self.area_weight = flt(self.area_weight or 0)
		self.type_weight = flt(self.type_weight or 0)
		self.feature_weight = flt(self.feature_weight or 0)
