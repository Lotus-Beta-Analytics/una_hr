# -*- coding: utf-8 -*-

from odoo import models, fields, api



# class AssetLocation(models.Model):
#     _name = 'asset.location'
#     _description = 'Asset Location'

#     name = fields.Char(string='Location Name')


# class AssetSubCategory(models.Model):
#     _name = 'asset.sub.category'
#     _description = 'Asset Sub-Category'

#     name = fields.Char(required=True)
#     category_id = fields.Many2one('account.asset.category', string="Main Category", required=True)
#     asset_ids = fields.One2many('account.asset', 'sub_category_id', string='Assets')
#     asset_count = fields.Integer(string='Asset Count', compute='_compute_asset_count')

#     @api.depends('asset_ids')
#     def _compute_asset_count(self):
#         for rec in self:
#             rec.asset_count = len(rec.asset_ids)


class AccountAsset(models.Model):
    _inherit = 'account.asset'

    sub_category_id = fields.Many2one('asset.sub.category', string="Sub-Category")
    asset_location_id = fields.Many2one('asset.location', string='Asset Location/User Dept')
    asset_serial = fields.Char(string='Registration Number')
    asset_supplier = fields.Many2one('res.partner', string='Supplier')
    quantity = fields.Float(string="Quantity")
    unit_price = fields.Float(string="Unit Price", compute="_compute_unit_price", store=True)

    product_id = fields.Many2one('product.product', string='Related Product')

    # parent_id = fields.Many2one('account.asset', string="Parent Category", index=True)
    # child_ids = fields.One2many('account.asset', 'parent_id', string="Subcategories")

    main_category_asset_count = fields.Integer(string="Assets under Main Category")
    sub_asset_count = fields.Integer(string="Assets under Subcategories")

    bill_id = fields.Many2one('account.move', string="Bill", compute='_compute_bill_id', store=False)

    non_depreciable_percentage = fields.Selection([
        ('0.00', '0%'),
        ('0.05', '5%'),
        ('0.10', '10%'),
        ('0.15', '15%'),
        ('0.20', '20%'),
        ('0.25', '25%'),
        ('0.30', '30%'),
    ], string='Non-Depreciable %', default='0.00')

    @api.onchange('non_depreciable_percentage', 'original_value')
    def _compute_salvage_value_from_selection(self):
        for record in self:
            if record.non_depreciable_percentage and record.original_value:
                percent = float(record.non_depreciable_percentage)
                record.salvage_value = record.original_value * percent


    # compute logic to add invoice/bill to the tree view
    @api.depends('original_move_line_ids.move_id')
    def _compute_bill_id(self):
        for asset in self:
            # Pick the first related bill from move lines
            bill_moves = asset.original_move_line_ids.mapped('move_id').filtered(lambda m: m.move_type == 'in_invoice')
            asset.bill_id = bill_moves[:1].id if bill_moves else False

    # @api.depends('child_ids.child_ids')
    # def _compute_asset_counts(self):
    #     for rec in self:
    #         rec.main_category_asset_count = len(rec.child_ids or [])
    #         rec.sub_asset_count = sum(len(child.child_ids or []) for child in rec.child_ids or [])

    @api.depends('original_value', 'quantity')
    def _compute_unit_price(self):
        for asset in self:
            asset.unit_price = (asset.original_value / asset.quantity) if asset.quantity else 0.0


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def _get_asset_values(self):
        values = super()._get_asset_values()
        if values:
            values['invoice_id'] = self.move_id.id
            values['invoice_line_id'] = self.id
        return values
















# # This add the location table to the asset model in odoo
# class AssetLocation(models.Model):
#     _name = 'asset.location'
#     _description = 'Asset Location'

#     name = fields.Char(string='Location Name')




# # models/asset_sub_category.py
# class AssetSubCategory(models.Model):
#     _name = 'asset.sub.category'
#     _description = 'Asset Sub-Category'

#     name = fields.Char(required=True)
#     category_id = fields.Many2one('account.asset.category', string="Main Category", required=True)





# # This adds the custom fields and then other customized fields.
# class una_asset_module(models.Model): 
#     _inherit = 'account.asset'

#     sub_category_id = fields.Many2one('asset.sub.category', string="Sub-Category")
#     asset_location_id = fields.Many2one('asset.location', string='Asset Location/User Dept')
#     asset_serial = fields.Char(string='Registration Number')
#     asset_invoice = fields.Many2one('account.move', string='Invoice')
#     asset_supplier = fields.Many2one('res.partner', string='Supplier')

#     # Fields to show quantity and unit prices
#     quantity = fields.Float(string="Quantity")
#     unit_price = fields.Float(string="Unit Price", compute="_compute_unit_price", store=True)

#     # Fields to show invoice number
#     invoice_id = fields.Many2one('account.move', string="Invoice")
#     invoice_name = fields.Char(related='invoice_id.name', string='Invoice Number', readonly=True)
#     invoice_line_id = fields.Many2one('account.move.line', string='Invoice Line')
#     product_id = fields.Many2one('product.product', string='Related Product')

#     # Asset Components Accounting
#     parent_id = fields.Many2one('account.asset', string="Parent Category", index=True)
#     child_ids = fields.One2many('account.asset', 'parent_id', string="Subcategories")

#     asset_count = fields.Integer(string="Assets", compute="_compute_asset_counts")
#     sub_asset_count = fields.Integer(string="Subcategory Assets", compute="_compute_asset_counts")

#     # Compute asset sub-category count
#     @api.depends('account_asset_ids', 'child_ids.account_asset_ids')
#     def _compute_asset_counts(self):
#         for rec in self:
#             rec.asset_count = len(rec.account_asset_ids)
#             rec.sub_asset_count = sum(len(child.account_asset_ids) for child in rec.child_ids)


    
#     @api.depends('original_value', 'quantity')
#     def _compute_unit_price(self):
#         for asset in self:
#             asset.unit_price = (asset.original_value / asset.quantity) if asset.quantity else 0.0
    


#     @api.model
#     def create(self, vals):
#         # Automatically assign the parent asset from context if not already set
#         if not vals.get('parent_asset_id') and self.env.context.get('default_parent_asset_id'):
#             vals['parent_asset_id'] = self.env.context['default_parent_asset_id']
#         # Set is_parent_asset = False for all new records unless explicitly set
#         if 'is_parent_asset' not in vals:
#             vals['is_parent_asset'] = False
#         return super().create(vals)

    
# class AccountMoveLine(models.Model):
#     _inherit = 'account.move.line'

#     def _get_asset_values(self):
#         """Add quantity from invoice line to asset creation."""
#         values = super()._get_asset_values()
#         if values:
#             values['invoice_id'] = self.move_id.id
#             values['invoice_line_id'] = self.id
#         return values