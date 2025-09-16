# models/cash_flow_report.py
# -*- coding: utf-8 -*-
from odoo import models, api, _
from odoo.tools.float_utils import float_round

class CashFlowReportIFRSHandler(models.AbstractModel):
    _name = 'account.cash.flow.report.ifrs.handler'
    _inherit = 'account.cash.flow.report.handler'
    _description = 'IFRS Cash Flow Report Handler (UNA - customised)'

    def _get_layout_data(self):
        """
        Build the layout tree matching the user's requested format.
        """
        return {
            # Operating activities
            'opening_balance': {'name': _('Cash and cash equivalents at beginning of period'), 'level': 0},
            'operating': {'name': _('Cash flows from operating activities'), 'level': 1, 'unfolded': True, 'class': 'fw-bold'},
                'profit_before_tax': {'name': _('Profit before tax'), 'level': 2, 'parent_line_id': 'operating'},
                'depreciation_amortisation_impairment': {'name': _('Depreciation, amortisation and impairment'), 'level': 2, 'parent_line_id': 'operating'},
                'gains_losses_disposals': {'name': _('Adjustments for gains/losses on disposal of assets'), 'level': 2, 'parent_line_id': 'operating'},
                'movement_working_capital': {'name': _('Movement in working capital and other non-cash movements:'), 'level': 2, 'parent_line_id': 'operating'},
                    'increase_receivables_prepayments_inventories': {'name': _('Increase/Decrease in trade and other receivables, prepayments, inventories and current assets'), 'level': 3, 'parent_line_id': 'movement_working_capital'},
                    'increase_payables_deferred_ticket_sales': {'name': _('Increase/Decrease in trade and other payables, deferred revenue on ticket sales and current liabilities'), 'level': 3, 'parent_line_id': 'movement_working_capital'},
                'interest_paid_operating': {'name': _('Interest paid'), 'level': 2, 'parent_line_id': 'operating'},
                'income_taxes_paid': {'name': _('Income taxes paid'), 'level': 2, 'parent_line_id': 'operating'},
                'net_cash_from_operating': {'name': _('Net cash from (used in) operating activities'), 'level': 1, 'parent_line_id': 'operating', 'class': 'fw-bold'},

            # Investing
            'investing': {'name': _('Cash flows from investing activities'), 'level': 1, 'unfolded': True, 'class': 'fw-bold'},
                'purchase_aircraft': {'name': _('Purchase of Aircrafts'), 'level': 2, 'parent_line_id': 'investing'},
                'purchase_ppe': {'name': _('Purchase of other Property, Plant and Equipment'), 'level': 2, 'parent_line_id': 'investing'},
                'purchase_intangibles': {'name': _('Purchase of Intangibles'), 'level': 2, 'parent_line_id': 'investing'},
                'proceeds_sale_aircraft': {'name': _('Proceeds from sale of Aircraft'), 'level': 2, 'parent_line_id': 'investing'},
                'proceeds_sale_ppe': {'name': _('Proceeds from sale of PPE'), 'level': 2, 'parent_line_id': 'investing'},
                'proceeds_sale_intangibles': {'name': _('Proceeds from sale of intangible Assets'), 'level': 2, 'parent_line_id': 'investing'},
                'interest_received_investing': {'name': _('Interest received'), 'level': 2, 'parent_line_id': 'investing'},
                'dividends_received_investing': {'name': _('Dividends received'), 'level': 2, 'parent_line_id': 'investing'},
                'net_cash_from_investing': {'name': _('Net cash from (used in) investing activities'), 'level': 1, 'parent_line_id': 'investing', 'class': 'fw-bold'},

            # Financing
            'financing': {'name': _('Cash flows from financing activities'), 'level': 1, 'unfolded': True, 'class': 'fw-bold'},
                'proceeds_issue_shares': {'name': _('Proceeds from issue of shares'), 'level': 2, 'parent_line_id': 'financing'},
                'proceeds_borrowings': {'name': _('Proceeds from borrowings'), 'level': 2, 'parent_line_id': 'financing'},
                'repayment_borrowings': {'name': _('Repayment of borrowings'), 'level': 2, 'parent_line_id': 'financing'},
                'dividends_paid_financing': {'name': _('Dividends paid'), 'level': 2, 'parent_line_id': 'financing'},
                'interest_paid_financing': {'name': _('Interest paid'), 'level': 2, 'parent_line_id': 'financing'},
                'repayments_lease_liabilities': {'name': _('Repayments of lease liabilities'), 'level': 2, 'parent_line_id': 'financing'},
                'net_cash_from_financing': {'name': _('Net cash from (used in) financing activities'), 'level': 1, 'parent_line_id': 'financing', 'class': 'fw-bold'},

            # Footer
            'net_forex': {'name': _('Net foreign exchange differences'), 'level': 0},
            'net_increase_decrease_cash': {'name': _('Net increase (decrease) in cash and cash equivalents'), 'level': 0},
            'cash_beginning': {'name': _('Cash and cash equivalents at beginning of period'), 'level': 0},
            'cash_end': {'name': _('Cash and cash equivalents at end of period'), 'level': 0, 'class': 'fw-bold'},
        }

    # Map of logical expression -> XML tag id (module.xml_id)
    # Edit these strings to reflect the actual xml ids in your module if they differ.
    TAGS_MAPPING = {
        # Operating
        'profit_before_tax': 'una_cashflow.tag_operating_profit_before_exceptional',
        'depreciation_amortisation_impairment': 'una_cashflow.tag_depreciation_amortisation',
        'gains_losses_disposals': 'una_cashflow.tag_sale_assets',  # reuse sale_assets tag if present
        'increase_receivables_prepayments_inventories': 'una_cashflow.tag_increase_receivables',
        'increase_payables_deferred_ticket_sales': 'una_cashflow.tag_increase_payables',
        'interest_paid_operating': 'una_cashflow.tag_interest_paid',
        'income_taxes_paid': 'una_cashflow.tag_tax_paid',
        'net_cash_from_operating': 'una_cashflow.tag_net_operating_cash',

        # Investing
        'purchase_aircraft': 'una_cashflow.tag_purchase_aircraft',
        'purchase_ppe': 'una_cashflow.tag_purchase_assets',
        'purchase_intangibles': 'una_cashflow.tag_purchase_intangibles',
        'proceeds_sale_aircraft': 'una_cashflow.tag_proceeds_sale_aircraft',
        'proceeds_sale_ppe': 'una_cashflow.tag_sale_assets',
        'proceeds_sale_intangibles': 'una_cashflow.tag_sale_intangibles',
        'interest_received_investing': 'una_cashflow.tag_interest_received',
        'dividends_received_investing': 'una_cashflow.tag_dividends_received',
        'net_cash_from_investing': 'una_cashflow.tag_net_investing_cash',

        # Financing
        'proceeds_issue_shares': 'una_cashflow.tag_proceeds_issue_shares',
        'proceeds_borrowings': 'una_cashflow.tag_proceeds_borrowings',
        'repayment_borrowings': 'una_cashflow.tag_repayment_borrowings',
        'dividends_paid_financing': 'una_cashflow.tag_dividends_paid',
        'interest_paid_financing': 'una_cashflow.tag_interest_paid_financing',
        'repayments_lease_liabilities': 'una_cashflow.tag_repayment_leases',
        'net_cash_from_financing': 'una_cashflow.tag_net_financing_cash',

        # Cash / FX
        'net_forex': 'una_cashflow.tag_fx_difference',
        'cash_beginning': 'una_cashflow.tag_cash_beginning',
        'cash_end': 'una_cashflow.tag_cash_end',
        'net_increase_decrease_cash': 'una_cashflow.tag_increase_cash_equivalents',
    }

    def _get_tag_amount(self, xmlid, options):
        """
        Return the sum of balances for an account.tag referenced by xmlid across the options date range.
        If tag is missing or cannot be resolved, return 0.0.
        """
        if not xmlid:
            return 0.0
        try:
            tag = self.env.ref(xmlid, raise_if_not_found=False)
            if not tag:
                return 0.0
            # search lines having this tag in the period
            date_from = options['date'].get('date_from')
            date_to = options['date'].get('date_to')
            domain = [
                ('account_id.tag_ids', 'in', tag.ids),
                ('parent_state', '=', 'posted'),
                ('date', '>=', date_from),
                ('date', '<=', date_to),
            ]
            aml = self.env['account.move.line'].search(domain)
            return float(sum(aml.mapped('balance')) or 0.0)
        except Exception:
            return 0.0

    def _format_amount(self, amount):
        """
        Format amount value as string with company currency symbol and two decimals.
        """
        currency = self.env.company.currency_id
        symbol = currency.symbol or ''
        rounded = float_round(amount or 0.0, precision_rounding=currency.rounding)
        return "%s %s" % (symbol, format(rounded, ',.2f'))

    # Custom expression engine (called from the report expression wizard or internal calls)
    def _custom_engine_evaluate_formula(self, report, options, expression, date_scope):
        """
        Evaluate named expressions. Uses TAGS_MAPPING when available, else fallbacks to computed methods.
        """
        # 1) If mapping exists, try to use it
        if expression in self.TAGS_MAPPING:
            amount = self._get_tag_amount(self.TAGS_MAPPING[expression], options)
            return amount

        # 2) Known special expressions that use opening/closing helper
        if expression == 'cash_beginning' or expression == 'opening_balance':
            # use account type filter for cash
            return self._report_custom_engine_cash_opening_balance(options)
        if expression == 'cash_end' or expression == 'closing_balance':
            return self._report_custom_engine_cash_closing_balance(options)
        if expression == 'net_increase_decrease_cash' or expression == 'cash_movement':
            return self._report_custom_engine_cash_movement(options)

        # 3) Fallbacks for a few core computations if tags aren't defined:
        if expression == 'profit_before_tax':
            # Fallback: sum of income accounts (negative if revenue) and expense accounts? We will use posted P&L lines
            domain = [
                ('move_id.state', '=', 'posted'),
                ('date', '>=', options['date'].get('date_from')),
                ('date', '<=', options['date'].get('date_to')),
                ('account_id.account_type', 'in', ['income', 'expense']),
            ]
            res = self.env['account.move.line']._read_group(domain=domain, fields=['balance:sum'])
            if res:
                return res[0].get('balance') or 0.0
            return 0.0

        if expression == 'depreciation_amortisation_impairment':
            # If no tag: try to sum lines whose account name contains 'Depreciation' (simple fallback)
            date_from = options['date'].get('date_from')
            date_to = options['date'].get('date_to')
            domain = [
                ('move_id.state', '=', 'posted'),
                ('date', '>=', date_from),
                ('date', '<=', date_to),
                ('account_id.name', 'ilike', 'depreciation'),
            ]
            res = self.env['account.move.line']._read_group(domain=domain, fields=['balance:sum'])
            return (res and res[0].get('balance')) or 0.0

        # default: call parent
        return super()._custom_engine_evaluate_formula(report, options, expression, date_scope)

    @api.model
    def _get_lines(self, options, line_id=None):
        """
        Build the lines in the same order as layout with computed amounts (columns structure expected by Odoo).
        """
        layout = self._get_layout_data()
        lines = []

        def add_line(key, amount, level=2):
            label = layout.get(key, {}).get('name', key)
            lines.append({
                'id': key,
                'name': label,
                'columns': [{'name': self._format_amount(amount)}],
                'level': level,
            })

        # Helper to fetch amount either via tag mapping or the custom engine:
        def amount_for(key):
            # If we have a mapping entry, prefer it
            xmlid = self.TAGS_MAPPING.get(key)
            if xmlid:
                v = self._get_tag_amount(xmlid, options)
                return v
            # try evaluate formula via custom engine
            try:
                v = self._custom_engine_evaluate_formula(None, options, key, None)
                return float(v or 0.0)
            except Exception:
                return 0.0

        # Build lines in requested visual order:

        # Opening balance (cash beginning)
        opening = amount_for('cash_beginning') or amount_for('opening_balance')
        add_line('opening_balance', opening, level=0)

        # Operating section
        # header (visual only)
        lines.append({'id': 'operating', 'name': layout['operating']['name'], 'level': 1, 'unfoldable': True, 'unfolded': True, 'class': 'fw-bold'})

        add_line('profit_before_tax', amount_for('profit_before_tax'), level=2)
        add_line('depreciation_amortisation_impairment', amount_for('depreciation_amortisation_impairment'), level=2)
        add_line('gains_losses_disposals', amount_for('gains_losses_disposals'), level=2)

        # Movement in working capital group header
        lines.append({'id': 'movement_working_capital', 'name': layout['movement_working_capital']['name'], 'level': 2, 'parent_line_id': 'operating'})
        add_line('increase_receivables_prepayments_inventories', amount_for('increase_receivables_prepayments_inventories'), level=3)
        add_line('increase_payables_deferred_ticket_sales', amount_for('increase_payables_deferred_ticket_sales'), level=3)

        add_line('interest_paid_operating', amount_for('interest_paid_operating'), level=2)
        add_line('income_taxes_paid', amount_for('income_taxes_paid'), level=2)

        # Net operating cash - prefer tag if exists else compute via: net_operating tag or compute as sum of above (simple)
        net_operating = amount_for('net_cash_from_operating') or (
            amount_for('profit_before_tax') +
            amount_for('depreciation_amortisation_impairment') +
            amount_for('gains_losses_disposals') -
            amount_for('increase_receivables_prepayments_inventories') +
            amount_for('increase_payables_deferred_ticket_sales') -
            amount_for('income_taxes_paid') -
            amount_for('interest_paid_operating')
        )
        add_line('net_cash_from_operating', net_operating, level=1)

        # Investing section
        lines.append({'id': 'investing', 'name': layout['investing']['name'], 'level': 1, 'unfoldable': True, 'unfolded': True, 'class': 'fw-bold'})

        add_line('purchase_aircraft', amount_for('purchase_aircraft'), level=2)
        add_line('purchase_ppe', amount_for('purchase_ppe'), level=2)
        add_line('purchase_intangibles', amount_for('purchase_intangibles'), level=2)
        add_line('proceeds_sale_aircraft', amount_for('proceeds_sale_aircraft'), level=2)
        add_line('proceeds_sale_ppe', amount_for('proceeds_sale_ppe'), level=2)
        add_line('proceeds_sale_intangibles', amount_for('proceeds_sale_intangibles'), level=2)
        add_line('interest_received_investing', amount_for('interest_received_investing'), level=2)
        add_line('dividends_received_investing', amount_for('dividends_received_investing'), level=2)

        # net investing - prefer tag, else simple sum of investing lines
        net_inv = amount_for('net_cash_from_investing') or (
            amount_for('proceeds_sale_aircraft') +
            amount_for('proceeds_sale_ppe') +
            amount_for('proceeds_sale_intangibles') +
            amount_for('interest_received_investing') +
            amount_for('dividends_received_investing') -
            amount_for('purchase_aircraft') -
            amount_for('purchase_ppe') -
            amount_for('purchase_intangibles')
        )
        add_line('net_cash_from_investing', net_inv, level=1)

        # Financing section
        lines.append({'id': 'financing', 'name': layout['financing']['name'], 'level': 1, 'unfoldable': True, 'unfolded': True, 'class': 'fw-bold'})

        add_line('proceeds_issue_shares', amount_for('proceeds_issue_shares'), level=2)
        add_line('proceeds_borrowings', amount_for('proceeds_borrowings'), level=2)
        add_line('repayment_borrowings', amount_for('repayment_borrowings'), level=2)
        add_line('dividends_paid_financing', amount_for('dividends_paid_financing'), level=2)
        add_line('interest_paid_financing', amount_for('interest_paid_financing'), level=2)
        add_line('repayments_lease_liabilities', amount_for('repayments_lease_liabilities'), level=2)

        net_fin = amount_for('net_cash_from_financing') or (
            amount_for('proceeds_issue_shares') +
            amount_for('proceeds_borrowings') -
            amount_for('repayment_borrowings') -
            amount_for('dividends_paid_financing') -
            amount_for('interest_paid_financing') -
            amount_for('repayments_lease_liabilities')
        )
        add_line('net_cash_from_financing', net_fin, level=1)

        # FX and net change
        fx = amount_for('net_forex')
        add_line('net_forex', fx, level=0)

        net_change = amount_for('net_increase_decrease_cash') or (net_operating + net_inv + net_fin + fx)
        add_line('net_increase_decrease_cash', net_change, level=0)

        # Cash at beginning (again) and end
        cash_begin = opening or amount_for('cash_beginning')
        add_line('cash_beginning', cash_begin, level=0)

        cash_end = amount_for('cash_end') or (cash_begin + net_change)
        add_line('cash_end', cash_end, level=0)

        return lines

    # --- Existing helpers retained from your original code --- #
    def _compute_range_balance(self, options, measure, mode, domain_opening, domain_period):
        """
        Computes the opening and closing balance using Odoo's internal reporting engine.
        Returns a tuple: (opening_balance, closing_balance)
        """
        opening_vals = self.env['account.report']._report_custom_engine_balance_move_line(
            options, measure, mode, domain=domain_opening,
        )

        period_vals = self.env['account.report']._report_custom_engine_balance_move_line(
            options, measure, mode, domain=domain_period,
        )

        def sum_measure(vals):
            if isinstance(vals, list):
                return sum(v.get(measure, 0.0) for v in vals)
            return float(vals or 0.0)

        opening_balance = sum_measure(opening_vals)
        period_balance = sum_measure(period_vals)
        closing_balance = opening_balance + period_balance

        return opening_balance, closing_balance

    def _get_opening_balance(self, options, domain=None, measure='balance', mode='posted'):
        domain = list(domain or [])
        date_from = options['date']['date_from']

        domain_opening = domain + [('date', '<', date_from)]
        domain_period = []  # Not needed here

        if mode == 'posted':
            domain_opening += [('move_id.state', '=', 'posted')]

        opening_balance, _ = self._compute_range_balance(options, measure, mode, domain_opening, domain_period)
        return float(opening_balance)

    def _get_closing_balance(self, options, domain=None, measure='balance', mode='posted'):
        domain = list(domain or [])
        date_from = options['date']['date_from']
        date_to = options['date']['date_to']

        domain_opening = domain + [('date', '<', date_from)]
        domain_period = domain + [('date', '>=', date_from), ('date', '<=', date_to)]

        if mode == 'posted':
            domain_opening += [('move_id.state', '=', 'posted')]
            domain_period += [('move_id.state', '=', 'posted')]

        _, closing_balance = self._compute_range_balance(options, measure, mode, domain_opening, domain_period)
        return float(closing_balance)

    def _report_custom_engine_cash_opening_balance(self, options, measure='balance', mode='posted', domain=None):
        domain = domain or [('account_id.account_type', '=', 'asset_cash')]
        return self._get_opening_balance(options, domain=domain, measure=measure, mode=mode)

    def _report_custom_engine_cash_closing_balance(self, options, measure='balance', mode='posted', domain=None):
        domain = domain or [('account_id.account_type', '=', 'asset_cash')]
        return self._get_closing_balance(options, domain=domain, measure=measure, mode=mode)

    def _report_custom_engine_cash_movement(self, options, measure='balance', mode='posted', domain=None):
        domain = domain or [('account_id.account_type', '=', 'asset_cash')]
        opening = self._get_opening_balance(options, domain=domain, measure=measure, mode=mode)
        closing = self._get_closing_balance(options, domain=domain, measure=measure, mode=mode)
        return closing - opening
