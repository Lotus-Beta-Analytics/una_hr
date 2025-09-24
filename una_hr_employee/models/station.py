from odoo import models, fields,api,_

class HREmployeeStation(models.Model):
    _name = 'hr.employee.station'
    _description = 'Employee Department/Station'
    _order = 'name'

    station_ids= fields.Char(string='Station Name', store=True)
  
    name = fields.Char(string="Station Name", store=True)

class HREmployee(models.Model):
    _inherit = 'hr.employee'

    station_id = fields.Many2one('hr.employee.station', string='Station', store =True)
