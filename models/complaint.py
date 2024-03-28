from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import random


class Complaint(models.Model):
    _name = 'realestate.complaint'
    _description = 'Tenant Complaint'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Name', required=True, tracking=True)
    email = fields.Char(string='Email', required=True, tracking=True)
    flat_address = fields.Char(string='Flat Address', required=True, tracking=True)
    complaint_type = fields.Selection([
        ('question', 'Question'),
        ('electrical_issue', 'Electrical Issue'),
        ('heating_issue', 'Heating Issue')
    ], string='Complaint Type', required=True, tracking=True)
    description = fields.Text(string='Description', tracking=True)
    complaint_number = fields.Char(string='Complaint Number', readonly=True, copy=False, tracking=True)
    state = fields.Selection([
        ('new', 'New'),
        ('in_review', 'In Review'),
        ('in_progress', 'In Progress'),
        ('solved', 'Solved'),
        ('dropped', 'Dropped')
    ], string='Stage', default='new', tracking=True)
    complaint_validity_check = fields.Selection([
        ('duplication', 'Duplication'),
        ('wrong_information', 'Wrong Information'),
        ('other', 'Other')
    ], string='Complaint Validity Check', tracking=True)
    complaint_validity_other_answer = fields.Text(string='Dropping Reason', tracking=True)
    action_plan = fields.Text(string='Action Plan', tracking=True)
    customer_service_representative = fields.Many2one('res.users', string='Customer Service Representative')

    # this field is for create unique sequence for every complaint
    complaint_reference = fields.Char(string='Sequence', required=True, copy=False, readonly=True,
                                      default=lambda self: _('New'))

    # from ir.sequence I create unique sequence for complaint model
    @api.model
    def create(self, vals):
        if vals.get('complaint_reference', _('New')) == _('New'):
            vals['complaint_reference'] = self.env['ir.sequence'].next_by_code('realestate.complaint') or _('New')

        # Automatically assign a customer service representative
        if not vals.get('customer_service_representative'):
            group = self.env.ref('realestate_complaint.group_customer_service_representative')
            users = group.users
            if users:
                vals['customer_service_representative'] = random.choice(users.ids)

        complaint = super(Complaint, self).create(vals)
        complaint_number = complaint.complaint_reference

        # Send confirmation email to the user
        try:
            template = self.env.ref('realestate_complaint.complaint_confirmation_email_template')
            template.send_mail(complaint.id, force_send=True)
        except Exception as e:
            pass
        return complaint

    # this function is for button Classify
    def action_classify(self):
        self.write({'state': 'in_review'})
        self.env['realestate.complaint'].search([('state', 'in', ['new', 'solved', 'dropped'])])
        return {
            'type': 'ir.actions.act_window',
            'name': 'Complaints in Review',
            'res_model': 'realestate.complaint',
            'view_mode': 'tree,form',
            'domain': [('state', 'in', ['new', 'solved', 'dropped'])],
            'target': 'main',
        }

    # this function is for complaint report button
    def print_complaint_report(self):
        self.write({'state': 'in_progress'})
        return self.env.ref('realestate_complaint.report_complaint').report_action(self)

    # this function is for complaint supervisor confirm button
    def supervisor_confirm(self):
        self.write({'state': 'in_progress'})

    # this function is for close button and mail sent
    def action_close(self):
        try:
            template = self.env.ref('realestate_complaint.complaint_solved_email_template')
            template.send_mail(self.id, force_send=True)
        except Exception:
            pass
        self.write({'state': 'solved'})

    # this function is for drop button and mail sent
    def action_drop(self):
        # Check if complaint validity check is provided
        if not self.complaint_validity_check:
            raise ValidationError(_("Please select a complaint validity check."))

        # If 'other' is selected, ensure dropping reason is provided
        if self.complaint_validity_check == 'other' and not self.complaint_validity_other_answer:
            raise ValidationError(_("Please provide a dropping reason."))
        try:
            template = self.env.ref('realestate_complaint.complaint_dropped_email_template')
            template.send_mail(self.id, force_send=True)
        except Exception:
            pass
        self.write({'state': 'dropped'})
