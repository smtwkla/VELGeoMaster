# Copyright (c) 2024, SMTW and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _


class ElectricityServiceConnection(Document):
	def before_validate(self):
		self.title = f'{self.sc_name} - {self.sc_number}'
