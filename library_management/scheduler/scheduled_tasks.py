import frappe
from datetime import datetime, timedelta
def send_overdue_notifications():
    issued_books = frappe.get_all("Article",
        filters={"status": "Issued"},
        fields=["article_name"])
    
    for i in issued_books:
        trans_list = frappe.get_all("Library Transaction",filters={"docstatus":1})
        borrowed_books= frappe.get_all("Add Article",filters={"article":i.article_name,"parent":trans_list})

    for book in borrowed_books:
        # Calculate notification date as two days before return date
        return_date = book.date + timedelta(days=10)
        notification_date = return_date - timedelta(days=2)

        # Get current date for comparison
        current_date = datetime.now().date()

        # Check if today is two days before the return date
        if current_date == notification_date:
            send_notification_email(book)

def create_notification_log(doc, recipient, subject, content, type = None):
    ''' method is used to create notification log
        args:
            doc: document object
            recipient: notification receiving user
            subject: subject of notification log
            type: type of the notification log '''
    notification_log = frappe.new_doc('Notification Log')
    notification_log.type = 'Alert'
    if type:
        notification_log.type = type
    notification_log.document_type = doc.doctype
    notification_log.document_name = doc.name
    notification_log.for_user = recipient
    notification_log.subject = subject
    notification_log.email_content = content
    notification_log.save(ignore_permissions = True)


