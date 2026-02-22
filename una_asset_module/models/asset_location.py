# -*- coding: utf-8 -*-

from odoo import models, fields, api



class AssetLocation(models.Model):
    _name = 'asset.location'
    _description = 'Asset Location'

    name = fields.Char(string='Location Name')