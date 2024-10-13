# Copyright (c) 2024, SMTW and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _


class ElectricityServiceConnection(Document):
	def set_title(self):
		self.title = f'{self.sc_number} [{self.campus}]'
	def set_campus(self):
		self.campus = "Campus"
	def validate(self):
		self.set_title()
		self.set_campus()
