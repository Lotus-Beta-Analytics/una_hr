# -*- coding: utf-8 -*-

from odoo import models, fields, api



class AssetSubCategory(models.Model):
    _name = 'asset.sub.category'
    _description = 'Asset Sub-Category'

    name = fields.Char(required=True)
    category_id = fields.Many2one('account.asset.category', string="Main Category", required=True)
    asset_ids = fields.One2many('account.asset', 'sub_category_id', string='Assets')
    asset_count = fields.Integer(string='Asset Count', compute='_compute_asset_count')

    @api.depends('asset_ids')
    def _compute_asset_count(self):
        for rec in self:
            rec.asset_count = len(rec.asset_ids)