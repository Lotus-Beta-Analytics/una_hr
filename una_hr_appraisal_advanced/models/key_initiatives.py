from odoo import models, fields, api,_
from odoo.exceptions import UserError 
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)
class AppraisalKeyInitiative(models.Model):
    _name = 'appraisal.key.initiative'
    _description = 'Appraisal Key Initiative'
    _rec_name = 'name'

    name = fields.Char(required=True)
    # description = fields.Text()
    department_id = fields.Many2one('hr.department', string='Department', default=lambda self: self._default_department_id())

    @api.model
    def _default_department_id(self):
        """Fetch the department of the logged-in user's employee."""
        user = self.env.user
        employee = self.env['hr.employee'].search([('user_id', '=', user.id)], limit=1)
        if employee and employee.department_id:
            return employee.department_id.id
        return None

class AppraisalKPI(models.Model):
    _name = 'appraisal.kpi'
    _description = 'Appraisal KPI'
    _rec_name = 'name'

    name = fields.Char(required=True)
    # description = fields.Text()
    department_id = fields.Many2one('hr.department', string='Department', default=lambda self: self._default_department_id())
    
    @api.model
    def _default_department_id(self):
        """Fetch the department of the logged-in user's employee."""
        user = self.env.user
        employee = self.env['hr.employee'].search([('user_id', '=', user.id)], limit=1)
        if employee and employee.department_id:
            return employee.department_id.id
        return None

class AppraisalBulkObjectiveWizard(models.TransientModel):
    _name = 'appraisal.bulk.objective.wizard'
    _description = 'Bulk Create Strategic Objectives for Departments'

    department_ids = fields.Many2many(
        'hr.department',
        string="Departments",
        required=True
    )
    functional_objective = fields.Char(
        string="Functional Objective",
        required=True
    )
    weight = fields.Float(string="Weight (70%)", required=True, default=0.0)

    key_initiative_ids = fields.Many2many(
        'appraisal.key.initiative',
        string="Key Initiatives"
    )
    kpi_ids = fields.Many2many(
        'appraisal.kpi',
        string="KPIs"
    )

    def action_create_objectives(self):
        """Create objectives, initiatives, and KPIs for selected departments"""
        for dept in self.department_ids:
            self.env['appraisal.strategic.objective.config'].create({
                'name': self.functional_objective,
                'department_id': dept.id,
                'weight': self.weight,
                'key_initiative_ids': [(6, 0, self.key_initiative_ids.ids)],
                'kpi_ids': [(6, 0, self.kpi_ids.ids)],
            })
