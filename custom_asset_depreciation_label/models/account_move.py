# custom_asset_label/models/account_move.py
from odoo import models, fields, api
from datetime import datetime

class AccountMove(models.Model):
    """
    Override account.move to customize depreciation journal entry labels.
    Sets reference to: BEING DEPRECIATION AT THE MONTH ENDED [MONTH_NAME]
    """
    _inherit = 'account.move'
    
    @api.model_create_multi
    def create(self, vals_list):
        """
        Override the create method to automatically set labels
        for depreciation journal entries when they are created.
        """
        # Call the parent create method first
        moves = super().create(vals_list)
        
        # Process each newly created move
        for move in moves:
            # Check if this is a depreciation move (has asset_id)
            if move.asset_id and move.date:
                self._update_move_label(move)
        
        return moves
    
    def write(self, vals):
        """
        Override write method to update labels when move date changes
        """
        # Store original dates before modification
        original_dates = {move.id: move.date for move in self}
        
        # Call parent write method
        result = super().write(vals)
        
        # If date was changed, update labels for depreciation moves
        if 'date' in vals:
            for move in self:
                if (move.asset_id and 
                    move.date and 
                    move.date != original_dates.get(move.id)):
                    self._update_move_label(move)
        
        return result
    
    def _update_move_label(self, move):
        """
        Helper method to update the label for a depreciation move
        """
        # Get month name from the move date (convert to uppercase)
        month_name = move.date.strftime('%B').upper()
        
        # Create the new reference/label
        new_label = f"BEING DEPRECIATION AT THE MONTH ENDED {month_name}"
        
        # Update the move reference
        move.ref = new_label
        
        # Also update the name of each journal item for consistency
        for line in move.line_ids:
            line.name = new_label
    
    def action_update_labels_manually(self):
        """
        Manual action to update labels for selected moves.
        This can be used as a button in the UI if needed.
        """
        updated_count = 0
        
        for move in self:
            if move.asset_id and move.date:
                self._update_move_label(move)
                updated_count += 1
        
        # Show confirmation message
        message = f"Updated labels for {updated_count} depreciation entries"
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': message,
                'type': 'success',
                'sticky': False,
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }