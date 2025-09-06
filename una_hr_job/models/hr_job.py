# models/hr_job.py
from odoo import models, fields, api, _

class HrJob(models.Model):
    _inherit = 'hr.job'

    cover_letter_digitization = fields.Selection([
        ('none', 'Do not digitize'),
        ('on_demand', 'Digitize on demand only'),
        ('auto', 'Digitize automatically')
    ], default='none', string="Cover Letter Digitization")

    certificate_digitization = fields.Selection([
        ('none', 'Do not digitize'),
        ('on_demand', 'Digitize on demand only'),
        ('auto', 'Digitize automatically')
    ], default='none', string="Certificate Digitization")
