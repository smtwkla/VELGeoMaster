# Copyright (c) 2024, SMTW and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class PropertyPayment(Document):
	def generate_title(self):
		self.title = f'{self.property} - {self.payment_type} - {self.payment_for_period}'
	def before_validate(self):
		self.generate_title()
