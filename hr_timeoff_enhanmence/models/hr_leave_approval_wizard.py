from odoo import models, fields, api, _
from odoo.exceptions import UserError

class HrLeaveApprovalWizard(models.TransientModel):
    _name = 'hr.leave.approval.wizard'
    _description = 'Leave Approval Comments'

    leave_id = fields.Many2one('hr.leave', required=True, string="Leave Request", readonly=True)
    comment = fields.Text("Approval Comment", required=True)

    def confirm_approval(self):
        self.ensure_one()
        leave = self.leave_id

        if leave.state == 'line_manager':
            leave.message_post(body=_("Line Manager Comment: %s") % self.comment)
            leave.action_approve_line_manager()
        elif leave.state == 'hod':
            leave.message_post(body=_("HOD Comment: %s") % self.comment)
            leave.action_approve_hod()

        elif leave.state == 'hr_team':
            leave.message_post(body=_("HR Team Comment: %s") % self.comment)
            leave.action_approve_hr_team()    
        else:
            raise UserError(_("This leave is not in a state to approve via this wizard."))

        return {'type': 'ir.actions.act_window_close'}
