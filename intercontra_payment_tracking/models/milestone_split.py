
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class IntercontraMilestoneSplit(models.Model):
    _name = "intercontra.milestone.split"
    _description = "Contractor split for milestone"

    milestone_id = fields.Many2one("intercontra.milestone", required=True, ondelete="cascade")
    contractor_id = fields.Many2one("res.partner", domain=[("supplier_rank", ">", 0)], required=True)
    percent = fields.Float(digits=(16,2), required=True)
    amount = fields.Monetary(compute="_compute_amount", store=True, currency_field="currency_id")
    currency_id = fields.Many2one(related="milestone_id.currency_id", store=True, readonly=True)

    @api.depends("percent", "milestone_id.amount")
    def _compute_amount(self):
        for rec in self:
            rec.amount = round((rec.milestone_id.amount or 0.0) * (rec.percent or 0.0) / 100.0, 2)

    @api.constrains("percent")
    def _check_percent_range(self):
        for rec in self:
            if rec.percent < 0 or rec.percent > 100:
                raise ValidationError(_("Split percent must be between 0 and 100."))
