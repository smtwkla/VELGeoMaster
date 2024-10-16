# Copyright (c) 2024, SMTW and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe


class Village(Document):
	def before_validate(self):
		self.district = frappe.get_doc('Taluk',self.taluk).district
