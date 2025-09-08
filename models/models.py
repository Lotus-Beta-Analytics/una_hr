# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EmployeePayslip(models.Model):
    _inherit = 'hr.payslip'
    _order = 'date_from desc'
    

    def action_print_payslip(self):
        return self.env.ref("hr_payroll.hr_payslip_action_report_pdf").report_action(self)

