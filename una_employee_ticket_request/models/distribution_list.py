# models/distribution_list.py
from odoo import models, fields, api, _

class TicketDistributionList(models.Model):
    _name = 'ticket.distribution.list'
    _description = 'Ticket Issuance Distribution List'
    user_ids = fields.Many2many('res.users', string="Select Employee to Notify")
