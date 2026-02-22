
from odoo import fields, models

class IntercontraVariation(models.Model):
    _name = "intercontra.variation"
    _description = "Project Variation"

    site_id = fields.Many2one("intercontra.site.project", required=True, ondelete="cascade")
    name = fields.Char(required=True)
    amount = fields.Monetary(currency_field="currency_id")
    currency_id = fields.Many2one(related="site_id.currency_id", store=True, readonly=True)
    note = fields.Text()
