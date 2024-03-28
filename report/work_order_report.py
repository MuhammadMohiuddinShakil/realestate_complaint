from odoo import api, models, _


class ComplaintReport(models.AbstractModel):
    _name = 'report.realestate_complaint.complaint_report'
    _description = 'Complaint Report'

    @api.model
    def _get_complaint_report_values(self, docids, data=None):
        docs = self.env['realestate.complaint'].browse(docids)
        complaint_list = []
        for complaint in docs:
            vals = {
                'name': complaint.name,
                'email': complaint.email,
                'flat_address': complaint.flat_address,
                'complaint_type': complaint.complaint_type,
                'description': complaint.description,
                'complaint_number': complaint.complaint_number,
                'state': complaint.state,
                'complaint_validity_check': complaint.complaint_validity_check,
                'complaint_validity_other_answer': complaint.complaint_validity_other_answer,
                'action_plan': complaint.action_plan,
                'customer_service_representative': complaint.customer_service_representative.name,
                'complaint_reference': complaint.complaint_reference,
            }
            complaint_list.append(vals)
        return {
            'doc_model': 'realestate.complaint',
            'docs': docs,
            'complaint_list': complaint_list,
        }
