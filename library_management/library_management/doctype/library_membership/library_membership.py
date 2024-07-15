import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus

class LibraryMembership(Document):
    # check before submitting this document
    def validate(self):
        self.validate_date()

    def before_submit(self):
        # Ensure from_date is before recalculated to_date after getting the loan period
        loan_period = frappe.db.get_single_value("Library Settings", "loan_period")
        self.to_date = frappe.utils.add_days(self.from_date, loan_period or 30)
        
        if self.from_date > self.to_date:
            frappe.throw(title='Error', msg='From Date must be before To Date')

        # Check if there is an active membership for the same member
        exists = frappe.db.exists(
            "Library Membership",
            {
                "library_member": self.library_member,
                "docstatus": DocStatus.submitted(),
                # Check if the membership's end date is later than this membership's start date
                "to_date": (">", self.from_date),
            },
        )
        if exists:
            frappe.throw(title='Error', msg="There is an active membership for this member")
    def validate_date(self):
        if self.from_date > self.to_date :
            frappe.throw("from date is greater thsn to date")
