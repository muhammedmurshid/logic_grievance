from odoo import models, fields, api, _
from odoo.exceptions import UserError


class GrievanceForm(models.Model):
    _name = 'grievance.form'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Grievance Form'

    name = fields.Char(string='Student Name')
    batch = fields.Many2one('logic.base.batch', string='Batch')
    # type = fields.Selection([('crash', 'Crash'), ('regular', 'Regular')], string='Type')
    mode_of_study = fields.Selection([('online', 'Online'), ('offline', 'Offline'), ('pre_recorded', 'Pre Recorded')],
                                     string='Mode of Study')
    description = fields.Text(string='Description')
    faculty = fields.Char(string="Faculty")
    course_id = fields.Many2one('logic.base.courses', string="Course")
    branch_id = fields.Many2one('logic.base.branches', string="Branch")
    coordinator = fields.Many2one('res.users', string="Assign to Coordinator", readonly=False)
    priority = fields.Selection([('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('urgent', 'Urgent')],
                                string='Priority')
    expected_resolution_date = fields.Date(string='Expected Closing')
    action_taken = fields.Text(string='Action Taken')
    phone_number = fields.Char(string="Phone Number")
    attach_file = fields.Binary(string="Attach File")
    email_address = fields.Char(string="Email")
    type_of_issue = fields.Many2one('grievance.form.type', string='Type of Issue')
    # assign_to = fields.Many2one('res.users', string='Assigned To', related='type_of_issue.assigned_to')
    # assign_to_users = fields.Many2many('res.users', string='Assigned To Users',
    #                                    related='type_of_issue.assigned_to_users')
    state = fields.Selection(
        [('draft', 'Draft'), ('assigned', 'Assigned'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled')],
        string='State', default='draft')

    def action_in_progress(self):
        self.write({'state': 'in_progress'})

    def action_assign_to_users(self):
        if self.coordinator:
            self.write({'state': 'assigned'})
        else:
            raise UserError(_('Coordinator is not assigned to this batch'))

    def action_completed(self):
        print(self.env.user.id, 'user')
        activity_id = self.env['mail.activity'].search(
            [('res_id', '=', self.id), ('user_id', '=', self.env.user.id), (
                'activity_type_id', '=', self.env.ref('logic_grievance.mail_activity_grievance_form').id)])
        activity_id.action_feedback(feedback=f'grievance has been fixed.')
        self.write({'state': 'completed'})

    def action_cancelled(self):
        activity_id = self.env['mail.activity'].search(
            [('res_id', '=', self.id), ('user_id', '=', self.env.user.id), (
                'activity_type_id', '=', self.env.ref('logic_grievance.mail_activity_grievance_form').id)])
        activity_id.action_feedback(feedback=f'grievance has been rejected.')
        self.write({'state': 'cancelled'})
