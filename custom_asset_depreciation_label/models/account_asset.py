from odoo import models, fields, api
from datetime import datetime

class AccountAsset(models.Model):
    _inherit = 'account.asset'
    
    def _create_move(self, depreciation_date, depreciation_amount, move_type, journal_id):
        """
        Override the method that creates depreciation journal entries
        This is called when generating depreciation moves
        """
        # Call parent method to create the move
        move = super()._create_move(depreciation_date, depreciation_amount, move_type, journal_id)
        
        if move:
            # Format the month name from depreciation date
            month_name = self._get_month_name_from_date(depreciation_date)
            
            # Create the custom label
            new_label = f"BEING DEPRECIATION AT THE MONTH ENDED {month_name}"
            
            # Update the move reference
            move.ref = new_label
            
            # Update all journal items (move lines)
            for line in move.line_ids:
                line.name = new_label
        
        return move
    
    def _get_month_name_from_date(self, date_value):
        """Helper method to extract month name from date"""
        if isinstance(date_value, str):
            dep_date = fields.Date.from_string(date_value)
        else:
            dep_date = date_value
        
        return dep_date.strftime('%B').upper()
    
    def validate(self):
        """Also update acquisition entry when asset is validated"""
        res = super().validate()
        
        for asset in self:
            # Update acquisition move if exists
            if asset.original_move_line_ids:
                acq_date = asset.acquisition_date or fields.Date.today()
                month_name = self._get_month_name_from_date(acq_date)
                new_label = f"BEING ASSET ACQUISITION AT THE MONTH ENDED {month_name}"
                
                # Update the original move (acquisition)
                for move_line in asset.original_move_line_ids:
                    if move_line.move_id:
                        move_line.move_id.ref = new_label
                        for line in move_line.move_id.line_ids:
                            line.name = new_label
        
        return res