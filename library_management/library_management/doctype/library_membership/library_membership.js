frappe.ui.form.on('Library Membership', {
    from_date: function(frm) {
        if (frm.doc.from_date && frm.doc.to_date && (frm.doc.from_date > frm.doc.to_date)) {
            frm.set_value('from_date', "");
            frappe.throw({
                message: ("തിയതി ആരംഭം അവസാന തിയതിയേക്കാൾ മുമ്പായിരിക്കണം"),
                indicator: 'red'
            });
        }
    },
    to_date: function(frm) {
        if (frm.doc.from_date && frm.doc.to_date && (frm.doc.from_date > frm.doc.to_date)) {
            frm.set_value('to_date', "");
            frappe.throw({
                message: ("തിയതി ആരംഭം അവസാന തിയതിയേക്കാൾ മുമ്പായിരിക്കണം"),
                indicator: 'red'
            });
        }
    }
});
