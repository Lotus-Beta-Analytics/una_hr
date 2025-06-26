from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    payslip_count = fields.Integer(string='My Payslips', compute='_compute_payslip_count')

    def _compute_payslip_count(self):
        for employee in self:
            employee.payslip_count = self.env['hr.payslip'].search_count([('employee_id', '=', employee.id)])


    def open_payslips(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Payslips',
            'view_mode': 'tree,form',
            'res_model': 'hr.payslip',
            'domain': [('employee_id', '=', self.id)],
            'context': {'default_employee_id': self.id}
        }