from odoo import models, fields, api
from datetime import datetime, date


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    join_date = fields.Date(string="Join Date")  # Already exists


class HrEmployeeAnniversaryLog(models.Model):
    _name = 'hr.employee.anniversary.log'
    _description = 'Log of Anniversary Emails Sent'

    employee_id = fields.Many2one('hr.employee', required=True)
    sent_time = fields.Datetime(string='Sent At', default=fields.Datetime.now)
    anniversary_date = fields.Date(string='Anniversary Date', required=True)


class HrEmployeeAnniversary(models.Model):
    _name = 'hr.employee.anniversary'
    _description = 'Employee Anniversary Cron Handler'

    @api.model
    def send_anniversary_emails(self):
        today = date.today()
        employees = self.env['hr.employee'].search([])

        for employee in employees:
            if not employee.join_date:
                continue

            if employee.join_date.month == today.month and employee.join_date.day == today.day:
                # Check how many anniversary emails were sent today
                email_logs_today = self.env['hr.employee.anniversary.log'].search_count([
                    ('employee_id', '=', employee.id),
                    ('anniversary_date', '=', today),
                ])

                if email_logs_today < 2:
                    # Send the email
                    template = self.env.ref('una_staff_anniversary.template_anniversary_celebrant')
                    if template:
                        template.send_mail(employee.id, force_send=True)

                        # Log the email sending
                        self.env['hr.employee.anniversary.log'].create({
                            'employee_id': employee.id,
                            'anniversary_date': today,
                        })


