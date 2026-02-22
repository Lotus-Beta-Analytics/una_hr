# -*- coding: utf-8 -*-
# from odoo import http


# class UnaAssetModule(http.Controller):
#     @http.route('/una_asset_module/una_asset_module', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/una_asset_module/una_asset_module/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('una_asset_module.listing', {
#             'root': '/una_asset_module/una_asset_module',
#             'objects': http.request.env['una_asset_module.una_asset_module'].search([]),
#         })

#     @http.route('/una_asset_module/una_asset_module/objects/<model("una_asset_module.una_asset_module"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('una_asset_module.object', {
#             'object': obj
#         })

