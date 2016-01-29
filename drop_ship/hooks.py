# -*- coding: utf-8 -*-
from __future__ import unicode_literals

app_name = "drop_ship"
app_title = "Drop Ship"
app_publisher = "Revant Nandgaonkar"
app_description = "Drop Ship App for ERPNext"
app_icon = "octicon octicon-package"
app_color = "#489126"
app_email = "revant.one@gmail.com"
app_version = "0.0.1"
app_license = "GPL v3"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/drop_ship/css/drop_ship.css"
# app_include_js = "/assets/drop_ship/js/drop_ship.js"

# include js, css files in header of web template
# web_include_css = "/assets/drop_ship/css/drop_ship.css"
# web_include_js = "/assets/drop_ship/js/drop_ship.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "drop_ship.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "drop_ship.install.before_install"
# after_install = "drop_ship.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "drop_ship.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"drop_ship.tasks.all"
# 	],
# 	"daily": [
# 		"drop_ship.tasks.daily"
# 	],
# 	"hourly": [
# 		"drop_ship.tasks.hourly"
# 	],
# 	"weekly": [
# 		"drop_ship.tasks.weekly"
# 	]
# 	"monthly": [
# 		"drop_ship.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "drop_ship.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "drop_ship.event.get_events"
# }

fixtures = ["Custom Script"]
