from odoo import models, fields, api, _
from odoo.exceptions import UserError
import mimetypes

class OnboardingUploadWizard(models.TransientModel):
    _name = 'onboarding.upload.wizard'
    _description = 'Upload Multiple Onboarding Documents'

    employee_id = fields.Many2one('hr.employee', string="Employee", required=True, ondelete='cascade')

    cv_attachment = fields.Binary('CV', filename="cv_filename")
    cv_filename = fields.Char('CV Filename')

    medical_attachment = fields.Binary('Medical Report', filename="medical_filename")
    medical_filename = fields.Char('Medical Report Filename')

    police_report_attachment = fields.Binary('Police Report', filename="police_report_filename")
    police_report_filename = fields.Char('Police Report Filename')

    credentials_attachment = fields.Binary('Credentials', filename="credentials_filename")
    credentials_filename = fields.Char('Credentials Filename')

    passport_photo_attachment = fields.Binary('Passport Photo', filename="passport_photo_filename")
    passport_photo_filename = fields.Char('Passport Photo Filename')

    bond_ack_attachment = fields.Binary('Bond Letter', filename="bond_ack_filename")
    bond_ack_filename = fields.Char('Bond Letter Filename')

    loe_ack_attachment = fields.Binary('LOE Acknowledgement', filename="loe_ack_filename")
    loe_ack_filename = fields.Char('LOE Acknowledgement Filename')

    employment_form_attachment = fields.Binary('Employment Form', filename="employment_form_filename")
    employment_form_filename = fields.Char('Employment Form Filename')

    background_attachment = fields.Binary('Background Document', filename="background_filename")
    background_filename = fields.Char('Background Document Filename')

    def action_upload(self):
        employee = self.employee_id
        field_map = {
            'cv': ('cv_attachment', 'cv_filename', 'onboarding_cv_attachment_ids'),
            'medical': ('medical_attachment', 'medical_filename', 'onboarding_medical_attachment_ids'),
            'police_report': ('police_report_attachment', 'police_report_filename', 'onboarding_police_report_attachment_ids'),
            'credentials': ('credentials_attachment', 'credentials_filename', 'onboarding_credentials_attachment_ids'),
            'passport_photo': ('passport_photo_attachment', 'passport_photo_filename', 'onboarding_passport_photo_attachment_ids'),
            'bond_ack': ('bond_ack_attachment', 'bond_ack_filename', 'onboarding_bond_ack_attachment_ids'),
            'loe_ack': ('loe_ack_attachment', 'loe_ack_filename', 'onboarding_loe_ack_attachment_ids'),
            'employment_form': ('employment_form_attachment', 'employment_form_filename', 'onboarding_employment_form_attachment_ids'),
            'background': ('background_attachment', 'background_filename', 'onboarding_background_check_attachment_ids'),
        }

        uploaded_docs = []
        for doc_key, (bin_field, name_field, employee_field) in field_map.items():
            bin_data = self[bin_field]
            filename = self[name_field]
            if bin_data:
                mimetype = mimetypes.guess_type(filename or '')[0] or 'application/octet-stream'
                attachment = self.env['ir.attachment'].create({
                    'name': filename or f'{doc_key}.upload',
                    'datas': bin_data,
                    'res_model': 'hr.employee',
                    'res_id': employee.id,
                    'type': 'binary',
                    'mimetype': mimetype,
                })
                employee.write({
                    employee_field: [(4, attachment.id)]
                })
                uploaded_docs.append(filename or doc_key)

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Upload Successful'),
                'message': _('Documents uploaded: %s' % ', '.join(uploaded_docs)),
                'type': 'success',
                'next': {'type': 'ir.actions.act_window_close'}
            }
        }
    @api.model
    def default_get(self, fields):
        res = super(OnboardingUploadWizard, self).default_get(fields)
        employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        if employee:
            res['employee_id'] = employee.id
        return res
