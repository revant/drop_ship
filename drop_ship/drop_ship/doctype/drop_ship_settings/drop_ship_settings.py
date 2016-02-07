# -*- coding: utf-8 -*-
# Copyright (c) 2015, Revant Nandgaonkar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class DropShipSettings(Document):

	def validate(self):
		self.validate_accounts()
		self.validate_repeating_companies()

	def validate_repeating_companies(self):
		ra_companies = []
		for entry in self.receivable_account:
			ra_companies.append(entry.company)

		if len(ra_companies)!= len(set(ra_companies)):
			frappe.throw(_("Same Company is entered more than once in Default Receivable Account"))

		ia_companies = []
		for entry in self.income_account:
			ia_companies.append(entry.company)

		if len(ia_companies)!= len(set(ia_companies)):
			frappe.throw(_("Same Company is entered more than once in Default Income Account"))

		pa_companies = []
		for entry in self.payable_account:
			pa_companies.append(entry.company)

		if len(pa_companies)!= len(set(pa_companies)):
			frappe.throw(_("Same Company is entered more than once in Default Payable Account"))

		cc_companies = []
		for entry in self.cost_center:
			cc_companies.append(entry.company)

		if len(cc_companies)!= len(set(cc_companies)):
			frappe.throw(_("Same Company is entered more than once in Default Cost Center"))

		ta_companies = []
		for entry in self.tax_account:
			ta_companies.append(entry.company)

		if len(ta_companies)!= len(set(ta_companies)):
			frappe.throw(_("Same Company is entered more than once in Tax Account"))

	def validate_accounts(self):
		"""Error when Company of Ledger account doesn't match with Company Selected"""
		for entry in self.receivable_account:
			if frappe.db.get_value("Account", entry.account, "company") != entry.company:
				frappe.throw(_("Account does not match with Company for Default Receivable Account"))

		for entry in self.income_account:
			if frappe.db.get_value("Account", entry.account, "company") != entry.company:
				frappe.throw(_("Account does not match with Company for Default Income Account"))

		for entry in self.payable_account:
			if frappe.db.get_value("Account", entry.account, "company") != entry.company:
				frappe.throw(_("Account does not match with Company for Default Payable Account"))

		for entry in self.cost_center:
			if frappe.db.get_value("Cost Center", entry.account, "company") != entry.company:
				frappe.throw(_("Cost Center does not match with Company"))

		for entry in self.tax_account:
			if frappe.db.get_value("Account", entry.account, "company") != entry.company:
				frappe.throw(_("Account does not match with Company for Default Tax Account"))

@frappe.whitelist()
def get_account(company):
	
	account_list = []
	
	income_account = frappe.db.sql("""select account from `tabDrop Ship Settings Income`
		where company = %s"""\
		,frappe.db.escape(company) , as_dict=1)

	if not income_account:
		frappe.throw(_("Set Default Income Account in Drop Ship Settings"))
	
	for item in income_account:
		account_list.append(item or "none")

	receivable_account = frappe.db.sql("""select account from `tabDrop Ship Settings Receivable`
		where company = %s"""\
		,frappe.db.escape(company) , as_dict=1)

	if not receivable_account:
		frappe.throw(_("Set Default Receivable Account in Drop Ship Settings"))

	for item in receivable_account:
		account_list.append(item or "none")

	payable_account = frappe.db.sql("""select account from `tabDrop Ship Settings Payable`
		where company = %s"""\
		,frappe.db.escape(company) , as_dict=1)

	if not payable_account:
		frappe.throw(_("Set Default Payable Account in Drop Ship Settings"))

	for item in payable_account:
		account_list.append(item or "none")

	cost_center = frappe.db.sql("""select account from `tabDrop Ship Settings Cost Center`
		where company = %s"""\
		,frappe.db.escape(company) , as_dict=1)

	if not cost_center:
		frappe.throw(_("Set Default Cost Center in Drop Ship Settings"))

	for item in cost_center:
		account_list.append(item or "none")

	tax_account = frappe.db.sql("""select account from `tabDrop Ship Settings Tax`
		where company = %s"""\
		,frappe.db.escape(company) , as_dict=1)

	if not tax_account:
		frappe.throw(_("Set Default Tax Account in Drop Ship Settings"))

	for item in tax_account:
		account_list.append(item or "none")

	return account_list
