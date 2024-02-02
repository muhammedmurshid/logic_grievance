from odoo import http
from odoo.http import request
import base64


class GrievanceWebsiteForm(http.Controller):
    @http.route(['/grievance_form'], type='http', auth="public", website=True, csrf=False)
    def grievance_form(self):
        type = request.env['grievance.form.type'].sudo().search([])
        course = request.env['logic.base.courses'].sudo().search([('state', '=', 'done')])
        branch = request.env['logic.base.branches'].sudo().search([])
        batch = request.env['logic.base.batch'].sudo().search([])
        values = {
            'type': type,
            'course': course,
            'branch': branch,
            'batch': batch
        }
        return request.render("logic_grievance.logic_grievance_online_form", values)

    @http.route(['/grievance_form/submit'], type='http', auth="public", website=True, csrf=False)
    def grievance_form_submit(self, **kw):
        print(kw, 'ooo')
        file = kw.get('attach_file')

        request.env['grievance.form'].sudo().create({
            'name': kw.get('name'),
            'batch': kw.get('batch_id'),
            'faculty': kw.get('faculty'),
            'email_address': kw.get('email'),
            'phone_number': kw.get('phone'),
            'mode_of_study': kw.get('mode_of_study'),
            'description': kw.get('description'),
            'priority': kw.get('priority'),
            'course_id': kw.get('course_id'),
            'branch_id': kw.get('branch_id'),
            'coordinator': kw.get('coordinator'),
            # 'expected_resolution_date': kw.get('expecting_closing'),
            'attach_file': base64.b64encode(file.read()),
            'type_of_issue': kw.get('type_of_issue'),

        })
        type = request.env['grievance.form.type'].sudo().search([('id', '=', kw.get('type_of_issue'))])
        activity = request.env['grievance.form'].sudo().search([], order='id desc', limit=1)
        print(activity.name, 'activity')

        # activity.activity_schedule('grievance_form.mail_activity_grievance_form', res_id=activity.id, user_id=type.assigned_to.id,
        #                     note=f'This batch grievance added.')
        # if type.assigned_to_users:
        #     for user in type.assigned_to_users:
        #         activity.activity_schedule('grievance_form.mail_activity_grievance_form', res_id=activity.id,
        #                                    user_id=user.id,
        #                                    note=f'This batch grievance added.')

        #
        return request.render("logic_grievance.tmp_grievance_form_success", {})
