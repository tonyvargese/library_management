
import frappe

# def after_migrate ():
#     print("migrated successfully")


def after_insert(doc, method):
    if doc.doctype=="User":
        frappe.msgprint(f"new user printed sucessfully: {doc.first_name} , {doc.email}")

def before_insert(doc, method):
    if doc.doctype == "Library Member":
        if doc.last_name == "P":
            doc.last_name = "KPP"