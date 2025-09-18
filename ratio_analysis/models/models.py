# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class RatioAnalysisReportHandler(models.AbstractModel):
    _name = "ratio.analysis.report.handler"
    _inherit = "account.report.custom.handler"
    _description = "Ratio Analysis Report Handler"

    filter_date = {'mode': 'range', 'filter': 'this_year'}

    ####################################################    
    # Report Definition
    ####################################################
    def _get_report_name(self):
        return _("Ratio Analysis Report")

    def _get_columns_name(self, options):
        return [
            {'name': _('Ratio')},
            {'name': _('Value')},
        ]

    def _get_lines(self, options, line_id=None):
        lines = []

        # Ratios list
        ratios = [
            ('Current Ratio', self._compute_current_ratio(options)),
            ('Return on Equity', self._compute_return_on_equity(options)),
            ('Return on Assets', self._compute_return_on_assets(options)),
            ('EBIT', self._compute_ebit(options)),
            ('EBITDAR', self._compute_ebitdar(options)),
            ('Gross Profit Margin', self._compute_gross_profit_margin(options)),
            ('Net Profit Margin', self._compute_net_profit_margin(options)),
            ('Direct Cost Margin', self._compute_direct_cost_margin(options)),
            ('Other Operating Cost Margin', self._compute_other_operating_margin(options)),
            ('Interest Coverage Ratio', self._compute_interest_coverage(options)),
            ('Assets Turnover', self._compute_assets_turnover(options)),
            ('Debt Ratio', self._compute_debt_ratio(options)),
        ]

        for name, value in ratios:
            lines.append({
                'id': name,
                'name': name,
                'columns': [{'name': value}],
                'level': 2,
            })

        return lines

    ####################################################
    # Computation Functions (simplified placeholders)
    ####################################################
    def _compute_current_ratio(self, options):
        current_assets = self._get_account_balance(options, ['current_assets'])
        current_liab = self._get_account_balance(options, ['current_liabilities'])
        return round(current_assets / current_liab, 2) if current_liab else 0.0

    def _compute_return_on_equity(self, options):
        npat = self._get_account_balance(options, ['net_profit'])
        equity = self._get_equity(options)
        return round((npat / equity) * 100, 2) if equity else 0.0

    def _compute_return_on_assets(self, options):
        npat = self._get_account_balance(options, ['net_profit'])
        total_assets = self._get_account_balance(options, ['total_assets'])
        return round((npat / total_assets) * 100, 2) if total_assets else 0.0

    def _compute_ebit(self, options):
        np = self._get_account_balance(options, ['net_profit'])
        interest = self._get_account_balance(options, ['interest'])
        tax = self._get_account_balance(options, ['tax'])
        return np + interest + tax

    def _compute_ebitdar(self, options):
        ebit = self._compute_ebit(options)
        depreciation = self._get_account_balance(options, ['depreciation'])
        amortization = self._get_account_balance(options, ['amortization'])
        return ebit + depreciation + amortization

    def _compute_gross_profit_margin(self, options):
        gp = self._get_account_balance(options, ['gross_profit'])
        revenue = self._get_account_balance(options, ['revenue'])
        return round((gp / revenue) * 100, 2) if revenue else 0.0

    def _compute_net_profit_margin(self, options):
        np = self._get_account_balance(options, ['net_profit'])
        revenue = self._get_account_balance(options, ['revenue'])
        return round((np / revenue) * 100, 2) if revenue else 0.0

    def _compute_direct_cost_margin(self, options):
        cost = self._get_account_balance(options, ['direct_cost'])
        revenue = self._get_account_balance(options, ['revenue'])
        return round((cost / revenue) * 100, 2) if revenue else 0.0

    def _compute_other_operating_margin(self, options):
        cost = self._get_account_balance(options, ['other_operating_cost'])
        revenue = self._get_account_balance(options, ['revenue'])
        return round((cost / revenue) * 100, 2) if revenue else 0.0

    def _compute_interest_coverage(self, options):
        ebit = self._compute_ebit(options)
        interest = self._get_account_balance(options, ['interest'])
        return round((ebit / interest), 2) if interest else 0.0

    def _compute_assets_turnover(self, options):
        revenue = self._get_account_balance(options, ['revenue'])
        total_assets = self._get_account_balance(options, ['total_assets'])
        return round((revenue / total_assets), 2) if total_assets else 0.0

    def _compute_debt_ratio(self, options):
        total_debt = self._get_account_balance(options, ['total_debt'])
        total_assets = self._get_account_balance(options, ['total_assets'])
        return round((total_debt / total_assets) * 100, 2) if total_assets else 0.0

    ####################################################
    # Helper methods to fetch balances
    ####################################################
    def _get_account_balance(self, options, tags):
        """
        Dummy implementation. Replace `tags` mapping with account codes/domains.
        Example: map 'net_profit' to income statement bottom line account.
        """
        return 100000.0  # placeholder

    def _get_equity(self, options):
        # Example: sum share capital + retained earnings + reserves - accumulated losses
        return 500000.0  # placeholder