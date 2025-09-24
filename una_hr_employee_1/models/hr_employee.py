from odoo import models, fields, api, _
from odoo.exceptions import UserError

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    confirmation_status = fields.Selection([
        ('not_confirmed', 'Not Confirmed'),
        ('confirmed', 'Confirmed'),
    ], string='Confirmation Status', default='not_confirmed', required=True)
    badge_ids = fields.Many2many(
        'gamification.badge',
        'employee_badge_rel',
        'employee_id',
        'badge_id',
        string='Badges',
        readonly=True
    )

    confirmation_label_html = fields.Html(
        string="Confirmation Label HTML",
        compute='_compute_confirmation_label_html',
        sanitize=False,
    )
    confirmation_date = fields.Date(
        string='Confirmation Date',
        help='The date the employee was confirmed.',
        )
    leave_manager_id = fields.Many2one('res.users', string="Leave Manager")

    external_id = fields.Char(string="External ID")
    emp_id= fields.Char(string="Staff ID Number")
    join_date = fields.Date(string="Join Date")

    irs_state_id = fields.Many2one('res.country.state', string="IRS State")
  
    @api.depends('confirmation_status')
    def _compute_confirmation_label_html(self):
        for rec in self:
            if rec.confirmation_status == 'confirmed':
                rec.confirmation_label_html = """
                <div style="
                    position: absolute;
                    top: 25px;
                    left: 25px;
                    background-color: #28a745;
                    color: white;
                    font-weight: bold;
                    padding: 3px 15px;
                    border-radius: 3px;
                    text-align: center;
                    z-index: 50;
                    display: flex;
                    align-items: center;
                    gap: 3px;
                    font-size: 9px;
                    transform: rotate(-30deg);
                    transform-origin: top left;
                    box-shadow: 0 2px 3px rgba(0,0,0,0.2);
                    ">
                    <i class="fa fa-check" aria-hidden="true"></i>CONFIRMED
                </div>
                """
            else:
                rec.confirmation_label_html = """
                <div style="
                    position: absolute;
                    top: 25px;
                    left: 25px;
                    background-color: #dc3545;
                    color: white;
                    font-weight: bold;
                    padding: 3px 15px;
                    border-radius: 3px;
                    text-align: center;
                    z-index: 40;
                    display: flex;
                    align-items: center;
                    gap: 3px;
                    font-size: 7px;
                    transform: rotate(-30deg);
                    transform-origin: top left;
                    box-shadow: 0 2px 2px rgba(0,0,0,0.2);
                    ">
                    <i class="fa fa-times" aria-hidden="true"></i> NOT CONFIRM
                </div>
                """

    def action_confirm_employee(self):
        today = fields.Date.today()
        self.write({'confirmation_status': 'confirmed',
                    'confirmation_date': fields.Date.context_today(self),
                    })
        for employee in self:
            employee._send_confirmation_email()
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def action_unconfirm_employee(self):
        self.write({'confirmation_status': 'not_confirmed',
                    'confirmation_date': False,
                    })
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
    
    def _send_confirmation_email(self):
        for employee in self:
            if not employee.work_email:
                raise UserError(_("No work email address found for %s.") % employee.name)

            template = self.env.ref('una_hr_employee.mail_template_employee_confirmation', raise_if_not_found=False)
            if not template:
                raise UserError(_("Email template not found. Please ensure it is correctly defined and loaded."))

            try:
                # Let Odoo queue and send the email later to avoid SMTP errors
                template.send_mail(employee.id, force_send=False)
            except Exception as e:
                raise UserError(_("Failed to queue confirmation email: %s") % str(e))
    



class SurveySurvey(models.Model):
    _inherit = 'survey.survey'

    custom_radio_option = fields.Selection([
        ('option_1', 'Option 1'),
        ('option_2', 'Option 2'),
    ], string="Custom Radio Option")

    hr_usage_type = fields.Selection([
        ('appraisal', 'Appraisal'),
        ('recruitment', 'Recruitment'),
    ], string="HR Usage Type")
