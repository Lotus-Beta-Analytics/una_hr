from odoo import models, fields, api, _
from urllib.parse import urlparse
import re
from odoo.exceptions import UserError, ValidationError
from urllib.parse import quote
import logging

_logger = logging.getLogger(__name__)



class HrAppraisalTrainingRecommendation(models.Model):
    _name = 'hr.appraisal.training.recommendation'
    _description = 'Training Recommendation'
    _order = 'id desc'

    appraisal_id = fields.Many2one('hr.appraisal', string='Appraisal', ondelete='cascade')
    training_topic = fields.Char(string='Training Topic')
    reason = fields.Text(string='Reason for Recommendation')
    date_recommended = fields.Date(string='Date Recommended', default=fields.Date.today)
    date_due = fields.Date(string="Expected Completion Date")
    department_id = fields.Many2one('hr.department', string='Department', related='employee_id.department_id', store=True)
    manager_id = fields.Many2one('hr.employee', string='Manager', default=lambda self: self.env.user.employee_id, readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Recommended For:')
    # course_url = fields.Char(string="Course URL", compute="action_open_course", store=True)

    course_id = fields.Many2one('slide.channel', string='Recommended Elearning Course')  # Dropdown of courses
      
    def action_open_course(self):
        self.ensure_one()

        if not self.course_id:
            raise UserError(_("No course selected."))

        website_url = self.course_id.website_url
        if not website_url:
            raise UserError(_("The selected course has no website URL. Make sure it's published."))

        # Check if the URL already contains http/https (fully qualified)
        if website_url.startswith("http://") or website_url.startswith("https://"):
            full_url = website_url
        else:
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            full_url = f"{base_url}{website_url}"

        return {
            'type': 'ir.actions.act_url',
            'url': full_url,
            'target': 'new',
        }
    
    def get_course_url(self):
        self.ensure_one()
        if not self.course_id:
            return ''
        
        website_url = self.course_id.website_url
        if website_url.startswith("http://") or website_url.startswith("https://"):
            return website_url
        else:
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            return f"{base_url}{website_url}"



    @api.onchange('manager_id')
    def _onchange_manager_id(self):
        if self.manager_id and self.manager_id.department_id:
            return {
                'domain': {
                    'employee_id': [('department_id', '=', self.manager_id.department_id.id)]
                }
            }
        
    @api.onchange('appraisal_id')
    def _onchange_appraisal_id(self):
        if self.appraisal_id:
            self.employee_id = self.appraisal_id.employee_id


    @api.model
    def create(self, vals):
        if not vals.get('manager_id'):
            current_employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
            if not current_employee or current_employee != self.env['hr.appraisal'].browse(vals.get('appraisal_id')).manager_id:
                raise ValidationError(_('Only line managers can recommend training.'))
            vals['manager_id'] = current_employee.id

        if vals.get('appraisal_id') and not vals.get('employee_id'):
            appraisal = self.env['hr.appraisal'].browse(vals['appraisal_id'])
            if appraisal.employee_id:
                vals['employee_id'] = appraisal.employee_id.id

        recommendation = super().create(vals)

        # Send email to employee
        template = self.env.ref('una_hr_appraisal_advanced.mail_template_training_recommendation_assigned', raise_if_not_found=False)
        if template and recommendation.employee_id.work_email:
            try:
                template.send_mail(recommendation.id, force_send=True)
            except Exception as e:
                _logger.warning("Failed to send training recommendation email to employee %s: %s", recommendation.employee_id.name, e)

        return recommendation
            

    # @api.model
    # def create(self, vals):
    #     if not vals.get('manager_id'):
    #         current_employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
    #         if not current_employee or current_employee != self.env['hr.appraisal'].browse(vals.get('appraisal_id')).manager_id:
    #             raise ValidationError(_('Only line managers can recommend training.'))
    #         vals['manager_id'] = current_employee.id

    #     if vals.get('appraisal_id') and not vals.get('employee_id'):
    #         appraisal = self.env['hr.appraisal'].browse(vals['appraisal_id'])
    #         if appraisal.employee_id:
    #             vals['employee_id'] = appraisal.employee_id.id
    #     return super().create(vals)
    
    
