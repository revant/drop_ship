// License: See license.txt

/* Set Account Selection filter to show only Ledgers with group_or_ledger is "Ledger" */

cur_frm.set_query("account", "receivable_account", function(doc, cdt, cdn) {
   return{
      filters: [
         ['Account', 'is_group', '=', 0],
      ]
   }
});

cur_frm.set_query("account", "income_account", function(doc, cdt, cdn) {
   return{
      filters: [
         ['Account', 'is_group', '=', 0],
      ]
   }
});

cur_frm.set_query("account", "payable_account", function(doc, cdt, cdn) {
   return{
      filters: [
         ['Account', 'is_group', '=', 0],
      ]
   }
});

cur_frm.set_query("account", "cost_center", function(doc, cdt, cdn) {
   return{
      filters: [
         ['Cost Center', 'is_group', '=', 0],
      ]
   }
});

cur_frm.set_query("account", "tax_account", function(doc, cdt, cdn) {
   return{
      filters: [
         ['Account', 'is_group', '=', 0],
      ]
   }
});
