from odoo import models, fields, api, _

class HrDepartment(models.Model):
    _inherit = 'hr.department'

    head_of_department_id = fields.Many2one(
        'res.users',
        string='DIRECTOR',
        compute='_compute_head_of_department',
        store=True,
        readonly=True
    )

    @api.depends('parent_id', 'parent_id.manager_id', 'parent_id.manager_id.user_id')
    def _compute_head_of_department(self):
        for dept in self:
            dept.head_of_department_id = dept.parent_id.manager_id.user_id


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    head_of_department_id = fields.Many2one(
        'res.users',
        string='DIRECTOR',
        compute='_compute_head_of_department',
        store=True,
        readonly=True
    )

    @api.depends(
        'department_id',
        'department_id.parent_id',
        'department_id.parent_id.manager_id',
        'department_id.parent_id.manager_id.user_id'
    )
    def _compute_head_of_department(self):
        for employee in self:
            employee.head_of_department_id = employee.department_id.parent_id.manager_id.user_id
