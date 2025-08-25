from odoo import models, fields, api
from datetime import date


class AppraisalReminder(models.Model):
    _inherit = 'hr.appraisal'

    @api.model
    def _send_appraisal_cycle_reminders(self):
        """Send appraisal reminders based on fixed cycles."""

        today = date.today()
        reminders = [
            {
                'name': 'First Quarterly Review',
                'start': date(today.year, 4, 1),
                'end': date(today.year, 4, 20),
            },
            {
                'name': 'Mid-Year Review',
                'start': date(today.year, 7, 1),
                'end': date(today.year, 7, 15),
            },
            {
                'name': 'End-of-Year Review',
                'start': date(today.year, 12, 15),
                'end': date(today.year + 1, 1, 15),
            },
        ]

        for cycle in reminders:
            if cycle['start'] <= today <= cycle['end']:
                self.env['hr.employee'].search([])._notify_appraisal_cycle(cycle['name'])


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def _notify_appraisal_cycle(self, cycle_name):
        template = self.env.ref('una_hr_appraisal_advanced.mail_template_appraisal_cycle_reminder')
        for employee in self:
            if employee.work_email:
                template.sudo().send_mail(employee.id, email_values={
                    'email_to': employee.work_email,
                    'subject': f'{cycle_name} Reminder - Performance Appraisal',
                }, force_send=True)
