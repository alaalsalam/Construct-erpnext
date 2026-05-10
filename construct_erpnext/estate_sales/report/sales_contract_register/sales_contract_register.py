import frappe
from frappe import _


def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
    return columns, data


def get_columns():
    return [
        {"fieldname": "contract_number", "fieldtype": "Link", "label": _("Contract"), "options": "Sales Contract", "width": 140},
        {"fieldname": "contract_date", "fieldtype": "Date", "label": _("Contract Date"), "width": 110},
        {"fieldname": "unit", "fieldtype": "Link", "label": _("Unit"), "options": "Unit", "width": 100},
        {"fieldname": "project_name", "fieldtype": "Data", "label": _("Project"), "width": 150},
        {"fieldname": "buyer_display", "fieldtype": "Data", "label": _("Customer / Buyer"), "width": 150},
        {"fieldname": "sale_price", "fieldtype": "Currency", "label": _("Sale Price"), "width": 120},
        {"fieldname": "net_price", "fieldtype": "Currency", "label": _("Net Price"), "width": 120},
        {"fieldname": "total_installment_amount", "fieldtype": "Currency", "label": _("Installment Total"), "width": 130},
        {"fieldname": "outstanding", "fieldtype": "Currency", "label": _("Outstanding"), "width": 120},
        {"fieldname": "contract_status", "fieldtype": "Select", "label": _("Status"), "width": 100},
        {"fieldname": "workflow_state", "fieldtype": "Select", "label": _("Workflow State"), "width": 110},
    ]


def get_data(filters):
    cond, values = get_conditions(filters)

    query = f"""
        SELECT
            sc.name AS contract_number,
            sc.contract_date,
            sc.unit,
            rp.project_name_ar AS project_name,
            COALESCE(c.customer_name, sc.buyer_name) AS buyer_display,
            sc.sale_price,
            sc.net_price,
            sc.total_installment_amount,
            sc.outstanding_installment_amount AS outstanding,
            sc.contract_status,
            sc.workflow_state
        FROM `tabSales Contract` sc
        LEFT JOIN `tabReal Estate Project` rp ON rp.name = sc.real_estate_project
        LEFT JOIN `tabCustomer` c ON c.name = sc.customer
        WHERE sc.docstatus < 2
        {cond}
        ORDER BY sc.contract_date DESC, sc.name DESC
    """

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

    if filters.get("customer"):
        conditions.append("sc.customer = %(customer)s")
        values["customer"] = filters["customer"]

    if filters.get("contract_status"):
        conditions.append("sc.contract_status = %(contract_status)s")
        values["contract_status"] = filters["contract_status"]

    if filters.get("from_date"):
        conditions.append("sc.contract_date >= %(from_date)s")
        values["from_date"] = filters["from_date"]

    if filters.get("to_date"):
        conditions.append("sc.contract_date <= %(to_date)s")
        values["to_date"] = filters["to_date"]

    return (" AND " + " AND ".join(conditions)) if conditions else "", values
