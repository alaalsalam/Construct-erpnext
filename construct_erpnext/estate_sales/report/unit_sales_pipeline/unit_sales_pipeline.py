import frappe
from frappe import _


def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
    return columns, data


def get_columns():
    return [
        {"fieldname": "unit_code", "fieldtype": "Link", "label": _("Unit"), "options": "Unit", "width": 100},
        {"fieldname": "unit_type", "fieldtype": "Link", "label": _("Unit Type"), "options": "Unit Type", "width": 120},
        {"fieldname": "status", "fieldtype": "Select", "label": _("Unit Status"), "width": 100},
        {"fieldname": "reservation", "fieldtype": "Link", "label": _("Reservation"), "options": "Unit Reservation", "width": 130},
        {"fieldname": "sales_contract", "fieldtype": "Link", "label": _("Sales Contract"), "options": "Sales Contract", "width": 140},
        {"fieldname": "customer_display", "fieldtype": "Data", "label": _("Customer / Buyer"), "width": 150},
        {"fieldname": "sale_price", "fieldtype": "Currency", "label": _("Sale Price"), "width": 120},
        {"fieldname": "expected_margin", "fieldtype": "Currency", "label": _("Expected Margin"), "width": 130},
        {"fieldname": "contract_status", "fieldtype": "Select", "label": _("Contract Status"), "width": 120},
    ]


def get_data(filters):
    cond, values = get_conditions(filters)

    query = f"""
        SELECT
            u.name AS unit_code,
            u.unit_type,
            u.status,
            res.name AS reservation,
            sc.name AS sales_contract,
            COALESCE(c.customer_name, sc.buyer_name, res.party_name) AS customer_display,
            COALESCE(sc.sale_price, u.expected_sale_price) AS sale_price,
            u.expected_margin,
            sc.contract_status
        FROM `tabUnit` u
        LEFT JOIN `tabUnit Reservation` res
            ON res.unit = u.name
            AND res.status IN ('Reserved')
        LEFT JOIN `tabSales Contract` sc
            ON sc.unit = u.name
            AND sc.docstatus < 2
        LEFT JOIN `tabCustomer` c ON c.name = sc.customer
        WHERE u.docstatus < 2
        {cond}
        ORDER BY u.name ASC
    """

    return frappe.db.sql(query, values, as_dict=1)


def get_conditions(filters):
    conditions = []
    values = {}

    if filters.get("real_estate_project"):
        conditions.append("u.real_estate_project = %(real_estate_project)s")
        values["real_estate_project"] = filters["real_estate_project"]

    if filters.get("unit_status"):
        conditions.append("u.status = %(unit_status)s")
        values["unit_status"] = filters["unit_status"]

    if filters.get("contract_status"):
        conditions.append("sc.contract_status = %(contract_status)s")
        values["contract_status"] = filters["contract_status"]

    return (" AND " + " AND ".join(conditions)) if conditions else "", values
