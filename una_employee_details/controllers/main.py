from odoo import http
from odoo.http import request

class EmployeeOnboardingRedirect(http.Controller):

    @http.route('/web', type='http', auth="user", website=True)
    def web_client(self, **kwargs):
        # Check onboarding status after login
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.uid)], limit=1)

        if employee:
            required_fields = [
                'onboarding_cv_attachment_ids',
                'onboarding_medical_attachment_ids',
                'onboarding_police_report_attachment_ids',
                'onboarding_credentials_attachment_ids',
                'onboarding_passport_photo_attachment_ids',
                'onboarding_bond_ack_attachment_ids',
                'onboarding_loe_ack_attachment_ids',
                'onboarding_employment_form_attachment_ids',
                'onboarding_background_check_attachment_ids'
            ]

            missing = all(len(getattr(employee, f)) == 0 for f in required_fields)
            if missing:
                return request.redirect('/onboarding/check_missing_popup')

        return request.redirect('/web')

    @http.route('/onboarding/check_missing_popup', type='http', auth="user")
    def onboarding_check_missing_popup(self, **kwargs):
        action = request.env.ref('una_employee_details.action_onboarding_upload_wizard').sudo()
        return request.render('web.webclient_bootstrap', {
            'action': {
                'type': 'ir.actions.act_window',
                'name': 'Complete Onboarding',
                'res_model': 'onboarding.upload.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {},
            }
        })



class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def _login_successful(self, user, access_token=None):
        employee = self.env['hr.employee'].search([('user_id', '=', user.id)], limit=1)
        if employee:
            required_fields = [
                'onboarding_cv_attachment_ids',
                'onboarding_medical_attachment_ids',
                'onboarding_police_report_attachment_ids',
                'onboarding_credentials_attachment_ids',
            ]
            missing = all(len(getattr(employee, f)) == 0 for f in required_fields)
            if missing:
                action = self.env.ref('your_module_name.action_onboarding_upload_wizard')
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Upload Required Onboarding Documents',
                    'res_model': 'onboarding.upload.wizard',
                    'view_mode': 'form',
                    'target': 'new',
                }

        return super()._login_successful(user, access_token)
