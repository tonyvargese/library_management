

// frappe.ui.form.on("Library Transaction", {
//     onload(frm) {
//         // Set query for library_member field
//         frm.set_query('library_member', () => {
//             return {
//                 filters: {
//                     "membership_valid": 1
//                 }
//             }
//         })

//         // Uncomment and correct this section if needed
        
//     },
// });

frappe.ui.form.on("Library Transaction", {
    onload(frm) {
        // Set query for library_member field
        frm.set_query('library_member', () => {
            return {
                query: 'library_management.library_management.doctype.library_transaction.library_transaction.custom_query',  // Replace with the actual dotted path to your custom query method

            }
        });

        // Uncomment and correct this section if needed
        // Additional queries can be added here if required
    },
});

