# Copyright (c) 2024, SMTW and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class SurveyNumber(Document):
	def set_title(self):
		self.title = f'{self.survey_number} [{self.village}]'
	def set_total_extent(self):
		hectare = int(self.total_extent_sqm / 10000)
		are = (self.total_extent_sqm - hectare * 10000) /100
		self.total_extent = f'{hectare} - {are:0>5.2f}'
		self.total_extent_acre = round(self.total_extent_sqm / 1000 * 0.2471053815, 3)
	def before_validate(self):
		self.set_title()
		self.set_total_extent()

