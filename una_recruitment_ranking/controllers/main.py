from odoo import http
from odoo.http import request
from odoo.addons.website_hr_recruitment.controllers.main import WebsiteHrRecruitment


class WebsiteHrRecruitmentExtended(WebsiteHrRecruitment):

    def _get_application_fields(self):
        fields = super()._get_application_fields()
        custom_fields = [
            'applicant_experience',
            'applicant_education',
            'applicant_certification_ids',
            'skill_ids',
            'date_obtained',           # ✅ NEW
            'expiration_date',
            'applicant_source',
            'applicant_medium',
        ]
        for f in custom_fields:
            if f not in fields:
                fields.append(f)
        return fields

    def _prepare_application_values(self, job, post):
        vals = super()._prepare_application_values(job, post)

        # Experience
        try:
            vals['applicant_experience'] = int(post.get('applicant_experience') or 0)
        except ValueError:
            vals['applicant_experience'] = 0
        post.pop('applicant_experience', None)  # remove to avoid "other info"

        # Education
        vals['applicant_education'] = post.get('applicant_education') or 'none'
        post.pop('applicant_education', None)

        # Certifications
        if post.get('certifications_text'):
            cert_names = [c.strip() for c in post['certifications_text'].split(',') if c.strip()]
            cert_model = request.env['hr.certification'].sudo()
            cert_ids = []
            for name in cert_names:
                cert = cert_model.search([('name', '=ilike', name)], limit=1)
                if not cert:
                    cert = cert_model.create({'name': name})
                cert_ids.append(cert.id)
            vals['applicant_certification_ids'] = [(6, 0, cert_ids)]
        post.pop('certifications_text', None)

        # Skills
        if post.get('skills_text'):
            skill_names = [s.strip() for s in post['skills_text'].split(',') if s.strip()]
            skill_model = request.env['hr.skill'].sudo()
            skill_ids = []
            for name in skill_names:
                skill = skill_model.search([('name', '=ilike', name)], limit=1)
                if not skill:
                    skill = skill_model.create({'name': name})
                skill_ids.append(skill.id)
            vals['skill_ids'] = [(6, 0, skill_ids)]
        post.pop('skills_text', None)

        if post.get('date_obtained'):
            vals['date_obtained'] = post['date_obtained']
        if post.get('expiration_date'):
            vals['expiration_date'] = post['expiration_date']


        if post.get('applicant_source'):
            vals['applicant_source'] = post['applicant_source']
        if post.get('applicant_medium'):
            vals['applicant_medium'] = post['applicant_medium']    

        return vals
