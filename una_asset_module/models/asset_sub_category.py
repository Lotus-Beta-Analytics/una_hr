# -*- coding: utf-8 -*-
from odoo import models, fields, api

class AssetSubCategory(models.Model):
    _name = 'asset.sub.category'
    _description = 'Asset Sub-Category'

    name = fields.Char(required=True)
    category_id = fields.Many2one('account.asset',  # link to account.asset
    string="Main Asset Model",
    domain="[('state', '=', 'model')]",  # same domain as your model_id field
    ondelete='restrict', required=True)

    # Explicit inverse_name to ensure Odoo finds the Many2one field
    asset_ids = fields.One2many(
        comodel_name='account.asset',
        inverse_name='sub_category_id',  # must match field in AccountAsset
        string='Assets'
    )

    asset_count = fields.Integer(string='Asset Count', compute='_compute_asset_count')

    @api.depends('asset_ids')
    def _compute_asset_count(self):
        for rec in self:
            rec.asset_count = len(rec.asset_ids)
