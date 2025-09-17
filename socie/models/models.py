# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.osv.expression import AND
import io
import logging
from odoo.tools.misc import xlsxwriter

_logger = logging.getLogger(__name__)

# # class StatementChangeInEquityReport(models.Model):
# class SocieReportHandler(models.AbstractModel):
#     _name = "socie.report.handler"
#     _inherit = "account.report.custom.handler"
#     _description = "SOCIE Report Handler"

#     filter_date = {'mode': 'range', 'filter': 'this_year'}


#     ####################################################    
#     # Report Definition
#     ####################################################
#     def _get_report_name(self):
#         return _("Statement of Changes in Equity")

#     def _get_columns_name(self, options):
#         return [
#             {'name': _('Profit for year')},
#             {'name': _('New Capital issued during the year')},
#             {'name': _('Loss for year')},
#             {'name': _('Prior year adjustment to spare parts stock')},
#             {'name': _('Write back of ED Salary')},
#             {'name': _('COVID-19 Rebate from FGN')},
#             {'name': _('Prepaid Lease Rental now recognised')},
#             {'name': _('Stamp Duty paid on new Share Capital')},
#             {'name': _('Bonus Issue made')},
#             {'name': _('Revaluation of Aircraft')},
#             {'name': _('Term Loan Swapped for Equity')},
#             {'name': _('Additional shares Issued')},
#             {'name': _('Prior year expenses paid')},
#             {'name': _('Prior year Provision for ITF and NSITF')},
#             {'name': _('Tax Audit liability paid')},
#             {'name': _('Balance at end of the year')},
#     ]





#         #     {'name': _('Issued Share Capital')},
#         #     {'name': _('Deposit for Shares')},
#         #     {'name': _('Assets Revaluation')},
#         #     {'name': _('Retained Earnings')},
#         #     {'name': _('Total Equity')},
#         # ]

#     def _get_lines(self, options, line_id=None):
#         lines = []
#         # Example structure, formulas will come later
#         lines.append(self._build_line(_("Issued Share Capital")))
#         lines.append(self._build_line(_("Deposit for Shares")))
#         lines.append(self._build_line(_("Assets Revaluation")))
#         lines.append(self._build_line(_("Retained Earnings")))
#         lines.append(self._build_line(_("Total Equity")))
#         return lines

#     # def _build_line(self, name):
#     #     return {
#     #         'id': name,
#     #         'name': name,
#     #         'columns': [{'name': ''}] * 5,  # 5 columns
#     #         'level': 2,
#     #     }





# class SocieXlsxReport(models.AbstractModel):
#     _name = 'report.socie.socie_xlsx'
#     _inherit = 'report.report_xlsx.abstract'
#     _description = 'SOCIE Report (XLSX)'

#     def generate_xlsx_report(self, workbook, data, objects):
#         sheet = workbook.add_worksheet(_("SOCIE"))
#         bold = workbook.add_format({'bold': True, 'border': 1})
#         normal = workbook.add_format({'border': 1})
#         currency = workbook.add_format({'num_format': '#,##0.00', 'border': 1})

#         # === HEADERS (Rows as movements, Columns as Equity categories) ===
#         headers = [
#             _("Issued Share Capital"),
#             _("Deposit for Shares"),
#             _("Assets Revaluation"),
#             _("Retained Earnings"),
#             _("Total Equity"),
#         ]
#         sheet.write(0, 0, _("SOCIE Movements"), bold)
#         for col, header in enumerate(headers, start=1):
#             sheet.write(0, col, header, bold)

#         # === Movements (rows from your handler’s _get_columns_name) ===
#         movements = [
#             _("Profit for year"),
#             _("New Capital issued during the year"),
#             _("Loss for year"),
#             _("Prior year adjustment to spare parts stock"),
#             _("Write back of ED Salary"),
#             _("COVID-19 Rebate from FGN"),
#             _("Prepaid Lease Rental now recognised"),
#             _("Stamp Duty paid on new Share Capital"),
#             _("Bonus Issue made"),
#             _("Revaluation of Aircraft"),
#             _("Term Loan Swapped for Equity"),
#             _("Additional shares Issued"),
#             _("Prior year expenses paid"),
#             _("Prior year Provision for ITF and NSITF"),
#             _("Tax Audit liability paid"),
#             _("Balance at end of the year"),
#         ]

#         # Map each movement to the correct equity column(s)
#         mapping = {
#             "Profit for year": {"retained": 3},
#             "Loss for year": {"retained": 3},
#             "New Capital issued during the year": {"share_cap": 1},
#             "Bonus Issue made": {"share_cap": 1, "retained": 3},
#             "Revaluation of Aircraft": {"reval": 2},
#             "Additional shares Issued": {"share_cap": 1},
#             "Term Loan Swapped for Equity": {"share_cap": 1},
#             "Balance at end of the year": {"total": 4},
#             # others you can map as needed
#         }

#         # Write movements + dummy balances (replace with real values)
#         row = 1
#         for move in movements:
#             sheet.write(row, 0, move, normal)

#             # Default empty columns
#             balances = [None, None, None, None, None]

#             # If mapped, put dummy amounts (later connect to Odoo lines)
#             if move in mapping:
#                 for key, col in mapping[move].items():
#                     balances[col] = 100000  # placeholder amount

#             # Write balances
#             for col, val in enumerate(balances, start=1):
#                 if val is None:
#                     sheet.write(row, col, "", normal)
#                 else:
#                     sheet.write(row, col, val, currency)

#             row += 1

#         # Auto-fit column width
#         sheet.set_column(0, len(headers), 30)

#     # Later you can implement a fetch function from your report handler
#     # to replace dummy amounts with real computed balances.





