# -*- coding: utf-8 -*-
# Copyright (c) 2015, Revant Nandgaonkar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class DropShipSettings(Document):
	pass

@frappe.whitelist()
def get_account(company):
	
	account_list = []
	
	receivable_account = frappe.db.sql("""select account from `tabDrop Ship Settings Receivable`
		where company = %s"""\
		,company , as_dict=1)

	if not receivable_account:
		receivable_account = {"account":"none"}

	income_account = frappe.db.sql("""select account from `tabDrop Ship Settings Income`
		where company = %s"""\
		,company , as_dict=1)

	if not income_account:
		income_account = {"account":"none"}
	
	for item in receivable_account:
		account_list.append(item or "none")

	for item in income_account:
		account_list.append(item or "none")

	return account_list