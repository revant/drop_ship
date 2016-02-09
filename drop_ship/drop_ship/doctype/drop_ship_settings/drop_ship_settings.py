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
def get_drop_ship_settings(company):
	"""Return Drop Ship Settings for Company -
	income_account, receivable_account, payable_account, tax_account and cost_center"""

	out = {
		"income_account" : frappe.db.get_value("Drop Ship Settings Income",
		{
			"company": company
		}, "account"),
		"receivable_account" :frappe.db.get_value("Drop Ship Settings Receivable",
		{
			"company": company
		}, "account"),
		"payable_account" :frappe.db.get_value("Drop Ship Settings Payable",
		{
			"company": company
		}, "account"),
		"tax_account" :frappe.db.get_value("Drop Ship Settings Tax",
		{
			"company": company
		}, "account"),
		"cost_center" :frappe.db.get_value("Drop Ship Settings Cost Center",
		{
			"company": company
		}, "account"),
	}

	if not out["income_account"]:
		frappe.throw(_("Set Default Income Account in Drop Ship Settings"))

	if not out["receivable_account"]:
		frappe.throw(_("Set Default Receivable Account in Drop Ship Settings"))

	if not out["payable_account"]:
		frappe.throw(_("Set Default Payable Account in Drop Ship Settings"))

	if not out["tax_account"]:
		frappe.throw(_("Set Default Tax Account in Drop Ship Settings"))

	if not out["cost_center"]:
		frappe.throw(_("Set Default Cost Center in Drop Ship Settings"))

	return out
