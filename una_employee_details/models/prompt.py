from odoo import models, fields, api, _

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    onboarding_documents_missing = fields.Boolean(
        string='Missing Onboarding Documents',
        compute='_compute_onboarding_documents_missing',
        store=True
    )

    missing_onboarding_docs = fields.Text(
        compute='_compute_missing_onboarding_docs',
        store=False
    )

    @api.depends(
        'onboarding_cv_attachment_ids',
        'onboarding_loe_ack_attachment_ids',
        'onboarding_bond_ack_attachment_ids',
        'onboarding_background_check_attachment_ids',
        'onboarding_police_report_attachment_ids',
        'onboarding_medical_attachment_ids',
        'onboarding_employment_form_attachment_ids',
        'onboarding_passport_photo_attachment_ids',
        'onboarding_credentials_attachment_ids',
        'onboarding_documented_attachment_ids',
        'onboarding_id_card_attachment_ids',
        'onboarding_licenses_attachment_ids',
    )
    def _compute_onboarding_documents_missing(self):
        for employee in self:
            required_fields = [
                employee.onboarding_cv_attachment_ids,
                employee.onboarding_loe_ack_attachment_ids,
                employee.onboarding_bond_ack_attachment_ids,
                employee.onboarding_background_check_attachment_ids,
                employee.onboarding_police_report_attachment_ids,
                employee.onboarding_medical_attachment_ids,
                employee.onboarding_employment_form_attachment_ids,
                employee.onboarding_passport_photo_attachment_ids,
                employee.onboarding_credentials_attachment_ids,
                employee.onboarding_documented_attachment_ids,
                employee.onboarding_id_card_attachment_ids,
                employee.onboarding_licenses_attachment_ids,
            ]
            employee.onboarding_documents_missing = any(not field for field in required_fields)

    def _compute_missing_onboarding_docs(self):
        for employee in self:
            missing = []
            if not employee.onboarding_cv_attachment_ids:
                missing.append("CV")
            if not employee.onboarding_loe_ack_attachment_ids:
                missing.append("LOE Acknowledgement")
            if not employee.onboarding_bond_ack_attachment_ids:
                missing.append("Bond Acknowledgement")
            if not employee.onboarding_background_check_attachment_ids:
                missing.append("Background Check")
            if not employee.onboarding_police_report_attachment_ids:
                missing.append("Police Report")
            if not employee.onboarding_medical_attachment_ids:
                missing.append("Medical Report")
            if not employee.onboarding_employment_form_attachment_ids:
                missing.append("Employment Form")
            if not employee.onboarding_passport_photo_attachment_ids:
                missing.append("Passport Photo")
            if not employee.onboarding_credentials_attachment_ids:
                missing.append("Credentials")
            if not employee.onboarding_documented_attachment_ids:
                missing.append("Documented Letters")
            if not employee.onboarding_id_card_attachment_ids:
                missing.append("ID Card")
            if not employee.onboarding_licenses_attachment_ids:
                missing.append("Licenses")
            employee.missing_onboarding_docs = ', '.join(missing)

    def action_schedule_onboarding_reminders(self):
        employees_to_remind = self.search([('onboarding_documents_missing', '=', True)])
        model_id = self.env['ir.model']._get_id('hr.employee')
        template = self.env.ref('una_employee_details.mail_template_onboarding_reminder', raise_if_not_found=False)

        for employee in employees_to_remind:
            user = employee.user_id
            if user:
                existing_activity = self.env['mail.activity'].search([
                    ('res_model_id', '=', model_id),
                    ('res_id', '=', employee.id),
                    ('activity_type_id', '=', self.env.ref('mail.mail_activity_data_todo').id),
                    ('user_id', '=', user.id),
                    ('summary', '=', 'Complete Onboarding Documents'),
                ], limit=1)

                if not existing_activity:
                    self.env['mail.activity'].create({
                        'res_model_id': model_id,
                        'res_id': employee.id,
                        'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                        'summary': 'Complete Onboarding Documents',
                        'note': 'Please upload all required onboarding documents.',
                        'user_id': user.id,
                    })

                if template:
                    template.send_mail(employee.id, force_send=True)
