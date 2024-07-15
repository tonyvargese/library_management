# Copyright (c) 2024, priyanka and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    columns, data = [], []
    columns = [
        {
            'fieldname': 'name',
            'label': _('Member ID'),
            'fieldtype': 'Link',
            'options':'Library Member'
        },
        {
            'fieldname': 'full_name',
            'label': _('Name'),
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'email_address',
            'label': _('Email'),
            'fieldtype': 'Data',
        },
    #   {
    #       'fieldname': 'status',
    #       'label': _('Status'),
    #       'fieldtype': 'Select',
    #       'options': ['Issued','Available'],
    #   },
    #   {
    #       'fieldname': 'isbn',
    #       'label': _('ISBN'),
    #       'fieldtype': 'Data',
    #   },
    #   {
    #       'fieldname': 'publisher',
    #       'label': _('Publisher'),
    #       'fieldtype': 'Data',
    #   }
        {
            'fieldname': 'membership_count',
            'label': _('Membership Count'),
            'fieldtype': 'Int',
        },
        {
            'fieldname': 'late_membership',
            'label': _('Membership Status'),
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'membership_from',
            'label': _('From Date'),
            'fieldtype': 'Date',
        },
        {
            'fieldname': 'membership_to',
            'label': _('To Date'),
            'fieldtype': 'Date',
        },
        {
            'fieldname': 'transaction_count',
            'label': _('Transaction Count'),
            'fieldtype': 'Data',
        },

    ]
    # article_list = frappe.db.get_all('Article',fields=['name','author','status','isbn','publisher','price'])
     
    # sub_trans = frappe.db.get_list("Library Transaction",{"docstatus":1},pluck="name")

    # for i in article_list:
    #   Issue_count = frappe.db.count("Add Article",{"article":i.name, "type":"Issue","parent":["in",sub_trans]})
    #   Return_count = frappe.db.count("Add Article",{"article":i.name, "type":"Return","parent":["in",sub_trans]})
    
    #   data.append({
    #        'name': i.name,
    #        'author': i.author,
    #        'status': i.status,
    #        'isbn': i.isbn,
    #        'publisher': i.publisher,
    #        'price': i.price,
    #        'issue_count': Issue_count,
    #        'return_count': Return_count
    #   })
    member_list = frappe.db.get_all('Library Member',fields=['name','full_name','email_address'])
    for i in member_list:
        Membership_count = frappe.db.count("Library Membership",{"library_member":i.name,'docstatus': 1})
        valid_membership = frappe.db.exists(
            "Library Membership",
            {
                "library_member": i["name"],
                "docstatus": 1,
                "from_date": ("<=", frappe.utils.nowdate()),
                "to_date": (">=", frappe.utils.nowdate()),
            }
        )
        membership_status = "Valid Membership" if valid_membership else "No Membership"
        check_membership =frappe.db.exists("Library Membership",{"library_member":i.name,"docstatus":1})
        from_date, to_date = None, None
        if check_membership:
            membership_from =frappe.get_last_doc("Library Membership",{"library_member":i.name },order_by="from_date asc")
            from_date, to_date = membership_from.from_date, membership_from.to_date

        Transaction_count = frappe.db.count("Library Transaction",{"library_member":i.name,'docstatus': 1})
        data.append({
             'name': i.name,
             'full_name': i.full_name,
             'email_address': i.email_address,
             'membership_count': Membership_count,
             'late_membership': membership_status,
             'membership_from':from_date,
             'membership_to':to_date,
             'transaction_count': Transaction_count,
            #  'return_count': Return_count
        })

    return columns, data