from odoo.addons.website_hr_recruitment.controllers.main import WebsiteHrRecruitment
from odoo.http import request
import base64

class WebsiteHrRecruitmentExtended(WebsiteHrRecruitment):

    def _prepare_application_values(self, job, **post):
        values = super()._prepare_application_values(job, **post)

        # Add standard fields
      

        # Add basic file uploads
        cert_file = request.httprequest.files.get('certifications_file')
        if cert_file:
            values['certifications_file'] = base64.b64encode(cert_file.read())
            values['certifications_filename'] = cert_file.filename

        cl_file = request.httprequest.files.get('cover_letter_file')
        if cl_file:
            values['cover_letter_file'] = base64.b64encode(cl_file.read())
            values['cover_letter_filename'] = cl_file.filename

        return values

    def _post(self, job, **post):
        values = self._prepare_application_values(job, **post)
        applicant = request.env['hr.applicant'].sudo().create(values)

        # Handle dynamic multiple certification uploads
        cert_names = request.params.getlist('certification_name')
        date_obtained = request.params.getlist('date_obtained')
        expiration_date = request.params.getlist('expiration_date')
        cert_files = request.httprequest.files.getlist('certification_file')

        for i in range(len(cert_names)):
            if not cert_names[i] or not date_obtained[i] or not cert_files[i]:
                continue  # skip invalid entries

            file = cert_files[i]
            request.env['hr.applicant.certification'].sudo().create({
                'applicant_id': applicant.id,
                'certification_name': cert_names[i],
                'date_obtained': date_obtained[i],
                'expiration_date': expiration_date[i] or False,
                'certification_file': base64.b64encode(file.read()),
                'certification_filename': file.filename,
            })

        return applicant
