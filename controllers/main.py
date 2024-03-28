from odoo import http
from odoo import api, fields, models, _
from odoo.http import request


class Complaint(http.Controller):

    # public access for complaint form
    @http.route('/complaint_form', type="http", auth="public", website=True)
    def complaint_form(self, **kw):
        print("Execution.........................")
        return http.request.render('realestate_complaint.complaint_form', {})

    # public access for complaint form submission, create compliant number and see confirmation page
    @http.route('/submit_complaint', type="http", auth="public", website=True)
    def submit_complaint(self, **kw):
        print("Data received...........", kw)
        # Create the complaint record
        complaint = http.request.env['realestate.complaint'].sudo().create(kw)
        # Retrieve the complaint number
        complaint_number = complaint.complaint_reference
        return http.request.render("realestate_complaint.user_thanks", {'complaint_number': complaint_number})
