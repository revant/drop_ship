# -*- coding: utf-8 -*-
# Copyright (c) 2015, Revant Nandgaonkar and contributors
# For license information, please see license.txt


from __future__ import unicode_literals
import frappe
import frappe.defaults
from frappe.utils import cint, flt, cstr
from frappe import _, msgprint, throw
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from drop_ship.drop_ship.doctype.drop_ship_settings.drop_ship_settings import get_drop_ship_settings


class DropShipInvoice(Document):

	def on_update(self):
		self.calculate_totals()

	def validate(self):
		self.validate_negative_inputs()

	def on_submit(self):
		self.make_gl()

	def on_cancel(self):
		from erpnext.accounts.general_ledger import delete_gl_entries
		delete_gl_entries(voucher_type=self.doctype, voucher_no=self.name)

	def calculate_totals(self):
		total = 0.0
		purchase_total = 0.0
		sales_tax_total = 0.0
		purchase_tax_total = 0.0

		ds_settings = get_drop_ship_settings(self.company)
		for item in self.items:
			item.amount = flt(flt(item.rate) * flt(item.qty))
			if not item.purchase_rate:
				price_list_rate = frappe.db.get_value("Item Price",
				{
					"price_list": self.buying_price_list,
					"item_code": item.item_code

				}, "price_list_rate")
				if price_list_rate:
					item.purchase_rate = flt(price_list_rate)
				else:
					frappe.msgprint(_("Purchase Rate for Item {0} is not in Price List {1}".format(item.item_code, self.buying_price_list)))
			if item.purchase_rate > 0:
				item.purchase_amount = item.purchase_rate * item.qty
			else:
				frappe.throw(_("Enter Purchase Rate for Item {0}".format(item.item_code)))

			tax_rate = frappe.db.get_value("Item Tax",
				{
					"parent": item.item_code,
					"tax_type": ds_settings["tax_account"]

				}, "tax_rate")
			if tax_rate:
				item.tax_rate = flt(tax_rate)
			else:
				frappe.throw(_("Tax Rate for Item {0} is not in Item Master".format(item.item_code)))

			item.purchase_tax_amount = item.purchase_amount * (item.tax_rate/100)
			item.sales_tax_amount = item.amount * (1 - (1/(1+(item.tax_rate/100)))) # Sales Rate includes tax
			item.selling_rate_excluding_tax = item.rate - item.sales_tax_amount # Sales Rate excluding tax displayed
			total += flt(item.amount)
			purchase_total += flt(item.purchase_amount)
			sales_tax_total += flt(item.sales_tax_amount)
			purchase_tax_total += flt(item.purchase_tax_amount)

		self.total = total
		self.purchase_total = purchase_total
		self.sales_tax_total = sales_tax_total
		self.purchase_tax_total = purchase_tax_total

		self.total_commission = self.total - self.purchase_total
		self.commission_rate = (self.total_commission / self.total) * 100

	def make_gl(self):
		from erpnext.accounts.general_ledger import make_gl_entries
		gl_map = []
		ds_settings = get_drop_ship_settings(self.company)

		ia = ds_settings["income_account"]
		ra = ds_settings["receivable_account"]
		pa = ds_settings["payable_account"]
		cc = ds_settings["cost_center"]
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
				'credit': flt(flt(self.total_commission) - flt(self.purchase_tax_total)), # if self.purchase_tax_total else flt(self.total_commission)
				'debit_in_account_currency': 0,
				'credit_in_account_currency': 0,
				'is_opening': "No", # or self.get("is_opening")
				'party_type': "Supplier",
				'party': self.supplier
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
				'credit': flt(flt(self.purchase_total)  + flt(self.purchase_tax_total)), # if self.purchase_tax_total else flt(self.purchase_total),
				'debit_in_account_currency': 0,
				'credit_in_account_currency': 0,
				'is_opening': "No", # or self.get("is_opening")
				'party_type': "Supplier",
				'party': self.supplier
			})
		)
		if gl_map:
			make_gl_entries(gl_map, cancel=0, adv_adj=0)

	def validate_negative_inputs(self):
		for item in self.items:
			if item.qty <= 0 or item.rate <= 0:
				frappe.throw(_("Quantity, Purchase Rate or Selling Rate cannot be zero or negative"))

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
