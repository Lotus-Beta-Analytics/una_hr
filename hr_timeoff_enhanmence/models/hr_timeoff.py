from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
from datetime import timedelta


_logger = logging.getLogger(__name__)

class HrLeave(models.Model):
    _inherit = 'hr.leave'

    relief_staff_id = fields.Many2one('hr.employee', string="Relief Staff")
    relief_staff_confirmed = fields.Boolean(string="Relief Staff Confirmed", default=False)
    relief_staff_comment = fields.Text("Relief Staff Comment")
    relief_staff_confirmed_date = fields.Datetime(string="Relief Staff Confirmation Date", readonly=True)

    state = fields.Selection([
        ('confirm', 'draft'),
        ('line_manager', 'Line Manager To Approve'),
        ('hod', 'HOD To Approve'),
        ('hr_team', 'HR Team To Approve'),
        ('validate', 'Approved'),
        ('refuse', 'Refused'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, tracking=True, copy=False, default='confirm')

    is_relief_staff = fields.Boolean(
    string="Is Relief Staff",
    compute="_compute_is_relief_staff",
    store=False
)

    @api.depends('relief_staff_id')
    def _compute_is_relief_staff(self):
        for leave in self:
            leave.is_relief_staff = (
                leave.relief_staff_id.user_id == self.env.user
            )



    
    @api.model
    def create(self, vals):
        
        vals.setdefault('state', 'confirm')

        employee_id = vals.get('employee_id')
        relief_staff_id = vals.get('relief_staff_id')

        # Validate that employee and relief staff are not the same
        if employee_id and relief_staff_id and employee_id == relief_staff_id:
            raise UserError(_("An employee cannot be selected as their own relief staff."))

        # Create the leave record
        leave = super().create(vals)

        # Optional: Send relief staff notification if provided and valid
        if relief_staff_id:
            relief_staff = self.env['hr.employee'].browse(relief_staff_id)
            if relief_staff and relief_staff.work_email:
                try:
                    leave._send_relief_staff_notification(relief_staff)
                except Exception as e:
                    _logger.warning("Failed to send relief staff notification on creation: %s", e)
            else:
                _logger.warning("Relief staff on creation has no email or is invalid. ID: %s", relief_staff_id)

        return leave


        
    

    def write(self, vals):
        for leave in self:
            # Determine the current or incoming values for comparison
            employee_id = vals.get('employee_id') or leave.employee_id.id
            relief_staff_id = vals.get('relief_staff_id') or leave.relief_staff_id.id

            # Validate that employee and relief staff are not the same
            if employee_id == relief_staff_id and employee_id:
                raise UserError(_("An employee cannot be selected as their own relief staff."))

            # If relief staff has changed, notify them
            if 'relief_staff_id' in vals:
                new_relief = self.env['hr.employee'].browse(vals['relief_staff_id'])
                if new_relief and new_relief.work_email:
                    try:
                        leave._send_relief_staff_notification(new_relief)
                    except Exception as e:
                        _logger.warning("Failed to send relief staff notification: %s", e)
                else:
                    _logger.warning("New relief staff has no valid email. ID: %s", vals['relief_staff_id'])

        # Proceed with the standard write operation
        return super().write(vals)

        

    
    def action_confirm_relief_staff(self):
        for leave in self:
            if leave.relief_staff_id.user_id != self.env.user:
                raise UserError(_("Only the assigned relief staff can confirm availability."))
            if leave.relief_staff_confirmed:
                raise UserError(_("Already confirmed."))

            leave.relief_staff_confirmed = True
            leave.relief_staff_confirmed_date = fields.Datetime.now()

            leave.message_post(body=_(
                "Relief staff %s confirmed availability on %s."
            ) % (self.env.user.name, leave.relief_staff_confirmed_date))
            template = self.env.ref('hr_timeoff_enhanmence.mail_template_notify_employee_relief_confirmed', raise_if_not_found=False)
            if template:
                try:
                    template.send_mail(leave.id, force_send=True)
                except Exception as e:
                    _logger.warning("Failed to notify employee after relief staff confirmation: %s", e)


          

    def action_confirm(self):
        for leave in self:
            if leave.state != 'confirm':
                raise UserError(_("You can only submit a leave request that is in draft state. Please reset it to draft before resubmitting."))

            if not leave.relief_staff_id:
                raise UserError(_("Select a relief staff."))
            if not leave.relief_staff_confirmed:
                raise UserError(_("Relief staff must confirm availability."))
            # leave.state = 'line_manager'
            leave.write({'state': 'line_manager'})

            template = self.env.ref('hr_timeoff_enhanmence.mail_template_notify_line_manager_submission', raise_if_not_found=False)
            if template:
                try:
                    template.send_mail(leave.id, force_send=True)
                except Exception as e:
                    _logger.warning("Failed to notify line manager after staff submission: %s", e)

            return {'type': 'ir.actions.client', 'tag': 'reload'}

           
    def action_approve_line_manager(self):
        for leave in self:
            if leave.state != 'line_manager':
                raise UserError(_("Only leave requests in 'Line Manager To Approve' state can be approved by the Line Manager."))
            if not self.env.user.has_group('hr_timeoff_enhanmence.group_line_manager'):
                raise UserError(_("You are not authorized to approve at this stage."))

            # leave.state = 'hod'
            hod = leave.employee_id.department_id.manager_id
            template = self.env.ref('hr_timeoff_enhanmence.mail_template_notify_hod_leave_approval', raise_if_not_found=False)
            if template:
                try:
                    template.send_mail(leave.id, force_send=True)
                except Exception as e:
                    _logger.warning("Failed to send email to HOD: %s", e)
            leave.write({'state': 'hod'})
            return {'type': 'ir.actions.client', 'tag': 'reload'}
        

            
           
    def action_approve_hod(self):
        for leave in self:
            if leave.state != 'hod':
                raise UserError(_("Only leave requests in 'HOD To Approve' state can be approved by the HOD."))
            if not self.env.user.has_group('hr_timeoff_enhanmence.group_hod'):
                raise UserError(_("You are not authorized to approve at this stage."))
     
            # leave.state = 'hr_team'
            template = self.env.ref('hr_timeoff_enhanmence.mail_template_notify_hr_after_hod', raise_if_not_found=False)
            if template:
                try:
                    template.send_mail(leave.id, force_send=True)
                except Exception as e:
                    _logger.warning("Failed to send email to HR: %s", e)

            leave.write({'state': 'hr_team'})
            return {'type': 'ir.actions.client', 'tag': 'reload'}
        


           
    def action_approve_hr_team(self):
        for leave in self:
            if leave.state != 'hr_team':
                raise UserError(_("Only leave requests in 'HR Team To Approve' state can be approved by the HR team."))
            if not self.env.user.has_group('hr_timeoff_enhanmence.group_hr_team'):
                raise UserError(_("You are not authorized to approve at this stage."))

            leave.state = 'validate'  # Final approval
            leave.write({'state': 'validate'})
            leave.message_post(body=_("Leave approved by HR team."))
            
        # Send final approval email
            template = self.env.ref('hr_timeoff_enhanmence.mail_template_leave_final_approval', raise_if_not_found=False)
            if template:
                try:
                    template.send_mail(leave.id, force_send=True)
                except Exception as e:
                    _logger.warning("Failed to send final approval email: %s", e)
            else:
                _logger.warning("Final approval email template not found.")


    def _send_relief_staff_notification(self, relief_staff):
        for leave in self:
            if not relief_staff or not relief_staff.work_email:
                raise UserError(_("No work email found for the selected relief staff."))

            template = self.env.ref('hr_timeoff_enhanmence.mail_template_relief_notification', raise_if_not_found=False)
            if not template:
                raise UserError(_("Relief staff email template not found. Please check the configuration."))

            try:
                # Queue the email safely
                template.send_mail(leave.id, force_send=False)
            except Exception as e:
                raise UserError(_("Failed to queue relief staff email: %s") % str(e))

        
            
   