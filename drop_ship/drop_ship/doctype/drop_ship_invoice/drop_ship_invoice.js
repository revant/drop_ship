
// see license.txt

var receivable_account = "";
var income_account = "";
var pr = 0.0;


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
