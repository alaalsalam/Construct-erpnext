# Copyright (c) 2026, Sovereign IT Services and contributors
# For license information, please see license.txt

import frappe


def after_install():
    """Run safe generic setup after Construct ERPNext is installed.

    El Salvador localization disabled for generic product build.
    Country-specific tax, payroll, and fiscal setup must be enabled
    explicitly per deployment.
    """
    frappe.logger().info("Generic product setup completed.")
