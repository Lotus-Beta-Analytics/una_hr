from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    probation_category_id = fields.Many2one(
        'ir.module.category',
        compute='_compute_probation_category_id',
        store=False
    )

    probation_groups_ids = fields.Many2many(
        'res.groups',
        compute='_compute_probation_groups',
        inverse='_inverse_probation_groups',
        string="Probation Access",
        store=False,
    )

    def _compute_probation_category_id(self):
        category = self.env.ref(
            'una_employee_probation_form.module_category_probation_reviews'
        )
        for rec in self:
            rec.probation_category_id = category.id

    @api.depends('groups_id')
    def _compute_probation_groups(self):
        category = self.env.ref(
            'una_employee_probation_form.module_category_probation_reviews'
        )
        for rec in self:
            rec.probation_groups_ids = rec.groups_id.filtered(
                lambda g: g.category_id == category
            )

    def _inverse_probation_groups(self):
        category = self.env.ref(
            'una_employee_probation_form.module_category_probation_reviews'
        )
        for rec in self:
            # Remove all groups in this category
            other_groups = rec.groups_id.filtered(
                lambda g: g.category_id != category
            )
            rec.groups_id = other_groups | rec.probation_groups_ids


