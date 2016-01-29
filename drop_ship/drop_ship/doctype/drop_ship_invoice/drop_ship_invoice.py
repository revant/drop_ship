# -*- coding: utf-8 -*-
# Copyright (c) 2015, Revant Nandgaonkar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from erpnext.controllers.selling_controller import SellingController
from frappe.utils import cstr, flt

class DropShipInvoice(SellingController):
    def on_submit(self):
    	self.make_gl()
    	
    def on_cancel(self):
    	delete_gl_entries(voucher_type=self.doctype, voucher_no=self.name)

    def make_gl(self):
    	""" # example Passing GL Entry directly on Submit
    	from erpnext.accounts.general_ledger import make_gl_entries
        gl_map = []

        gl_map.append(
            frappe._dict({
            	"posting_date":self.posting_date,
            	"fiscal_year":self.fiscal_year,
                "account": "Debtors - MNT",
                "party_type": "Customer",
                "party": "Akshay Bungalow",
                "debit": flt(0),
                "credit": flt(10000),
                "remarks": "Test Journal",
                "voucher_type": self.doctype,
                "voucher_no": self.name
            })
        )

        gl_map.append(
            frappe._dict({
            	"posting_date":self.posting_date,
            	"fiscal_year":self.fiscal_year,
                "account": "Cash - MNT",
                "debit": flt(10000),
                "credit": flt(0),
                "remarks": "Test Journal",
				"voucher_type": self.doctype,
                "voucher_no": self.name
            })
        )

        if gl_map:
            make_gl_entries(gl_map, cancel=0, adv_adj=0)
        """

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
		target.run_method("calculate_taxes_and_totals")

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
		#},
		#"Sales Taxes and Charges": {
		#	"doctype": "Sales Taxes and Charges",
		#	"add_if_empty": True
		#},
		#"Sales Team": {
		#	"doctype": "Sales Team",
		#	"add_if_empty": True
		}
	}, target_doc, postprocess, ignore_permissions=ignore_permissions)

	return doclist