# models/hr_contract.py
from odoo import models, fields

class HrContract(models.Model):
    _inherit = 'hr.contract'

    employee_salary = fields.Monetary(string="Employee Salary")
    accrued_arrears = fields.Monetary(string="Accrued Arrears/Proration")
    position_allowance = fields.Monetary(string="Position Allowance/Palliative")
    tax_rate = fields.Float(string="Tax Rate (%)")
    non_tax_rate = fields.Float(string="Non Tax Rate (%)")
    earned_income = fields.Monetary(string="Earned Income")
    cra = fields.Monetary(string="CRA (Consolidated Relief Allowance)")
    annual_paye_tax = fields.Monetary(string="Annual PAYE Tax")
    annual_tax_payable = fields.Monetary(string="Annual Tax Payable")
    monthly_tax_payable = fields.Monetary(string="Monthly Tax Payable")
    development_levy = fields.Monetary(string="Development Levy")
    life_assurance_premium = fields.Monetary(string="Life Assurance Premium")
    dfo_allowance = fields.Monetary(string="DFO Allowance")
    chief_pilot_allowance = fields.Monetary(string="Chief Pilot Allowance")
    flight_safety_allowance = fields.Monetary(string="Flight Safety Allowance")
    line_training_allowance = fields.Monetary(string="Line Training Allowance")
    line_maintenance_allowance = fields.Monetary(string="Line Maintenance Allowance")
    spare_repair_allowance = fields.Monetary(string="Spare Repair Allowance")
    monthly_reimbursable = fields.Monetary(string="Monthly Reimbursable")
    coop = fields.Monetary(string="Cooperative")
    salary_review_adjustment = fields.Monetary(string="Salary Review Adjustment")
    staff_loan = fields.Monetary(string="Staff Loan")
    evc = fields.Monetary(string="Employee Voluntary Contribution")
    resignation_adjustment = fields.Monetary(string="Resignation Adjustment")
    suspension_adjustment = fields.Monetary(string="Suspension Adjustment")
    leave_of_absence_adjustment = fields.Monetary(string="Leave of Absence Adjustment")
    termination_adjustment = fields.Monetary(string="Termination Adjustment")
    checkout_adjustment = fields.Monetary(string="Checkout Adjustment")

    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self.env.company.currency_id)
