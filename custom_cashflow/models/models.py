# models/cash_flow_report.py
from odoo import models, fields, api, _

class CashFlowReportIFRSHandler(models.AbstractModel):
    _name = 'account.cash.flow.report.ifrs.handler'
    _inherit = 'account.cash.flow.report.handler'
    _description = 'IFRS Cash Flow Report Handler'

    def _get_layout_data(self):
        return {
            # Opening balance 
            'opening_balance': {'name': _('Cash and cash equivalents at the beginning of the year'), 'level': 0},

            # Operating activities
            'operating': {'name': _('Cash flow from operating activities'), 'level': 1, 'unfolded': True, 'class': 'fw-bold'},
                'operating_profit': {'name': _('Operating profit from continuing operations before exceptional items'), 'level': 2, 'parent_line_id': 'operating'},
                'exceptional_items': {'name': _('Exceptional Items'), 'level': 2, 'parent_line_id': 'operating'},
                'operating_after_exceptional': {'name': _('Operating profit after exceptional items from continuing operations'), 'level': 2, 'parent_line_id': 'operating'},
                'depreciation': {'name': _('Depreciation, amortisation and impairment'), 'level': 2, 'parent_line_id': 'operating'},
                'pension': {'name': _('Employer contributions to defined benefit pension schemes net of service cost'), 'level': 2, 'parent_line_id': 'operating'},
                'working_capital': {'name': _('Movement in working capital and other non-cash movements:'), 'level': 2, 'parent_line_id': 'operating'},
                    'receivables': {'name': _('Increase in trade and other receivables, prepayments, inventories and current assets'), 'level': 3, 'parent_line_id': 'working_capital'},
                    'payables': {'name': _('Increase in trade and other payables, deferred revenue on ticket sales and current liabilities'), 'level': 3, 'parent_line_id': 'working_capital'},
                'interest_paid': {'name': _('Interest paid'), 'level': 2, 'parent_line_id': 'operating'},
                'interest_received': {'name': _('Interest received'), 'level': 2, 'parent_line_id': 'operating'},
                'tax_paid': {'name': _('Tax paid'), 'level': 2, 'parent_line_id': 'operating'},
                'net_operating': {'name': _('Net cash generated from operating activities'), 'level': 1, 'parent_line_id': 'operating', 'class': 'fw-bold'},

            # Investing activities
            'investing': {'name': _('Cash flow from investing activities'), 'level': 1, 'unfolded': True, 'class': 'fw-bold'},
                'purchase_assets': {'name': _('Purchase of property, plant and equipment and intangible assets'), 'level': 2, 'parent_line_id': 'investing'},
                'sale_assets': {'name': _('Sales of property, plant and equipment and intangible assets'), 'level': 2, 'parent_line_id': 'investing'},
                'dividends_received': {'name': _('Dividends received'), 'level': 2, 'parent_line_id': 'investing'},
                'other_investing': {'name': _('Other investing movements'), 'level': 2, 'parent_line_id': 'investing'},
                'deposits': {'name': _('(Increase)/Decrease in other current interest-bearing deposits'), 'level': 2, 'parent_line_id': 'investing'},
                'net_investing': {'name': _('Net cash used in investing activities'), 'level': 1, 'parent_line_id': 'investing', 'class': 'fw-bold'},

            # Financing activities
            'financing': {'name': _('Cash flow from financing activities'), 'level': 1, 'unfolded': True, 'class': 'fw-bold'},
                'proceeds_loans': {'name': _('Proceeds from long-term borrowings'), 'level': 2, 'parent_line_id': 'financing'},
                'repay_loans': {'name': _('Repayments of borrowings'), 'level': 2, 'parent_line_id': 'financing'},
                'repay_assets': {'name': _('Repayment of asset financed liabilities'), 'level': 2, 'parent_line_id': 'financing'},
                'lease_liabilities': {'name': _('Repayment of lease liabilities'), 'level': 2, 'parent_line_id': 'financing'},
                'dividends_paid': {'name': _('Dividends paid'), 'level': 2, 'parent_line_id': 'financing'},
                'net_financing': {'name': _('Net cash flow used in financing activities'), 'level': 1, 'parent_line_id': 'financing', 'class': 'fw-bold'},

            # Net movement and closing balances
            'decrease_increase': {'name': _('(Decrease)/Increase in cash and cash equivalents'), 'level': 0},
            'fx_diff': {'name': _('Net foreign exchange differences'), 'level': 0},
            'closing_balance': {'name': _('Cash and cash equivalents at the end of the year'), 'level': 0},
            'interest_deposits': {'name': _('Interest-bearing deposits maturing after more than three months'), 'level': 0},
            'total_cash': {'name': _('Cash, cash equivalents and other interest-bearing deposits at the year end'), 'level': 0, 'class': 'fw-bold'},
        }


    # Computation for the report lines
    def _custom_engine_evaluate_formula(self, report, options, expression, date_scope):
        if expression == 'operating_profit':
            return self.env['account.move.line']._read_group(
                domain=[('account_id.account_type', '=', 'income')],
                fields=['balance:sum']
            )[0]['balance']
        return super()._custom_engine_evaluate_formula(report, options, expression, date_scope)


    @api.model
    def _get_lines(self, options, line_id=None):
        lines = []

        def compute_tag_sum(tag_xml_id):
            tag = self.env.ref(tag_xml_id)
            aml = self.env['account.move.line'].search([
                ('account_id.tag_ids', 'in', tag.ids),
                ('parent_state', '=', 'posted'),
                ('date', '>=', options['date'].get('date_from')),
                ('date', '<=', options['date'].get('date_to')),
            ])
            return sum(aml.mapped('balance'))

        tags = [
            ('tag_operating_profit_before_exceptional', "Operating profit before exceptional items"),
            ('tag_exceptional_items', "Exceptional Items"),
            ('tag_operating_profit_after_exceptional', "Operating profit after exceptional items"),
            ('tag_depreciation_amortisation', "Depreciation, amortisation and impairment"),
            ('tag_pension_contributions', "Employer pension contributions"),
            ('tag_movement_working_capital', "Movement in working capital"),
            ('tag_increase_receivables', "Increase in receivables"),
            ('tag_increase_payables', "Increase in payables"),
            ('tag_interest_paid', "Interest paid"),
            ('tag_interest_received', "Interest received"),
            ('tag_tax_paid', "Tax paid"),
            ('tag_net_operating_cash', "Net cash from operating activities"),
            ('tag_purchase_assets', "Purchase of assets"),
            ('tag_sale_assets', "Sale of assets"),
            ('tag_dividends_received', "Dividends received"),
            ('tag_other_investing', "Other investing movements"),
            ('tag_interest_bearing_deposits', "Interest-bearing deposits"),
            ('tag_net_investing_cash', "Net cash used in investing activities"),
            ('tag_proceeds_borrowings', "Proceeds from borrowings"),
            ('tag_repayment_borrowings', "Repayment of borrowings"),
            ('tag_repayment_asset_finance', "Repayment of asset finance"),
            ('tag_repayment_leases', "Repayment of leases"),
            ('tag_dividends_paid', "Dividends paid"),
            ('tag_net_financing_cash', "Net cash from financing activities"),
            ('tag_increase_cash_equivalents', "Increase/(Decrease) in cash equivalents"),
            ('tag_fx_difference', "FX differences"),
            ('tag_cash_beginning', "Cash at beginning"),
            ('tag_cash_end', "Cash at end"),
        ]

        for tag_xml_id, label in tags:
            amount = compute_tag_sum(f"una_cashflow.{tag_xml_id}")
            lines.append({
                'id': tag_xml_id,
                'name': label,
                'columns': [{'name': self.env.company.currency_id.symbol + " " + str(amount)}],
                'level': 2,
            })

        return lines
    





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


    # --- Public Methods Callable from Expression Wizard ---
    def _report_custom_engine_cash_opening_balance(self, options, measure='balance', mode='posted', domain=None):
        """
        Returns only the opening balance for cash/cash equivalents.
        Can be called from Python Function Engine in the expression wizard.
        """
        domain = domain or [('account_id.account_type', '=', 'asset_cash')]
        return self._get_opening_balance(options, domain=domain, measure=measure, mode=mode)

    def _report_custom_engine_cash_closing_balance(self, options, measure='balance', mode='posted', domain=None):
        """
        Returns only the closing balance for cash/cash equivalents.
        Can be called from Python Function Engine in the expression wizard.
        """
        domain = domain or [('account_id.account_type', '=', 'asset_cash')]
        return self._get_closing_balance(options, domain=domain, measure=measure, mode=mode)

    def _report_custom_engine_cash_movement(self, options, measure='balance', mode='posted', domain=None):
        """
        Returns movement: (closing - opening), i.e. net change in cash over the period.
        """
        domain = domain or [('account_id.account_type', '=', 'asset_cash')]
        opening = self._get_opening_balance(options, domain=domain, measure=measure, mode=mode)
        closing = self._get_closing_balance(options, domain=domain, measure=measure, mode=mode)
        return closing - opening