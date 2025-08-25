from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
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

    course_id = fields.Many2one('slide.channel', string='Recommended Course')  # Dropdown of courses
    course_preview_url = fields.Char(string="Course Link", compute="_compute_course_preview_url")

    @api.depends('course_id')
    def _compute_course_preview_url(self):
        for rec in self:
            if rec.course_id and rec.course_id.website_id:
                base_url = rec.course_id.website_id.domain or self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                rec.course_preview_url = f"{base_url}/slides/channel/{rec.course_id.id}/preview"
            else:
                rec.course_preview_url = False

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
        return super().create(vals)
