from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.model
    def _cron_send_birthday_notifications(self):
        """Send birthday greetings to employees and notify others."""

        today = fields.Date.today()
        celebrants = self.search([('birthday', '!=', False)]).filtered(
            lambda emp: emp.birthday and emp.birthday.strftime('%m-%d') == today.strftime('%m-%d')
        )

        _logger.info("Found %d celebrants on %s", len(celebrants), today)

        template_celebrant = self.env.ref(
            'employee_birthday_notifier.template_birthday_celebrant', raise_if_not_found=False)
        template_broadcast = self.env.ref(
            'employee_birthday_notifier.template_birthday_announcement', raise_if_not_found=False)

        if not template_celebrant or not template_broadcast:
            _logger.warning("Missing email templates. Cannot proceed.")
            return

        all_emails = self.search([('work_email', '!=', False)]).mapped('work_email')

        for emp in celebrants:
            _logger.info("Sending celebrant email to %s (%s)", emp.name, emp.work_email)
            if emp.work_email:
                template_celebrant.send_mail(emp.id, force_send=True)
            if all_emails:
                template_broadcast.with_context(celebrant_name=emp.name).send_mail(
                    emp.id,
                    email_values={'email_to': ','.join(all_emails)},
                    force_send=True
                )