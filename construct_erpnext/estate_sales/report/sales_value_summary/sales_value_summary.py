import frappe
from frappe import _


def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
    return columns, data


def get_columns():
    return [
        {"fieldname": "project_name", "fieldtype": "Data", "label": _("Project"), "width": 180},
        {"fieldname": "contract_count", "fieldtype": "Int", "label": _("Contracts"), "width": 90},
        {"fieldname": "contracted_sales_value", "fieldtype": "Currency", "label": _("Contracted Sales Value"), "width": 150},
        {"fieldname": "scheduled_installment", "fieldtype": "Currency", "label": _("Scheduled Installment"), "width": 150},
        {"fieldname": "pending_scheduled", "fieldtype": "Currency", "label": _("Pending Scheduled"), "width": 140},
        {"fieldname": "sold_units", "fieldtype": "Int", "label": _("Sold Units"), "width": 100},
        {"fieldname": "reserved_units", "fieldtype": "Int", "label": _("Reserved Units"), "width": 110},
    ]


def get_data(filters):
    cond, values = get_conditions(filters)

    query = f"""
        SELECT
            COALESCE(rp.project_name_ar, sc.real_estate_project) AS project_name,
            COUNT(DISTINCT sc.name) AS contract_count,
            SUM(sc.net_price) AS contracted_sales_value,
            SUM(sc.total_installment_amount) AS scheduled_installment,
            SUM(sc.outstanding_installment_amount) AS pending_scheduled,
            COUNT(DISTINCT CASE WHEN u.status = 'Sold' THEN u.name END) AS sold_units,
            COUNT(DISTINCT CASE WHEN u.status = 'Reserved' THEN u.name END) AS reserved_units
        FROM `tabSales Contract` sc
        LEFT JOIN `tabReal Estate Project` rp ON rp.name = sc.real_estate_project
        LEFT JOIN `tabUnit` u ON u.real_estate_project = sc.real_estate_project
        WHERE sc.docstatus < 2
        {cond}
        GROUP BY
            COALESCE(rp.project_name_ar, sc.real_estate_project)
        ORDER BY project_name ASC
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
