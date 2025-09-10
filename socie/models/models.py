# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.osv.expression import AND

# class StatementChangeInEquityReport(models.Model):
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
            {'name': _('Profit for year')},
            {'name': _('New Capital issued during the year')},
            {'name': _('Loss for year')},
            {'name': _('Prior year adjustment to spare parts stock')},
            {'name': _('Write back of ED Salary')},
            {'name': _('COVID-19 Rebate from FGN')},
            {'name': _('Prepaid Lease Rental now recognised')},
            {'name': _('Stamp Duty paid on new Share Capital')},
            {'name': _('Bonus Issue made')},
            {'name': _('Revaluation of Aircraft')},
            {'name': _('Term Loan Swapped for Equity')},
            {'name': _('Additional shares Issued')},
            {'name': _('Prior year expenses paid')},
            {'name': _('Prior year Provision for ITF and NSITF')},
            {'name': _('Tax Audit liability paid')},
            {'name': _('Balance at end of the year')},
    ]





        #     {'name': _('Issued Share Capital')},
        #     {'name': _('Deposit for Shares')},
        #     {'name': _('Assets Revaluation')},
        #     {'name': _('Retained Earnings')},
        #     {'name': _('Total Equity')},
        # ]

    def _get_lines(self, options, line_id=None):
        lines = []
        # Example structure, formulas will come later
        lines.append(self._build_line(_("Issued Share Capital")))
        lines.append(self._build_line(_("Deposit for Shares")))
        lines.append(self._build_line(_("Assets Revaluation")))
        lines.append(self._build_line(_("Retained Earnings")))
        lines.append(self._build_line(_("Total Equity")))
        return lines

    # def _build_line(self, name):
    #     return {
    #         'id': name,
    #         'name': name,
    #         'columns': [{'name': ''}] * 5,  # 5 columns
    #         'level': 2,
    #     }
