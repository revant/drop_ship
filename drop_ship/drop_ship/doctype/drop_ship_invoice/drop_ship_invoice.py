# -*- coding: utf-8 -*-
# Copyright (c) 2015, Revant Nandgaonkar and contributors
# For license information, please see license.txt


from __future__ import unicode_literals
import frappe
import frappe.defaults
from frappe.utils import cint, flt
from frappe import _, msgprint, throw
from erpnext.accounts.party import get_party_account, get_due_date
from erpnext.controllers.stock_controller import update_gl_entries_after
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

from erpnext.controllers.selling_controller import SellingController
from erpnext.accounts.utils import get_account_currency


class DropShipInvoice(Document):
	pass
	# def refresh(self):
	# 	for item in self.items:
	# 		item.amount = item.rate * item.qty
	# 		self.total = self.total + item.amount
	# 		purchase_amount = item.purchase_rate * item.qty
	# 		self.purchase_total = self.purchase_total + purchase_amount;

@frappe.whitelist()
def get_item_prices(price_list, item_code=None):

	item_price = frappe.db.get_value("Item Price", 
		{
			"price_list": price_list,
			"item_code": item_code
		}, "price_list_rate")

	if item_price:
		return item_price
	else: 
		frappe.throw(_("Item not in Price List"))

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
