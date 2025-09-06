from odoo import models, fields, api, _

class RejectTicketWizard(models.TransientModel):
    _name = 'reject.ticket.wizard'
    _description = 'Reason for Ticket Rejection'

    ticket_id = fields.Many2one('employee.ticket.request', string='Ticket Request', required=True)
    reason = fields.Text(string='Reason for Rejection', required=True)

    def confirm_rejection(self):
        self.ensure_one()
        ticket = self.ticket_id
        ticket.state = 'rejected'
        rejecting_user = self.env.user

        ticket.message_post(
            body=f"Ticket was rejected with the following reason:<br/><b>{self.reason}</b>",
            subtype_id=self.env.ref('mail.mt_comment').id
        )
        template = self.env.ref('una_employee_ticket_request.mail_template_ticket_request_rejected')
        if template:
            template.with_context(
                reason=self.reason,
                rejected_by=rejecting_user.name
            ).send_mail(ticket.id, force_send=True)


        ticket.message_post(
            body=f"Ticket was rejected with the following reason:<br/><b>{self.reason}</b>",
            subtype_id=self.env.ref('mail.mt_comment').id
        )
