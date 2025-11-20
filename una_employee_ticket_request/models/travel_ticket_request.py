from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError

class TravelTicketRequest(models.Model):
    _name = 'travel.ticket.request'
    _description = 'Employee Travel Ticket Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Request Reference", required=True, copy=False, readonly=True,
                       default=lambda self: self.env['ir.sequence'].next_by_code('travel.ticket.request'))
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, default=lambda self: self.env.user.employee_id)
    department_id = fields.Many2one(related='employee_id.department_id', string='Department', store=True)
    travel_purpose = fields.Text(string='Purpose of Travel', required=True)
    destination = fields.Char(string='Destination', required=True)
    travel_date = fields.Date(string='Travel Date', required=True)
    return_date = fields.Date(string='Return Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('manager_approval', 'Manager Approval'),
        ('cco_approval', 'CCO Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Status', default='draft', tracking=True)
    ticket_count = fields.Integer(string="Tickets Used", compute="_compute_ticket_count", store=True)
    ticket_limit = fields.Integer(string="Ticket Limit", default=4)
    is_over_limit = fields.Boolean(string="Over Limit", compute="_compute_ticket_count")

    @api.depends('employee_id')
    def _compute_ticket_count(self):
        for rec in self:
            count = self.env['travel.ticket.request'].search_count([
                ('employee_id', '=', rec.employee_id.id),
                ('state', '=', 'approved')
            ])
            rec.ticket_count = count
            rec.is_over_limit = count >= rec.ticket_limit

    def action_submit(self):
        for rec in self:
            if rec.is_over_limit:
                raise UserError(f"{rec.employee_id.name} has reached the ticket limit ({rec.ticket_limit}).")
            rec.state = 'manager_approval'

    def action_manager_approve(self):
        self.ensure_one()
        self.state = 'cco_approval'

    def action_cco_approve(self):
        self.ensure_one()
        self.state = 'approved'
        # Notify Head of Call Center
        group = self.env.ref('your_module_name.group_head_call_center')
        partners = group.users.mapped('partner_id')
        self.message_post(
            subject="Ticket Request Approved",
            body=f"Travel ticket for {self.employee_id.name} has been approved. Please proceed to issue the ticket.",
            partner_ids=partners.ids
        )

    def action_reject(self):
        self.ensure_one()
        self.state = 'rejected'
