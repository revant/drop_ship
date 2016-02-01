
// see license.txt

var receivable_account = "";
var income_account = "";
var pr = 0.0;

calculate_totals = function(doc) {
	var items = doc.items || [];
	doc.purchase_total = 0.0;
	doc.total = 0.0;
	for(var i=0;i<items.length;i++) {
		frappe.call({
        	method: "frappe.client.get",
        	args: {
        		doctype: "Item Price",
        		filters: {
        			"price_list": doc.price_list,
        			"item_code": items[i].item_code
        		}
        	},
        	callback: function (data) {
				pr = data.message.price_list_rate;
  	    	}
    	});
    	items[i].purchase_rate = flt(pr);
		refresh_field('purchase_rate', doc.items);
		items[i].amount = flt(flt(items[i].rate) * flt(items[i].qty));
		doc.total += items[i].amount;
		items[i].purchase_amount = flt(flt(items[i].purchase_rate) * flt(items[i].qty));
		doc.purchase_total += items[i].purchase_amount;
	}
	doc.total_commission = doc.total - doc.purchase_total;
	doc.commission_rate = ((doc.total - doc.purchase_total) / doc.total) * 100;
	refresh_field('purchase_total');
	refresh_field('total');
	refresh_field('purchase_amount');
	refresh_field('purchase_rate', doc.items);
}

get_items_from_so = function() {
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

cur_frm.cscript.refresh = function(doc, dt, dn) {
	calculate_totals(doc);
}

frappe.ui.form.on("Drop Ship Invoice", {
	onload: function(frm) {
		frappe.call({
        	method: "drop_ship.drop_ship.doctype.drop_ship_settings.drop_ship_settings.get_account",
        	args: {
        		company: frm.doc.company
        	},
        	callback: function (data) {
        		receivable_account = data.message[0].account;
				income_account = data.message[1].account;
        		if(!receivable_account){
	        		msgprint (__("Set Receivable account in Drop Ship Settings"));
        		}
        		if(!income_account){
	        		msgprint (__("Set Income account in Drop Ship Settings"));
        		}
        	}
    	});
	}
});

cur_frm.add_fetch("item_code", "stock_uom", "stock_uom");
