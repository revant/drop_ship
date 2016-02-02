# -*- coding: utf-8 -*-
# Copyright (c) 2015, Revant Nandgaonkar and contributors
# For license information, please see license.txt


from __future__ import unicode_literals
import frappe
import frappe.defaults
from frappe.utils import cint, flt, cstr
from frappe import _, msgprint, throw
from erpnext.accounts.party import get_party_account, get_due_date
from erpnext.controllers.stock_controller import update_gl_entries_after
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

from erpnext.controllers.selling_controller import SellingController
from erpnext.accounts.utils import get_account_currency
from erpnext.controllers.accounts_controller import AccountsController

class DropShipInvoice(Document):

	def on_submit(self):
		self.make_gl()
		     	
	def on_cancel(self):
		from erpnext.accounts.general_ledger import delete_gl_entries
		delete_gl_entries(voucher_type=self.doctype, voucher_no=self.name)
  		  
	def make_gl(self):
		from erpnext.accounts.general_ledger import make_gl_entries
		gl_map = []
		accounts_list = self.get_account(self.company)

		ia = accounts_list[0].account
		ra = accounts_list[1].account
		pa = accounts_list[2].account
		cc = accounts_list[3].account
		gl_map.append(
			frappe._dict({
				'company': self.company,
				'posting_date': self.posting_date,
				'voucher_type': self.doctype,
				'voucher_no': self.name,
				'remarks': self.get("remarks"),
				'fiscal_year': self.fiscal_year,
				'account': ia,
				'cost_center': cc,
				'debit': flt(0),
				'credit': flt(self.total_commission),
				'debit_in_account_currency': 0,
				'credit_in_account_currency': 0,
				'is_opening': "No", # or self.get("is_opening")
				'party_type': None,
				'party': None
			})
		)
		gl_map.append(
			frappe._dict({
				'company': self.company,
				'posting_date': self.posting_date,
				'voucher_type': self.doctype,
				'voucher_no': self.name,
				'remarks': self.get("remarks"),
				'fiscal_year': self.fiscal_year,
				'account': ra,
				'debit': flt(self.total),
				'credit': flt(0),
				'debit_in_account_currency': 0,
				'credit_in_account_currency': 0,
				'is_opening': "No", # or self.get("is_opening")
				'party_type': "Customer",
				'party': self.customer
			})
		)
		gl_map.append(
			frappe._dict({
				'company': self.company,
				'posting_date': self.posting_date,
				'voucher_type': self.doctype,
				'voucher_no': self.name,
				'remarks': self.get("remarks"),
				'fiscal_year': self.fiscal_year,
				'account': pa,
				'debit': flt(0),
				'credit': flt(self.purchase_total),
				'debit_in_account_currency': 0,
				'credit_in_account_currency': 0,
				'is_opening': "No", # or self.get("is_opening")
				'party_type': "Supplier",
				'party': self.supplier
			})
		)
		if gl_map:
			make_gl_entries(gl_map, cancel=0, adv_adj=0)

	def get_account(self, company):
	
		account_list = []
		
		income_account = frappe.db.sql("""select account from `tabDrop Ship Settings Income`
			where company = %s"""\
			, frappe.db.escape(company) , as_dict=1)

		if not income_account:
			income_account = {"account":"none"}

		receivable_account = frappe.db.sql("""select account from `tabDrop Ship Settings Receivable`
			where company = %s"""\
			, frappe.db.escape(company) , as_dict=1)

		if not receivable_account:
			receivable_account = {"account":"none"}
		
		payable_account = frappe.db.sql("""select account from `tabDrop Ship Settings Payable`
			where company = %s"""\
			,company , as_dict=1)

		if not payable_account:
			payable_account = {"account":"none"}
		
		cost_center = frappe.db.sql("""select account from `tabDrop Ship Settings Cost Center`
			where company = %s"""\
			,company , as_dict=1)

		if not cost_center:
			cost_center = {"account":"none"}
		
		for item in income_account:
			account_list.append(item or "none")

		for item in receivable_account:
			account_list.append(item or "none")

		for item in payable_account:
			account_list.append(item or "none")

		for item in cost_center:
			account_list.append(item or "none")

		return account_list

@frappe.whitelist()
def get_price(self, price_list, item_code=None):
	if not price_list:
		frappe.throw(_("Select Price List"))
	if not item_code:
		frappe.throw(_("Select Item"))

	return frappe.db.get_value("Item Price", {
	 			"item_code":item_code,
	 			"price_list":price_list
	 		}, "price_list_rate")

@frappe.whitelist()
def make_drop_ship_invoice(source_name, target_doc=None, ignore_permissions=False):
	def postprocess(source, target):
		set_missing_values(source, target)
		#Get the advance paid Journal Entries in Sales Invoice Advance
		#target.get_advances()

	def set_missing_values(source, target):
		target.is_pos = 0
		target.ignore_pricing_rule = 1
		target.flags.ignore_permissions = True
		target.run_method("set_missing_values")
		# target.run_method("calculate_taxes_and_totals")

	def update_item(source, target, source_parent):
		target.amount = flt(source.amount) - flt(source.billed_amt)
		target.base_amount = target.amount * flt(source_parent.conversion_rate)
		target.qty = target.amount / flt(source.rate) if (source.rate and source.billed_amt) else source.qty

	doclist = get_mapped_doc("Sales Order", source_name, {
		"Sales Order": {
			"doctype": "Drop Ship Invoice",
			"validation": {
				"docstatus": ["=", 1]
			}
		},
		"Sales Order Item": {
			"doctype": "Drop Ship Invoice Item",
			"field_map": {
				"name": "so_detail",
				"parent": "sales_order",
			},
			"postprocess": update_item,
			"condition": lambda doc: doc.qty and (doc.base_amount==0 or abs(doc.billed_amt) < abs(doc.amount))
		},
		"Sales Taxes and Charges": {
			"doctype": "Sales Taxes and Charges",
			"add_if_empty": True
		}
	}, target_doc, postprocess, ignore_permissions=ignore_permissions)

	return doclist
