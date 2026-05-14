from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe.utils import flt, nowdate


class MatchResult(Document):
	def autoname(self):
		self.name = make_autoname("MATCH-.YYYY.-.#####")

	def validate(self):
		self.match_date = self.match_date or nowdate()
		self.total_matches = len(self.items or [])
		self.best_score = max([flt(row.score) for row in self.items], default=0)
