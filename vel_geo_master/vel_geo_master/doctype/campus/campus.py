# Copyright (c) 2024, SMTW and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe


class Campus(Document):
	def before_validate(self):
		self.taluk = frappe.get_cached_doc('Village', self.village).taluk
		self.district = frappe.get_cached_doc('Taluk', self.taluk).district
