from odoo import models, fields


class BankApiConfig(models.Model):
    _name = 'bank.api.config'
    _description = 'Bank API Configuration'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True)

    api_url = fields.Char(
        string='API URL',
        required=True
    )

    api_token = fields.Char(
        string='API Token',
        required=True
    )

    account_no = fields.Char(
        string='Account Number',
        required=True
    )

    journal_id = fields.Many2one(
        'account.journal',
        string='Bank Journal',
        domain=[('type', '=', 'bank')],
        required=True
    )

    last_sync = fields.Datetime(
        string='Last Sync'
    )

    active = fields.Boolean(default=True)
