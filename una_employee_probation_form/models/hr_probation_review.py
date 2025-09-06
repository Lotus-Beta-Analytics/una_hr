# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
import logging
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)
from dateutil.relativedelta import relativedelta

class HrProbationReview(models.Model):
    _name = 'hr.probation.review'
    _description = 'Probation Review'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Link to employee; most header info derives from here
    def _get_default_employee(self):
        employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        if not employee:
            raise UserError(_("No employee linked to your user account. Please contact HR."))
        return employee.id

    employee_id = fields.Many2one(
        'hr.employee', 
        string="Employee", 
        required=True, 
        tracking=True,
        default=_get_default_employee
    )

    line_manager_id = fields.Many2one(
    'hr.employee',
    string="Line Manager",
    compute="_compute_line_manager",
    store=True
)

    @api.depends('employee_id')
    def _compute_line_manager(self):
        for rec in self:
            rec.line_manager_id = rec.employee_id.parent_id

    name = fields.Char(string="Review Name", compute="_compute_name", store=True)

    @api.depends('employee_id')
    def _compute_name(self):
        for rec in self:
            emp_name = rec.employee_id.name or 'Unknown'
            date_str = rec.probation_end_date.strftime('%Y-%m-%d') if rec.probation_end_date else 'No Date'
            rec.name = f"{emp_name} - Probation Review ({date_str})"


    # Employee snapshot fields shown on the PDF
    employee_name = fields.Char(string="Name", related='employee_id.name', store=True)
    job_id = fields.Many2one(related='employee_id.job_id', comodel_name='hr.job', string="Position", store=True)
    department_id = fields.Many2one(related='employee_id.department_id', comodel_name='hr.department', string="Department", store=True)
    entry_date = fields.Date(string="Entry date", related='employee_id.join_date', store=True)
    probation_end_date = fields.Date(string="Probation end date", compute="_compute_probation_end_date", store=True)

    # Company employee number / code on your form (free text to match "UNAC/Number")
    unac_number = fields.Char(string="UNAC/Number", store=True)

    # Line items (a–f) for 3 sections; stored in one table with type to keep UI clean
    line_ids = fields.One2many('hr.probation.review.line', 'review_id', string="Details", store=True)

    # Convenience smart-one2many domains
    responsibility_line_ids = fields.One2many('hr.probation.review.line', 'review_id',
                                              domain=[('line_type', '=', 'responsibility')],
                                              string="Summary of Key Responsibilities", store=True)
    achievement_line_ids = fields.One2many('hr.probation.review.line', 'review_id',
                                           domain=[('line_type', '=', 'achievement')],
                                           string="Summary of Key Achievements", store=True)
    plan_line_ids = fields.One2many('hr.probation.review.line', 'review_id',
                                    domain=[('line_type', '=', 'plan')],
                                    string="Planned Activities / Targets (Next 3 Months)", store=True)

    # Staff sign-off
    staff_name = fields.Char(string="Staff Name", default=lambda self: self._get_default_staff_name(), readonly=True, store=True)
    def _get_default_staff_name(self):
        employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        return employee.name if employee else ''


    staff_date = fields.Date(string="Staff Date", store=True)

    # Supervisor review
    supervisor_comments = fields.Text(string="Supervisor Comments", store=True)
    supervisor_decision = fields.Selection([
        ('acceptable', 'Acceptable Performance – recommended for confirmation of employment'),
        ('fair', 'Fair Performance – recommended for a fixed period of three months'),
        ('poor', 'Poor/Unsatisfactory performance – recommended for termination of employment'),
        ('other', 'Other'),
    ], string="Supervisor Decision", store=True)

    

    supervisor_other = fields.Char(string="Other (specify)", store=True)

    # HR comments / consequences
    hr_comments = fields.Text(string="HR Comments / Consequences of the review", store=True)
    hr_signature = fields.Char(string="HR Signature", store=True)
    hr_date = fields.Date(string="HR Date", store=True)

    # Flow control (optional but useful)
    state = fields.Selection([
        ('draft', 'To Submit'),
        ('staff_submitted', 'Submitted by Staff'),
        ('supervisor_review', 'Supervisor Review'),
        ('hr_review', 'HR Review'),
        ('done', 'Completed'),
    ], string="Status", default='draft', tracking=True, store=True)

    state_color = fields.Char(compute='_compute_state_color')

    @api.depends('state')
    def _compute_state_color(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state_color = 'gray'
            elif rec.state == 'staff_submitted':
                rec.state_color = 'blue'
            elif rec.state == 'supervisor_review':
                rec.state_color = 'yellow'    
            elif rec.state == 'hr_review':
                rec.state_color = 'purple'
            elif rec.state == 'done':
                rec.state_color = 'green'    
        

    @api.depends('entry_date')
    def _compute_probation_end_date(self):
        for rec in self:
            rec.probation_end_date = rec.entry_date + relativedelta(months=3) if rec.entry_date else False

             

    # Simple actions to move through stages
    def action_submit_staff(self):
        for rec in self:
            rec.state = 'supervisor_review'
            template = self.env.ref('una_employee_probation_form.mail_template_notify_line_manager_probation_submitted', raise_if_not_found=False)
            if template and rec.employee_id.parent_id.work_email:
                _logger.info(
                    "Sending probation submission email to Line Manager (%s) for employee %s",
                    rec.employee_id.parent_id.work_email,
                    rec.employee_id.name
                )
                template.send_mail(rec.id, force_send=True)
            else:
                _logger.warning(
                    "Could not send submission email: Missing template or manager email for employee %s",
                    rec.employee_id.name
                )
                # template.send_mail(rec.id, force_send=True)

    def action_submit_supervisor(self):
        for rec in self:
            current_employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
            if not current_employee:
                raise UserError(_("You are not linked to an employee record. Please contact HR."))

            if rec.line_manager_id != current_employee:
                raise UserError(_("Only the direct Line Manager of %s can perform the supervisor review.") % rec.employee_id.name)
            rec.state = 'hr_review'
            template = self.env.ref(
                'una_employee_probation_form.mail_template_notify_hr_probation_submitted',
                raise_if_not_found=False
            )
            if template:
                _logger.info(
                    "Sending probation review submitted notification to HR for employee %s",
                    rec.employee_id.name
                )
                template.send_mail(rec.id, force_send=True)
            else:
                _logger.warning(
                    "Could not send HR notification: Missing template for employee %s",
                    rec.employee_id.name
                )
        

    def action_complete(self):
        for rec in self:
            rec.state = 'done'
            template = self.env.ref(
                'una_employee_probation_form.mail_template_notify_employee_review_completed',
                raise_if_not_found=False
            )
            if template and rec.employee_id.work_email:
                _logger.info(
                    "Sending probation review completed email to employee %s (%s)",
                    rec.employee_id.name,
                    rec.employee_id.work_email
                )
                template.send_mail(rec.id, force_send=True)
            else:
                _logger.warning(
                    "Could not send review completion email to employee %s: missing template or email",
                    rec.employee_id.name
                )
            


    def _send_probation_review_reminders(self):
        today = fields.Date.context_today(self)
        # Employees who joined exactly 3 months ago
        target_date = today - relativedelta(months=3)
        employees = self.env['hr.employee'].search([
            ('join_date', '=', target_date),
            ('work_email', '!=', False)
        ])
        template = self.env.ref(
            'una_employee_probation_form.mail_template_probation_review_reminder',
            raise_if_not_found=False
        )
        if not template:
            _logger.warning("Reminder email template not found.")
            return
        for employee in employees:
            # Check if there's already a draft review
            review = self.search([
                ('employee_id', '=', employee.id),
                ('state', '=', 'draft'),
            ], limit=1)
            if not review:
                review = self.create({
                    'employee_id': employee.id,
                    'state': 'draft',
                    # entry_date and probation_end_date are computed automatically
                })
                _logger.info(
                    "Created new probation review record for %s", employee.name
                )
            if template and employee.work_email:
                _logger.info(
                    "Sending probation reminder to %s (%s)", employee.name, employee.work_email
                )
                template.send_mail(review.id, force_send=True)
            else:
                _logger.warning(
                    "Could not send email: Missing email or template for employee %s", employee.name
                )
        

    # def _send_probation_review_reminders(self):
    #     today = fields.Date.context_today(self)

    #     reviews = self.search([
    #         ('probation_end_date', '=', today),
    #         ('state', '=', 'draft')
    #     ])

    #     template = self.env.ref('una_employee_probation_form.mail_template_probation_review_reminder', raise_if_not_found=False)

    #     for review in reviews:

    #         if review.employee_id.work_email and template:
    #             _logger.info(
    #                 "Sending probation reminder email to employee %s (%s)",
    #                 review.employee_id.name,
    #                 review.employee_id.work_email
    #             )
    #             template.send_mail(review.id, force_send=True)
    #         else:
    #             _logger.warning(
    #                 "Could not send reminder: Missing template or employee email for %s",
    #                 review.employee_id.name
    #             )
            # if review.employee_id.work_email and template:
            #     template.send_mail(review.id, force_send=True)
        
    def get_review_form_url(self):
        """Generate the URL to open the form jin the frontend"""
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        return f"{base_url}/web#id={self.id}&model=hr.probation.review&view_type=form"


class HrProbationReviewLine(models.Model):
    _name = 'hr.probation.review.line'
    _description = 'Probation Review Line'

    review_id = fields.Many2one('hr.probation.review', string="Review", ondelete='cascade', store=True)
    line_type = fields.Selection([
        ('responsibility', 'Responsibility'),
        ('achievement', 'Achievement'),
        ('plan', 'Plan'),
    ], string="Type", index=True, store=True)
    sequence = fields.Integer(default=10)
    name = fields.Char(string="Item", help="Enter item text (e.g., point a, b, c...)", store=True)

    display_name = fields.Char(string="Label", compute="_compute_display_name", store=False)

    def _compute_display_name(self):
        for rec in self:
            if not rec.review_id or not rec.line_type:
                # Just assign empty or something else if needed
                rec.display_name = ''
                continue

            sibling_lines = rec.review_id.line_ids.filtered(
                lambda l: l.line_type == rec.line_type
            ).sorted(key=lambda l: l.sequence)

            try:
                index = list(sibling_lines).index(rec)
            except ValueError:
                index = 0

            def alpha_index(n):
                result = ''
                while True:
                    n, r = divmod(n, 26)
                    result = chr(97 + r) + result
                    if n == 0:
                        break
                    n -= 1
                return result

            # Only alphabetical letter + dot, no name
            rec.display_name = f"{alpha_index(index)}."



class HrEmployee(models.Model):
    _inherit = "hr.employee"

    join_date = fields.Date(string="Join Date", help="Date employee joined (entry date used for probation).", store=True)
