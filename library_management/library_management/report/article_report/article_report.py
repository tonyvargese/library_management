from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
    columns = [
        {
            'fieldname': 'article_name',
            'label': _('Article name'),
            'fieldtype': 'Data',

            
        },
        {
            'fieldname': 'status',
            'label': _('Status'),
            'fieldtype': 'Select',
            'options': "\n Available\n Issued"
        },
        
        {
            'fieldname': 'isbn',
            'label': _('ISBN'),
            'fieldtype': 'Data',

            "width" : 400
        },
        
        
        {
            'fieldname': 'publisher',
            'label': _('Publisher'),
            'fieldtype': 'Data',
            'width':450
        }
    ]
    

    data = frappe.db.get_list("Article", fields=["article_name","status","isbn","publisher"])

    return columns, data