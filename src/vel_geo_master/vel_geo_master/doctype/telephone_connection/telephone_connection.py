# Copyright (c) 2024, SMTW and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class TelephoneConnection(Document):
	def clear_nonapplicable_fields(self):
		if self.connection_type == "Mobile":
			self.geolocation = None
			self.door_number = None
			self.survey_number = None
			self.campus = None
		else:
			self.used_on_device = None
			self.used_by = None
			self.is_esim = False

	def validate(self):
		if self.is_active and self.date_of_surrender:
			frappe.throw ("Date of surrender is set, but connection is marked as 'Is Active'.")

	def before_validate(self):
		self.clear_nonapplicable_fields()
