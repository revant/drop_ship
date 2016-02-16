<!-- title: Drop Ship Invoice -->
<!-- no-breadcrumbs -->

In case of no warehouse Drop Ship business model Drop Ship Invoice is substitute for Sales Invoice. It records both supplier and customer details and details about item to be drop shipped.

> Drop Ship > Documents > Drop Ship Invoice

Drop Ship Invoices can be made from Submitted Sales Orders. On the Sales Order use "Drop Ship" button from "Make" menu.

To map with new Drop Ship Invoice from selected Sales Order use "Sales Order" from "get items from" menu

####Fill in the details of New Drop Ship Invoice.


<img class="screenshot" alt="Drop Ship Invoice" src="{{ docs_base_url }}/assets/img/drop-ship-invoice/drop-ship-invoice-1.png">
<ul>
 <li><strong>Series</strong>: Select Series</li>
 <li><strong>Date</strong>: Enter Date for Drop Ship Invoice</li>
 <li><strong>Company</strong>: Default Company is selected or select Company</li>
 <li><strong>Customer</strong>: Customer for which Drop Ship Invoice is made</li>
 <li><strong>Supplier</strong>: Supplier for which Drop Ship Invoice is made</li>
 <li><strong>Buying Price List</strong>: Select Price List to auto populate Purchase Prices for Items</li>
</ul>

<img class="screenshot" alt="Drop Ship Invoice Item" src="{{ docs_base_url }}/assets/img/drop-ship-invoice/drop-ship-invoice-item.png">
<ul>
 <li><strong>Item</strong>: Select item</li>
 <li><strong>Quantity</strong>: Enter quantity</li>
 <li><strong>Company</strong>: Default company is selected or select company</li>
 <li><strong>Purchase Rate</strong>: Enter purchase rate or it will be auto populated with selected buying price list</li>
 <li><strong>Selling Rate</strong>: Enter Selling Rate manually if not pulled from Sales Order</li>
 <li><strong>Auto generated Fields</strong>: </li>
 <ul>
 <li><strong>Purchase Rate</strong>: Fetched from selected buying price list</li>
 <li><strong>Selling Rate excluding Tax</strong>: calculated by subtracting sales tax from item rate</li>
 <li><strong>UOM</strong>: as per Item selected</li>
 <li><strong>Tax Rate</strong>: as per Set in Item Master and as per the account set in Drop Ship Settings</li>
 <li><strong>Purchase Amount</strong>: Purchase rate x quantity</li>
 <li><strong>Sales Amount</strong>: Sales rate x quantity</li>
 <li><strong>Purchase Tax Amount</strong>: Purchase amount x tax rate</li>
 <li><strong>Sales Tax Amount</strong>: Sales amount x (1 - (1/(1+(tax rate)))) i.e Sales Rate includes tax</li>
 </ul>
</ul>

<img class="screenshot" alt="Drop Ship Invoice" src="{{ docs_base_url }}/assets/img/drop-ship-invoice/drop-ship-invoice-2.png">
<ul>
 <li><strong>Posting Time</strong>: Enter posting time or default selected</li>
 <li><strong>Fiscal Year</strong>: Enter fiscal year or default is selected</li>
 <li><strong>Exchange Rate</strong>: Auto selected on save or enter rate</li>
 <li><strong>Company Currency</strong>: Enter company currency or default selected</li>
 <li><strong>Remarks</strong>: Enter remarks for GL Entry</li>
 <li><strong>Auto generated Fields</strong>: </li>
 <ul>
 <li><strong>Customer Name / Supplier Name</strong>: Auto selected as per Customer / Supplier Link</li>
 <li><strong>Customer Address / Supplier Address</strong>: Auto selected as per Customer / Supplier Link</li>
 <li><strong>Sales Total</strong>: Summation of Sales Amount</li>
 <li><strong>Purchase Total</strong>: Summation of Purchase Amount</li>
 <li><strong>Sales Tax Total</strong>: Summation of Tax Sales Tax included in Sales Price</li>
 <li><strong>Purchase Tax Total</strong>: Summation of Purchase Amount x Tax Rate</li>
 <li><strong>Commission Rate</strong>: Percentage of Total commission on Sales Total</li>
 <li><strong>Total Commission</strong>: Purchase Total subtracted from Sales Total</li>
 </ul>
</ul>


{next}

<!-- autodoc -->
<!-- jinja -->
<!-- static -->
