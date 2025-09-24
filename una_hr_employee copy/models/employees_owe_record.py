from odoo import models, fields, api, _

class HREmployee(models.Model):
    _inherit = 'hr.employee'

    has_badges = fields.Boolean(string="Has Badges", compute='_compute_badge_ids', store=True)
    badge_ids = fields.Many2many(
        'gamification.badge',
        compute='_compute_badge_ids',
        string='Badges',
        readonly=True
    )

    @api.depends('user_id')
    def _compute_badge_ids(self):
        for employee in self:
            if employee.user_id:
                badge_users = self.env['gamification.badge.user'].search([
                    ('user_id', '=', employee.user_id.id)
                ])
                badges = badge_users.mapped('badge_id')
            else:
                badges = self.env['gamification.badge']
            
            employee.badge_ids = badges
            employee.has_badges = bool(badges)


class HrEmployeePublic(models.Model):
    _inherit = 'hr.employee.public'

    has_badges = fields.Boolean(string="Has Badges", compute='_compute_badge_ids', store=True)
    badge_ids = fields.Many2many(
        'gamification.badge',
        compute='_compute_badge_ids',
        string='Badges',
        readonly=True
    )

    @api.depends('user_id')
    def _compute_badge_ids(self):
        for employee in self:
            if employee.user_id:
                badge_users = self.env['gamification.badge.user'].search([
                    ('user_id', '=', employee.user_id.id)
                ])
                badges = badge_users.mapped('badge_id')
            else:
                badges = self.env['gamification.badge']

            employee.badge_ids = badges
            employee.has_badges = bool(badges)
