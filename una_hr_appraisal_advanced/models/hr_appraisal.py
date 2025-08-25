from odoo import fields, models, api,_
from odoo.exceptions import UserError
from datetime import datetime
from datetime import date
import logging
_logger = logging.getLogger(__name__)

class HrAppraisal(models.Model):
    _inherit = 'hr.appraisal'

    course_id = fields.Many2one('slide.channel', string='Recommended Course')  # Dropdown of courses
    course_preview_url = fields.Char(string="Course Link", compute="_compute_course_preview_url")

    employee_signed = fields.Boolean(string="Signed by Employee")
    employee_comment = fields.Text(string="Employee Comments: ")
    employee_sign_date = fields.Datetime(string="Employee Sign Date")

    manager_signed = fields.Boolean(string="Signed by Manager")
    manager_comment = fields.Text(string="Manager Comments: ")
    manager_sign_date = fields.Datetime(string="Manager Sign Date")
    training_recommendation_ids = fields.One2many(
        'hr.appraisal.training.recommendation', 'appraisal_id',
        string='Training Recommendations')
    date_from = fields.Date(string="Start Date")
    emp_id = fields.Char(
        string="Employee ID Number",
        related="employee_id.emp_id",
        store=True,
        readonly=True
    )

    def action_employee_sign(self):
        for rec in self:
            current_employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
            if rec.employee_id != current_employee:
                raise UserError("Only the appraisee can sign this section.")
            rec.employee_signed = True
            rec.employee_sign_date = fields.Datetime.now()

    def action_manager_sign(self):
        for rec in self:
            current_employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
            if current_employee.id not in rec.manager_ids.ids:
                raise UserError("Only the assigned manager(s) can sign this section.")
            rec.manager_signed = True
            rec.manager_sign_date = fields.Datetime.now()

    @api.model
    def create(self, vals):
        record = super().create(vals)

        # Send email to employee when goal is assigned
        template = self.env.ref(
            'una_hr_appraisal_advanced.mail_template_goal_assigned_to_employee',
            raise_if_not_found=False
        )
        if template and record.employee_id and record.employee_id.work_email:
            try:
                template.send_mail(record.id, force_send=True)
                record.message_post(
                    body=f"Goal '{record.name}' assigned. Email sent to employee: {record.employee_id.name} ({record.employee_id.work_email}).",
                    subtype_id=self.env.ref('mail.mt_note').id
                )
            except Exception as e:
                _logger.warning("Failed to send goal assignment email to employee %s: %s", record.employee_id.name, e)
        return record
        

