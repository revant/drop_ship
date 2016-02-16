"""
Configuration for docs
"""

source_link = "https://github.com/revant/drop_ship"
docs_base_url = "https://revant.github.io/drop_ship"
headline = "Drop Ship App for ERPNext"
sub_heading = "Sponsored by Supplify.com"
long_description = """
Drop Ship:

 1. Supplier delivers to Customer
 1. Material never reaches any company warehouse
 1. Only GL is affected no effect on Stock
 1. Tax implications will be added later

Accounting Entries

- Receivable account Dr .... Total selling price
	- To Income account .... Total selling price - (Purchase price + Purchase tax)
	- To Payable account .... Purchase price total + Purchase tax total

"""

def get_context(context):
    # optional settings

    context.brand_html = 'Drop Ship'
    # context.favicon = 'path to favicon'
    #
    # context.top_bar_items = [
    #   {"label": "About", "url": context.docs_base_url + "/about"},
    # ]
