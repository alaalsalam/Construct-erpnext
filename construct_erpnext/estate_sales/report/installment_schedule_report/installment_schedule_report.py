import frappe
from frappe import _
from frappe.utils import getdate, today, flt


def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
    return columns, data


def get_columns():
    return [
        {"fieldname": "contract_number", "fieldtype": "Link", "label": _("Contract"), "options": "Sales Contract", "width": 140},
        {"fieldname": "unit", "fieldtype": "Link", "label": _("Unit"), "options": "Unit", "width": 100},
        {"fieldname": "buyer_display", "fieldtype": "Data", "label": _("Customer / Buyer"), "width": 150},
        {"fieldname": "installment_number", "fieldtype": "Data", "label": _("Installment No"), "width": 110},
        {"fieldname": "label", "fieldtype": "Data", "label": _("Label"), "width": 130},
        {"fieldname": "due_date", "fieldtype": "Date", "label": _("Due Date"), "width": 110},
        {"fieldname": "percentage", "fieldtype": "Percent", "label": _("Percent"), "width": 80},
        {"fieldname": "amount", "fieldtype": "Currency", "label": _("Amount"), "width": 120},
        {"fieldname": "installment_status", "fieldtype": "Select", "label": _("Status"), "width": 90},
        {"fieldname": "invoice_ref", "fieldtype": "Link", "label": _("Invoice"), "options": "Sales Invoice", "width": 120},
        {"fieldname": "overdue_days", "fieldtype": "Int", "label": _("Overdue Days"), "width": 100},
    ]


def get_data(filters):
    cond, values = get_conditions(filters)

    query = f"""
        SELECT
            sc.name AS contract_number,
            sc.unit,
            COALESCE(c.customer_name, sc.buyer_name) AS buyer_display,
            sis.installment_number,
            sis.label,
            sis.due_date,
            sis.percentage,
            sis.amount,
            sis.installment_status,
            sis.sales_invoice AS invoice_ref,
            CASE
                WHEN sis.installment_status IN ('Pending', 'Due', 'Overdue', 'Partial')
                     AND sis.due_date < %(today)s
                THEN DATEDIFF(%(today)s, sis.due_date)
                ELSE 0
            END AS overdue_days
        FROM `tabSales Installment Schedule` sis
        INNER JOIN `tabSales Contract` sc ON sc.name = sis.parent
        LEFT JOIN `tabCustomer` c ON c.name = sc.customer
        WHERE sc.docstatus < 2
        {cond}
        ORDER BY sc.contract_date DESC, sis.sequence ASC
    """

    values["today"] = today()
    return frappe.db.sql(query, values, as_dict=1)


def get_conditions(filters):
    conditions = []
    values = {}

    if filters.get("company"):
        conditions.append("sc.company = %(company)s")
        values["company"] = filters["company"]

    if filters.get("real_estate_project"):
        conditions.append("sc.real_estate_project = %(real_estate_project)s")
        values["real_estate_project"] = filters["real_estate_project"]

    if filters.get("sales_contract"):
        conditions.append("sc.name = %(sales_contract)s")
        values["sales_contract"] = filters["sales_contract"]

    if filters.get("customer"):
        conditions.append("sc.customer = %(customer)s")
        values["customer"] = filters["customer"]

    if filters.get("installment_status"):
        conditions.append("sis.installment_status = %(installment_status)s")
        values["installment_status"] = filters["installment_status"]

    if filters.get("from_due_date"):
        conditions.append("sis.due_date >= %(from_due_date)s")
        values["from_due_date"] = filters["from_due_date"]

    if filters.get("to_due_date"):
        conditions.append("sis.due_date <= %(to_due_date)s")
        values["to_due_date"] = filters["to_due_date"]

    return (" AND " + " AND ".join(conditions)) if conditions else "", values
