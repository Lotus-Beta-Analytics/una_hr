from odoo import models, fields, api
from datetime import datetime

class HrAppraisalReport(models.Model):
    _name = 'report.hr.appraisal.analytics'
    _description = 'Appraisal Analytics Report'
    _auto = False  # This is a view model

    employee_id = fields.Many2one('hr.employee', string="Employee")
    department_id = fields.Many2one('hr.department', string="Department")
    manager_id = fields.Many2one('hr.employee', string="Manager")
    state = fields.Selection([
        ('new', 'Draft'),
        ('submitted', 'Line Manager'),
        ('manager_approved', 'HR Manager'),
        ('hr_approved', 'Approved'),
        ('cancel', 'Cancelled'),
    ], string="Status")

    date = fields.Date(string="Date")
    month = fields.Char(string="Month")
    year = fields.Char(string="Year")
    final_score = fields.Float(string="Final Score")
    final_rating_label = fields.Char(string="Final Rating")

    def init(self):
        # Create or replace SQL view
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW report_hr_appraisal_analytics AS (
                SELECT
                    row_number() OVER () AS id,
                    a.id AS appraisal_id,
                    a.employee_id,
                    e.department_id,
                    a.manager_id,
                    a.state,
                    a.create_date::date AS date,
                    TO_CHAR(a.create_date, 'Month') AS month,
                    TO_CHAR(a.create_date, 'YYYY') AS year,
                    a.final_score,
                    a.final_rating_label
                FROM hr_appraisal a
                JOIN hr_employee e ON a.employee_id = e.id
            )
        """)
