from odoo import models, fields, api, _

class HrDepartmentStation(models.Model):
    _name = 'hr.department.station'
    _description = 'Department / Station'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')
    note = fields.Text(string='Notes')


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    department_station_id = fields.Many2one(
        'hr.department.station',  # Replace with your model
        string="Department/Station"
    )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        department_station = self.env['ir.config_parameter'].sudo().get_param('your_module.department_station_id')
        if department_station:
            res.update(department_station_id=int(department_station))
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('your_module.department_station_id', self.department_station_id.id if self.department_station_id else False)
