from odoo import models, fields, api, _

class HrEmployeePublic(models.Model):
    _inherit = "hr.employee.public"

    # Employee Confirmation
    confirmation_status = fields.Selection(related="employee_id.confirmation_status", readonly=True)
    confirmation_date = fields.Date(related="employee_id.confirmation_date", readonly=True)

    # Custom IDs
    emp_id = fields.Char(related="employee_id.emp_id", readonly=True)
    external_id = fields.Char(related="employee_id.external_id", readonly=True)
    irs_state_id = fields.Many2one(related="employee_id.irs_state_id", readonly=True)

    # Next of Kin
    next_of_kin_name = fields.Char(related="employee_id.next_of_kin_name", readonly=True)
    next_of_kin_relationship = fields.Char(related="employee_id.next_of_kin_relationship", readonly=True)
    next_of_kin_phone = fields.Char(related="employee_id.next_of_kin_phone", readonly=True)
    next_of_kin_email = fields.Char(related="employee_id.next_of_kin_email", readonly=True)
    next_of_kin_address = fields.Text(related="employee_id.next_of_kin_address", readonly=True)

    # Certificates
    birth_certificate_filename = fields.Char(related="employee_id.birth_certificate_filename", readonly=True)
    education_certificate_filename = fields.Char(related="employee_id.education_certificate_filename", readonly=True)

    # Department
    head_of_department_id = fields.Many2one(related="employee_id.head_of_department_id", readonly=True)
    leave_manager_id = fields.Many2one('res.users', string="Leave Manager")

    # Travel Ticket Fields (added)
    join_date = fields.Date(related="employee_id.join_date", readonly=True)


    # image_1920 = fields.Image(
    #     string='Profile Image',
    #     compute='_compute_image_1920',
    #     inverse='_inverse_image_1920',
    #     store=False,
    # )

    # @api.depends('employee_id.image_1920')
    # def _compute_image_1920(self):
    #     for record in self:
    #         record.image_1920 = record.employee_id.image_1920

    # def _inverse_image_1920(self):
    #     for record in self:
    #         if record.employee_id and record.employee_id.user_id.id == self.env.uid:
    #             record.employee_id.image_1920 = record.image_1920


    
