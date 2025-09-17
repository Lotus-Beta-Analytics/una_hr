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
            {'name': _('Issued Share Capital')},
            {'name': _('Deposit for Shares')},
            {'name': _('Assets Revaluation')},
            {'name': _('Retained Earnings')},
            {'name': _('Total Equity')},
        ]

    def _get_lines(self, options, line_id=None):
        lines = []
        # Example structure, formulas will come later
        lines.append(self._build_line(_("Balance at end of the year - 2020")))
        lines.append(self._build_line(_("Profit for year")))
        lines.append(self._build_line(_("Balance at end of the year - 2021")))
        lines.append(self._build_line(_("New Capital issued during the year")))
        lines.append(self._build_line(_("Loss for year")))
        lines.append(self._build_line(_("Prior year adjustment to spare parts stock")))
        lines.append(self._build_line(_("Balance at end of the year - 2022")))
        lines.append(self._build_line(_("New Capital issued during the year")))
        lines.append(self._build_line(_("Write back of ED Salary")))
        lines.append(self._build_line(_("COVID-19 Rebate from FGN")))
        lines.append(self._build_line(_("Prepaid Lease Rental now recognised")))
        lines.append(self._build_line(_("Profit for year 2023")))
        lines.append(self._build_line(_("Balance at end of the year - 2023")))
        lines.append(self._build_line(_("New Capital issued during the year")))
        lines.append(self._build_line(_("Stamp Duty paid on new Share Capital")))
        lines.append(self._build_line(_("Bonus Issue made")))
        lines.append(self._build_line(_("Revaluation of Aircraft")))
        lines.append(self._build_line(_("Term Loan Swapped for Equity")))
        lines.append(self._build_line(_("Additional shares Issued")))
        lines.append(self._build_line(_("Prior year expenses paid")))
        lines.append(self._build_line(_("Prior year Provision for ITF and NSITF")))
        lines.append(self._build_line(_("Tax Audit liability paid")))
        lines.append(self._build_line(_("Profit for year 2024")))
        lines.append(self._build_line(_("Balance at end of the year - 2024")))
        return lines

    def _build_line(self, name):
        return {
            'id': name,
            'name': name,
            'columns': [{'name': ''}] * 5,  # 5 columns
            'level': 2,
        }
