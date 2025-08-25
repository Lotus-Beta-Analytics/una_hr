from odoo import models, fields, api,_
from odoo.exceptions import UserError 
from odoo.exceptions import ValidationError
import logging

from datetime import date
from dateutil.relativedelta import relativedelta

class HrAppraisal(models.Model):
    _inherit = 'hr.appraisal'

    previous_manager_id = fields.Many2one('hr.employee', string="Previous Manager", compute='_compute_previous_manager', store=True)
    requires_previous_manager_consultation = fields.Boolean(string="Requires Previous Manager Consultation", compute='_compute_previous_manager', store=True)

    @api.depends('employee_id', 'manager_id', 'date')
    def _compute_previous_manager(self):
        for rec in self:
            rec.previous_manager_id = False
            rec.requires_previous_manager_consultation = False

            if rec.employee_id and rec.manager_id and rec.date:
                # Get latest manager history for this employee before appraisal date
                history = self.env['hr.appraisal.manager.history'].search([
                    ('employee_id', '=', rec.employee_id.id),
                    ('new_manager_id', '=', rec.manager_id.id),
                    ('transfer_date', '<=', rec.date),
                ], order='transfer_date desc', limit=1)

                if history:
                    delta = relativedelta(rec.date, history.transfer_date)
                    if delta.months + delta.years * 12 < 6:
                        rec.previous_manager_id = history.previous_manager_id
                        rec.requires_previous_manager_consultation = True

class HrAppraisalManagerHistory(models.Model):
    _name = 'hr.appraisal.manager.history'
    _description = 'Employee Manager History'

    employee_id = fields.Many2one('hr.employee', string="Employee", required=True, index=True)
    previous_manager_id = fields.Many2one('hr.employee', string="Previous Manager", required=True)
    new_manager_id = fields.Many2one('hr.employee', string="New Manager", required=True)
    transfer_date = fields.Date(string="Transfer Date", required=True, default=fields.Date.today)

    appraisal_id = fields.Many2one('hr.appraisal', string="Related Appraisal", ondelete='cascade')

