from odoo import models, fields

import base64
from odoo.http import request
from odoo.addons.website_hr_recruitment.controllers.main import WebsiteHrRecruitment

class HrApplicantCertification(models.Model):
    _name = 'hr.applicant.certification'
    _description = 'Applicant Professional Certification'

    applicant_id = fields.Many2one('hr.applicant', required=True, ondelete='cascade')
    certification_file = fields.Binary(string="Certification File", required=True)
    certification_filename = fields.Char(string="Filename", required=True)
    certification_name = fields.Char(string="Certification Name", required=True)
    date_obtained = fields.Date(required=True)
    expiration_date = fields.Date()


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    certification_ids = fields.One2many(
        'hr.applicant.certification',
        'applicant_id',
        string="Professional Certifications"
    )
    applicant_id = fields.Many2one('hr.applicant', required=True, ondelete='cascade')
    certification_file = fields.Binary(string="Certification File", required=True)
    certification_filename = fields.Char(string="Filename", required=True)
    certification_name = fields.Char(string="Certification Name", required=True)
    date_obtained = fields.Date(required=True)
    expiration_date = fields.Date() 

    cover_letter_file = fields.Binary(string="Cover Letter")
    cover_letter_filename = fields.Char(string="Cover Letter Filename")
class WebsiteHrRecruitmentExtended(WebsiteHrRecruitment):

    def _prepare_application_values(self, job, **post):
        values = super()._prepare_application_values(job, **post)
        values.update({
            'field_of_study': post.get('field_of_study'),
            'degree': post.get('degree'),
            'degree_class': post.get('degree_class'),
            'skills': post.get('skills'),
        })

        return values

    def _post(self, job, **post):
        vals = self._prepare_application_values(job, **post)
        applicant = request.env['hr.applicant'].sudo().create(vals)

        # Multiple certifications
        certification_names = request.params.getlist('certification_name')
        dates_obtained = request.params.getlist('date_obtained')
        expiration_dates = request.params.getlist('expiration_date')
        cert_files = request.httprequest.files.getlist('certification_file')

        for i in range(len(certification_names)):
            if not certification_names[i] or not dates_obtained[i] or not cert_files[i]:
                continue  # Skip incomplete entries

            file = cert_files[i]
            request.env['hr.applicant.certification'].sudo().create({
                'applicant_id': applicant.id,
                'certification_name': certification_names[i],
                'date_obtained': dates_obtained[i],
                'expiration_date': expiration_dates[i] or False,
                'certification_file': base64.b64encode(file.read()),
                'certification_filename': file.filename,
            })

        return applicant
