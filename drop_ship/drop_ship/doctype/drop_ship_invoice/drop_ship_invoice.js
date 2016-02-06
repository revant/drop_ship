
// see license.txt

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

cur_frm.add_fetch("item_code", "stock_uom", "stock_uom");
