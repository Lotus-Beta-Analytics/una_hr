from odoo import fields, models

class HrCertification(models.Model):
    _name = "hr.certification"
    _description = "Applicant Certification"

    name = fields.Char()
