# -*- coding: utf-8 -*-
import requests
from datetime import datetime

from odoo import models, fields
from odoo.exceptions import UserError


class BankApiConfig(models.Model):
    _inherit = 'bank.api.config'

    # ==========================
    # PUBLIC METHODS
    # ==========================

    def action_sync_now(self):
        for rec in self:
            rec._run_sync()

    def run_scheduled_sync(self):
        configs = self.search([('active', '=', True)])
        for config in configs:
            config._run_sync()

    # ==========================
    # MAIN ENGINE
    # ==========================

    def _run_sync(self):

        data = self._fetch_api_data()

        if not data:
            return

        statement = self._create_statement()

        self._create_statement_lines(statement, data)

        self.last_sync = fields.Datetime.now()

    # ==========================
    # API FETCH
    # ==========================

    def _fetch_api_data(self):

        headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }

        try:
            response = requests.get(
                self.api_url,
                headers=headers,
                timeout=30
            )
        except Exception as e:
            raise UserError(f'Connection Error: {e}')

        if response.status_code != 200:
            raise UserError(
                f'API Error {response.status_code}'
            )

        return response.json()

    # ==========================
    # STATEMENT CREATION
    # ==========================

    def _create_statement(self):

        return self.env['account.bank.statement'].create({
            'name': f'{self.journal_id.name} Sync {fields.Date.today()}',
            'journal_id': self.journal_id.id,
            'date': fields.Date.today(),
        })

    # ==========================
    # LINES CREATION
    # ==========================

    def _create_statement_lines(self, statement, data):

        for rec in data:

            if self._is_duplicate(rec):
                continue

            amount = self._get_amount(rec)

            self.env['account.bank.statement.line'].create({
                'statement_id': statement.id,
                'date': self._format_date(rec.get('ValueDate')),
                'payment_ref': rec.get('ReferenceNo'),
                'name': rec.get('Description'),
                'amount': amount,
                'unique_import_id': rec.get('ptid'),
            })

    # ==========================
    # HELPERS
    # ==========================

    def _is_duplicate(self, rec):

        return bool(self.env['account.bank.statement.line'].search([
            ('unique_import_id', '=', rec.get('ptid'))
        ], limit=1))

    def _get_amount(self, rec):

        if rec.get('DebitCredit') == 'C':
            return float(rec.get('CreditAmt') or 0)

        return -float(rec.get('DebitAmt') or 0)

    def _format_date(self, date_str):

        if not date_str:
            return fields.Date.today()

        return datetime.strptime(
            date_str, '%d%m%Y'
        ).date()
