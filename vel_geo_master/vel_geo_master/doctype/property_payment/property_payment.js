// Copyright (c) 2024, SMTW and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Property Payment", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on("Property Payment", {
	setup: function (frm) {
			frm.set_query("property_type", function () {
				return {
					filters: {
						name: ["in", ["Building", "Electricity Service Connection", "Survey Number", "Telephone Connection", "Water Supply Connection", "Land Patta"]],
					},
				};
			});

	},

});

frappe.ui.form.on("Property Payment", {
    onload: function(frm) {
		frm.set_query('property_type', 'properties', ()=>{
		    return{
		        filters:{
		            name: ["in", ["Building", "Electricity Service Connection", "Survey Number", "Telephone Connection", "Water Supply Connection", "Land Patta"]],
		        }
		    }
		})
	}
})
