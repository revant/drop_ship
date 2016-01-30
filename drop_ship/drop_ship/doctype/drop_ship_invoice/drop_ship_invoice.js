// see license.txt
calculate_totals = function(doc) {
	var items = doc.items || [];
	doc.total_purchase = 0.0;
	doc.total_sales = 0.0;
	for(var i=0;i<items.length;i++) {
		//if (!items[i].purchase_rate){
		//	items[i].purchase_rate = doc.purchase_rate;
		//}
		items[i].selling_amount = flt(flt(items[i].rate) * flt(items[i].qty));
		doc.total_sales += items[i].selling_amount;
		items[i].purchase_amount = flt(flt(items[i].purchase_rate) * flt(items[i].qty));
		doc.total_purchase += items[i].purchase_amount;
	}

	refresh_field('total_purchase');
	refresh_field('total_sales');
}

frappe.ui.form.on("Drop Ship Invoice", {
	refresh: function(doc, dt, dn) {
		cur_frm.add_custom_button(__('Sales Order'), this.sales_order_btn, __("Get items from"));
		calculate_totals(doc);
	},
	sales_order_btn: function() {
		this.$sales_order_btn = cur_frm.add_custom_button(__('Sales Order'),
			function() {
				frappe.model.map_current_doc({
					method: "erpnext.selling.doctype.sales_order.sales_order.make_sales_invoice",
					source_doctype: "Sales Order",
					get_query_filters: {
						docstatus: 1,
						status: ["not in", ["Stopped", "Closed"]],
						per_billed: ["<", 99.99],
						customer: cur_frm.doc.customer || undefined,
						company: cur_frm.doc.company
					}
				})
			}, __("Get items from"));
	},
	get_items_from_so: function() {
		frappe.model.map_current_doc({
			method: "drop_ship.drop_ship.doctype.drop_ship_invoice.drop_ship_invoice.make_drop_ship_invoice",
			source: cur_frm.doc.name,
			get_query_filters: {
				docstatus: 1,
				status: ["not in", ["Stopped", "Closed"]],
				per_billed: ["<", 99.99],
				customer: cur_frm.doc.customer || undefined,
				company: cur_frm.doc.company
			}
		})
	}
});

cur_frm.add_fetch("item_code", "item_name", "item_name");
cur_frm.add_fetch("item_code", "description", "description");
cur_frm.add_fetch("item_code", "stock_uom", "stock_uom");


//cur_frm.cscript.refresh = function(doc, dt, dn) {
	/*if(!doc.__islocal) {
		if(doc.docstatus==1 && frappe.model.can_create("Journal Entry")){
    		cur_frm.add_custom_button(__("Make Journal Entry"), make_journal_entry, frappe.boot.doctype_icons["Journal Entry"]);
    	}
    }*/
    
//}
