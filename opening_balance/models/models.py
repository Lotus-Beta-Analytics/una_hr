# -*- coding: utf-8 -*-
from odoo import models, api, _


class AccountReport(models.AbstractModel):
    _inherit = "account.report"

    def _compute_range_balance(self, options, measure, mode, domain_opening, domain_period):
        """
        Computes the opening and closing balance using Odoo's internal reporting engine.
        Returns a tuple: (opening_balance, closing_balance)
        """
        opening_vals = self._report_custom_engine_balance_move_line(
            options,
            measure,
            mode,
            domain=domain_opening,
        )

        period_vals = self._report_custom_engine_balance_move_line(
            options,
            measure,
            mode,
            domain=domain_period,
        )

        # Safely extract measure values
        def sum_measure(vals):
            if isinstance(vals, list):
                return sum(v.get(measure, 0.0) for v in vals)
            return float(vals or 0.0)

        opening_balance = sum_measure(opening_vals)
        period_balance = sum_measure(period_vals)
        closing_balance = opening_balance + period_balance

        return opening_balance, closing_balance

    # === Public methods for use in UI (Python Function Engine) ===

    def _report_custom_engine_opening_balance(self, options, measure='balance', mode='posted', domain=None):
        """
        Returns only the opening balance (before date_from).
        """
        domain = list(domain or [])
        date_from = options['date']['date_from']

        domain_opening = domain + [('date', '<', date_from)]
        domain_period = []  # Not needed for opening-only, but passed to helper

        if mode == 'posted':
            domain_opening += [('move_id.state', '=', 'posted')]

        opening_balance, _ = self._compute_range_balance(
            options, measure, mode, domain_opening, domain_period
        )
        return float(opening_balance)

    def _report_custom_engine_closing_balance(self, options, measure='balance', mode='posted', domain=None):
        """
        Returns closing balance at the end of the selected period.
        (i.e., opening balance + net movement within period)
        """
        domain = list(domain or [])
        date_from = options['date']['date_from']
        date_to = options['date']['date_to']

        domain_opening = domain + [('date', '<', date_from)]
        domain_period = domain + [('date', '>=', date_from), ('date', '<=', date_to)]

        if mode == 'posted':
            domain_opening += [('move_id.state', '=', 'posted')]
            domain_period += [('move_id.state', '=', 'posted')]

        _, closing_balance = self._compute_range_balance(
            options, measure, mode, domain_opening, domain_period
        )
        return float(closing_balance)

    def _report_custom_engine_opening_closing_difference(self, options, measure='balance', mode='posted', domain=None):
        """
        Returns (closing - opening), i.e., net movement in period.
        """
        domain = list(domain or [])
        date_from = options['date']['date_from']
        date_to = options['date']['date_to']

        domain_opening = domain + [('date', '<', date_from)]
        domain_period = domain + [('date', '>=', date_from), ('date', '<=', date_to)]

        if mode == 'posted':
            domain_opening += [('move_id.state', '=', 'posted')]
            domain_period += [('move_id.state', '=', 'posted')]

        opening_balance, closing_balance = self._compute_range_balance(
            options, measure, mode, domain_opening, domain_period
        )
        return float(closing_balance - opening_balance)