class SocieReportHandler(models.AbstractModel):
    _name = "socie.report.handler"
    _inherit = "account.report.custom.handler"
    _description = "SOCIE Report Handler"

    filter_date = {'mode': 'range', 'filter': 'this_year'}

    ####################################################
    # Report Definition
    ####################################################
    def _get_report_name(self):
        return _("Statement of Changes in Equity")

    def _get_columns_name(self, options):
        return [
            {'name': _('Issued Share Capital')},
            {'name': _('Deposit for Shares')},
            {'name': _('Assets Revaluation')},
            {'name': _('Retained Earnings')},
            {'name': _('Total Equity')},
        ]

    def _get_lines(self, options, line_id=None):
        """Build SOCIE rows with computations mapped to columns"""
        lines = []

        movements = [
            "Profit for year",
            "New Capital issued during the year",
            "Loss for year",
            "Prior year adjustment to spare parts stock",
            "Write back of ED Salary",
            "COVID-19 Rebate from FGN",
            "Prepaid Lease Rental now recognised",
            "Stamp Duty paid on new Share Capital",
            "Bonus Issue made",
            "Revaluation of Aircraft",
            "Term Loan Swapped for Equity",
            "Additional shares Issued",
            "Prior year expenses paid",
            "Prior year Provision for ITF and NSITF",
            "Tax Audit liability paid",
            "Balance at end of the year",
        ]

        # Mapping rows → target equity column(s)
        # col index: 0=Issued Share Capital, 1=Deposit, 2=Revaluation, 3=Retained Earnings, 4=Total
        mapping = {
            "Profit for year": {3: self._get_profit_for_year(options)},
            "Loss for year": {3: self._get_loss_for_year(options)},
            "New Capital issued during the year": {0: self._get_new_capital(options)},
            "Bonus Issue made": {
                0: self._get_bonus_issue_capital(options),
                3: self._get_bonus_issue_retained(options),
            },
            "Revaluation of Aircraft": {2: self._get_revaluation(options)},
            "Additional shares Issued": {0: self._get_additional_shares(options)},
            "Term Loan Swapped for Equity": {0: self._get_loan_swap(options)},
            "Prior year adjustment to spare parts stock": {3: self._get_prior_adj_spares(options)},
            "Write back of ED Salary": {3: self._get_ed_salary_writeback(options)},
            "COVID-19 Rebate from FGN": {3: self._get_covid_rebate(options)},
            "Prepaid Lease Rental now recognised": {3: self._get_lease_adjustment(options)},
            "Stamp Duty paid on new Share Capital": {0: self._get_stamp_duty(options)},
            "Prior year expenses paid": {3: self._get_prior_expenses(options)},
            "Prior year Provision for ITF and NSITF": {3: self._get_prior_itf_nsitf(options)},
            "Tax Audit liability paid": {3: self._get_tax_audit(options)},
            "Balance at end of the year": {4: self._get_balance(options)},
        }

        for move in movements:
            balances = [0, 0, 0, 0, 0]
            if move in mapping:
                for col, value in mapping[move].items():
                    balances[col] = value or 0

            lines.append({
                'id': move.lower().replace(" ", "_"),
                'name': move,
                'columns': [{'name': self.format_value(val)} for val in balances],
                'level': 2,
            })

        return lines

    ####################################################
    # Computation helpers (fetching from account.move.line)
    ####################################################

    def _sum_account(self, options, account_codes):
        """Helper: sum balances of accounts by code list"""
        aml = self.env['account.move.line']
        query = aml.with_context(self._set_context(options)).read_group(
            domain=[('account_id.code', 'in', account_codes)],
            fields=['balance'],
            groupby=[]
        )
        return query and query[0]['balance'] or 0.0

    def _get_profit_for_year(self, options):
        # Link to P&L → net profit (Retained earnings)
        return self._sum_account(options, ['9999'])  # replace 9999 with retained earnings closing

    def _get_loss_for_year(self, options):
        val = self._get_profit_for_year(options)
        return val if val < 0 else 0

    def _get_new_capital(self, options):
        return self._sum_account(options, ['3000'])  # replace 3000 with your share capital accounts

    def _get_bonus_issue_capital(self, options):
        return self._sum_account(options, ['3001'])  # Bonus issues to capital

    def _get_bonus_issue_retained(self, options):
        return -self._sum_account(options, ['3001'])

    def _get_revaluation(self, options):
        return self._sum_account(options, ['3100'])  # Asset revaluation reserve

    def _get_additional_shares(self, options):
        return self._sum_account(options, ['3002'])  # new issues

    def _get_loan_swap(self, options):
        return self._sum_account(options, ['3200'])  # loan to equity swap

    def _get_prior_adj_spares(self, options):
        return self._sum_account(options, ['4001'])  # manual adjustments account

    def _get_ed_salary_writeback(self, options):
        return self._sum_account(options, ['5001'])  # reversal account

    def _get_covid_rebate(self, options):
        return self._sum_account(options, ['6001'])  # rebate/grant income

    def _get_lease_adjustment(self, options):
        return self._sum_account(options, ['4002'])  # lease adj account

    def _get_stamp_duty(self, options):
        return -self._sum_account(options, ['7001'])  # transaction cost

    def _get_prior_expenses(self, options):
        return self._sum_account(options, ['4003'])

    def _get_prior_itf_nsitf(self, options):
        return self._sum_account(options, ['4004'])

    def _get_tax_audit(self, options):
        return self._sum_account(options, ['4005'])

    def _get_balance(self, options):
        """Sum across all equity-related accounts"""
        return self._sum_account(options, ['3000', '3001', '3002', '3100', '3200'])

