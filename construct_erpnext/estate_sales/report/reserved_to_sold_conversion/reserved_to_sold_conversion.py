import frappe
from frappe import _


def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
    return columns, data


def get_columns():
    return [
        {"fieldname": "unit", "fieldtype": "Link", "label": _("Unit"), "options": "Unit", "width": 100},
        {"fieldname": "reservation_name", "fieldtype": "Link", "label": _("Reservation"), "options": "Unit Reservation", "width": 130},
        {"fieldname": "reservation_date", "fieldtype": "Date", "label": _("Reservation Date"), "width": 120},
        {"fieldname": "sales_contract", "fieldtype": "Link", "label": _("Sales Contract"), "options": "Sales Contract", "width": 140},
        {"fieldname": "contract_date", "fieldtype": "Date", "label": _("Contract Date"), "width": 120},
        {"fieldname": "conversion_days", "fieldtype": "Int", "label": _("Conversion Days"), "width": 110},
        {"fieldname": "sale_price", "fieldtype": "Currency", "label": _("Sale Price"), "width": 120},
        {"fieldname": "buyer_display", "fieldtype": "Data", "label": _("Customer / Buyer"), "width": 150},
    ]


def get_data(filters):
    cond, values = get_conditions(filters)

    query = f"""
        SELECT
            res.unit,
            res.name AS reservation_name,
            res.reservation_date,
            sc.name AS sales_contract,
            sc.contract_date,
            CASE
                WHEN sc.contract_date AND res.reservation_date
                THEN DATEDIFF(sc.contract_date, res.reservation_date)
                ELSE 0
            END AS conversion_days,
            sc.sale_price,
            COALESCE(c.customer_name, sc.buyer_name) AS buyer_display
        FROM `tabUnit Reservation` res
        INNER JOIN `tabSales Contract` sc ON sc.unit_reservation = res.name AND sc.docstatus < 2
        LEFT JOIN `tabCustomer` c ON c.name = sc.customer
        WHERE res.docstatus < 2
        AND res.status = 'Converted'
        {cond}
        ORDER BY sc.contract_date DESC, res.name DESC
    """

    return frappe.db.sql(query, values, as_dict=1)


def get_conditions(filters):
    conditions = []
    values = {}

    if filters.get("real_estate_project"):
        conditions.append("sc.real_estate_project = %(real_estate_project)s")
        values["real_estate_project"] = filters["real_estate_project"]

    if filters.get("from_date"):
        conditions.append("sc.contract_date >= %(from_date)s")
        values["from_date"] = filters["from_date"]

    if filters.get("to_date"):
        conditions.append("sc.contract_date <= %(to_date)s")
        values["to_date"] = filters["to_date"]

    return (" AND " + " AND ".join(conditions)) if conditions else "", values
