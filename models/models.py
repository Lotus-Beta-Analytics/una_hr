# -*- coding: utf-8 -*-

from odoo import models, fields, api




# This add the location table to the asset model in odoo
class AssetLocation(models.Model):
    _name = 'asset.location'
    _description = 'Asset Location'

    name = fields.Char(string='Location Name')


# This adds the custom fields and then other customized fields.
class una_asset_module(models.Model): 
    _inherit = 'account.asset'

    asset_location_id = fields.Many2one('asset.location', string='Asset Location')
    asset_serial = fields.Char(string='Registration Number')
    asset_invoice = fields.Many2one('account.move', string='Invoice')
    asset_supplier = fields.Many2one('res.partner', string='Supplier')