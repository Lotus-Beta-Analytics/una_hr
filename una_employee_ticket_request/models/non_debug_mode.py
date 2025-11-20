from odoo import models, fields, api
from odoo.exceptions import UserError


class ResUsers(models.Model):
    _inherit = 'res.users'

    ticket_category_id = fields.Many2one(
        'ir.module.category',
        compute='_compute_ticket_category_id',
        store=False
    )

    ticket_groups_ids = fields.Many2many(
        'res.groups',
        compute='_compute_ticket_groups',
        inverse='_inverse_ticket_groups',
        string="Ticket Request Access",
        store=False,
    )

    def _compute_ticket_category_id(self):
        category = self.env.ref(
            'una_employee_ticket_request.module_category_Employee_Ticket_Request'
        )
        for rec in self:
            rec.ticket_category_id = category.id

    @api.depends('groups_id')
    def _compute_ticket_groups(self):
        category = self.env.ref(
            'una_employee_ticket_request.module_category_Employee_Ticket_Request'
        )
        for rec in self:
            rec.ticket_groups_ids = rec.groups_id.filtered(
                lambda g: g.category_id == category
            )

    def _inverse_ticket_groups(self):
        category = self.env.ref(
            'una_employee_ticket_request.module_category_Employee_Ticket_Request'
        )
        for rec in self:
            # Remove all groups in this category, keep others
            other_groups = rec.groups_id.filtered(
                lambda g: g.category_id != category
            )
            rec.groups_id = other_groups | rec.ticket_groups_ids
