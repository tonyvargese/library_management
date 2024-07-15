import frappe
from frappe.model.document import Document
# from datetime import date, timedelta
from frappe.utils import date_diff, getdate
from frappe.utils import nowdate

class LibraryTransaction(Document):
    def before_submit(self):
        #check for the emptiness
        #If the add_articles field is empty, the not operator set condition to True
        if not self.add_articles:
            frappe.throw("At least one article must be added before submitting")
        for i in self.add_articles:
            if i.type_tran == "Issue":
                self.validate_issue()
                self.validate_maximum_limit()
        #    i is article_entry or denote each article entered in the add_articles field 
# get value from db in article which matches the value of  i.article             
                article = frappe.get_doc("Article", i.article)
                article.status = "Issued"
                article.save()

            elif i.type_tran == "Return":
                self.validate_return()
                article = frappe.get_doc("Article", i.article)
                article.status = "Available"
                article.save()

    def validate_issue(self):
        self.validate_membership()
        for i in self.add_articles:
            article = frappe.get_doc("Article", i.article)
            if article.status == "Issued":
                frappe.throw(f"Article {article.name} is already issued by another member")

    def validate_return(self):
        for i in self.add_articles:
            article = frappe.get_doc("Article", i.article)
            if article.status == "Available":
                frappe.throw(f"Article {article.name} cannot be returned without being issued first")

    def validate_maximum_limit(self):
#get single value of max_articles from library seetings doctype 
        max_articles = frappe.db.get_single_value("Library Settings", "max_articles")
        count =0
        issued_tran = frappe.get_all(
                        "Library Transaction",
                        filters={"library_member": self.library_member,
                        "docstatus": 1},
                        fields=["name"],
                        )
        print(issued_tran)
        for tran in issued_tran:
            
            if frappe.db.exists(
                "Article Child",
                {
                "type_tran": "Issue",
                "parent":tran["name"]
                },
            ):
                count += 1
  
        print (count)
        if count + len(self.add_articles) > max_articles:
            frappe.throw("Maximum limit reached for issuing articles")

    def validate_membership(self):
        valid_membership = frappe.db.exists(
            "Library Membership",
            {
                "library_member": self.library_member,
                "docstatus": 1,
                "from_date": ("<", self.date),
                "to_date": (">", self.date),
            },
        )
        if not valid_membership:
            frappe.throw("The member does not have a valid membership")
    def before_save(self):
        for i in self.add_articles:
            print("hello")

            if i.type_tran == "Return":  # Only proceed for "Return" transactions
                print("hai")
            # damage_level = self.get('fines')
                damage_fine = frappe.db.get_single_value("Library Settings", "damage_fine")
                lost_fine = frappe.db.get_single_value("Library Settings", "lost_fine")
                borrow_period = frappe.db.get_single_value("Library Settings", "borrow_period")
                fine_per_day = frappe.db.get_single_value("Library Settings", "fine_day")

                total_damage_fine = 0
                total_late_fine = 0  # Initialize total_late_fine outside the loop

                issued_transactions = frappe.get_all(
                        "Library Transaction",
                        filters={"library_member": self.library_member, "docstatus": 1},
                        fields=["name","date"],
                        order_by = "date desc"
                        )
                print("hai")
                print(issued_transactions)
                issue_date = None
                for transaction in issued_transactions:
                    if frappe.db.exists("Article Child", {"article":i.article, "type_tran": "Issue", "parent":transaction["name"]}):
                        print("here?")
                        issue_date = transaction["date"]
                        print(issue_date)
                        break
                if issue_date:
                    print("koi")
                    overdue_days = date_diff(getdate(self.date), getdate(issue_date)) - borrow_period
                    late_fine = 0  # Initialize late_fine within the loop
                    if overdue_days > 0:
                        late_fine = overdue_days * fine_per_day
                        print(late_fine)
                    total_late_fine += late_fine  # Add late_fine to total_late_fine
                
                article = frappe.get_doc("Article", i.article)
                price = article.price
                damage_level = i.get('fine_type')
                # Fine calculation based on damage level
                
                if damage_level == "Damage":
                    dfine = price * damage_fine
                elif damage_level == "Lost":
                    dfine = price * lost_fine
                else:
                    dfine = 0
                print(dfine)

                fine = dfine + total_late_fine
                print(fine)
                print(f"{fine} is the Fine for article {i.article}")
                # self.fine = fine
                # frappe.db.set_value('fine',fine)
                # frappe.db.set_value("Article Child",add_articles.fine, fine)
                print(self.fine+1)
                self.tfine += fine
                print(self.tfine+2)
            else:
                self.fine = 0  
@frappe.whitelist()
def custom_query(doctype, txt, searchfield, start, page_len, filters):
    today = nowdate()
    
    # list=[
    print(today)            
            
    valid_member = frappe.get_all(
            "Library Membership",
            filters={
                    "from_date": ("<=", today),
                    "to_date": (">=", today)
                    },
            pluck="library_member",
    )
    print(valid_member)
    return [[member] for member in valid_member] or []

# [[1][2]]
        # ]

# from_date < self.date AND
# to_date > self.date
