
// see license.txt
frappe.ui.form.on(cur_frm.doctype, {
refresh: function(doc) {
		cur_frm.add_custom_button(__('Sales Order'),
			function() {
			frappe.model.map_current_doc({
				method: "drop_ship.drop_ship.doctype.drop_ship_invoice.drop_ship_invoice.make_drop_ship_invoice",
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
});

cur_frm.add_fetch("item_code", "stock_uom", "stock_uom");
cur_frm.add_fetch("customer", "customer_name", "customer_name");
cur_frm.add_fetch("supplier", "supplier_name", "supplier_name");
