from odoo import models, fields

class HrEmployeePublic(models.Model):
    _inherit = "hr.employee.public"

    ticket_limit = fields.Integer(related="employee_id.ticket_limit", readonly=True)
    tickets_used_this_year = fields.Integer(related="employee_id.tickets_used_this_year", readonly=True)
    ticket_approved_count = fields.Integer(related="employee_id.ticket_approved_count", readonly=True)
    travel_date = fields.Date(related="employee_id.travel_date", readonly=True)
    return_date = fields.Date(related="employee_id.return_date", readonly=True)