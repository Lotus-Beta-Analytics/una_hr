
from odoo import fields, models

class IntercontraMilestoneTemplate(models.Model):
    _name = "intercontra.milestone.template"
    _description = "Milestone Template"

    client = fields.Selection([("atc","ATC"), ("ihs","IHS")], required=True)
    role = fields.Selection([("client","Client (AR)"), ("contractor","Contractor (AP)")], required=True)
    code = fields.Char()
    name = fields.Char(required=True)
    percent = fields.Float(digits=(16,2), required=True)
    active = fields.Boolean(default=True)
