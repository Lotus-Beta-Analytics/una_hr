# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import date

import logging
_logger = logging.getLogger(__name__)

class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    # _name = 'hr.employee'  # Explicitly keep the same model name

    # Each item below is a boolean field + a remarks field
    onboarding_loe_ack = fields.Boolean(string="ACKNOWLEDGED COPY OF LOE RECEIVED/EXECUTED")
    onboarding_loe_ack_remarks = fields.Char(string="Remarks")

    onboarding_bond_ack = fields.Boolean(string="THE BOND LETTER ACKNOWLEDGED RECEIVED/EXECUTED AND NOTARIZED", tracking=True)
    onboarding_bond_ack_remarks = fields.Char(string="Remarks", tracking=True)

    onboarding_background_check = fields.Boolean(string="BACKGROUND FORM COMPLETED/ RETURNED/ AND VERIFICATION CHECKED", tracking=True)
    onboarding_background_check_remarks = fields.Char(string="Remarks", tracking=True)

    onboarding_police_report = fields.Boolean(string="POLICE REPORT COMPLETED FROM SECURITY DEPT", tracking=True)
    onboarding_police_report_remarks = fields.Char(string="Remarks", tracking=True)

    onboarding_medical = fields.Boolean(string="MEDICAL REPORT COMPLETED", tracking=True)
    onboarding_medical_remarks = fields.Char(string="Remarks", tracking=True)

    onboarding_employment_form = fields.Boolean(string="ONBOARDING EMPLOYMENT FORM EXECUTED", tracking=True)
    onboarding_employment_form_remarks = fields.Char(string="Remarks", tracking=True)

    onboarding_passport_photo = fields.Boolean(string="PASSPORT PHOTOGRAPHS RECEIVED", tracking=True)
    onboarding_passport_photo_remarks = fields.Char(string="Remarks", tracking=True)

    onboarding_credentials = fields.Boolean(string="COPIES OF CREDENTIALS RECEIVED", tracking=True)
    onboarding_credentials_remarks = fields.Char(string="Remarks", tracking=True)

    onboarding_documented = fields.Boolean(string="INFORMATION DOCUMENTED IN THE HUMAN MANAGER PORTAL", tracking=True)
    onboarding_documented_remarks = fields.Char(string="Remarks", tracking=True)

    onboarding_id_card = fields.Selection(
    [('yes', 'Yes'), ('no', 'No')],
    string="ID CARD PRODUCED",
    tracking=True
)
    onboarding_id_card_remarks = fields.Char(string="Remarks", tracking=True)

    onboarding_uniforms = fields.Selection(
    [('yes', 'Yes'), ('no', 'No')],
    string="UNIFORMS ISSUED",
    tracking=True
)
    onboarding_uniforms_remarks = fields.Char(string="Remarks", tracking=True)

    onboarding_referees = fields.Boolean(string="REFEREES /GUARANTOR FORM FILLED/ COLLECTED", tracking=True)
    onboarding_referees_remarks = fields.Char(string="Remarks", tracking=True)

    onboarding_licenses = fields.Boolean(string="LICENSES COLLECTD AND DOCUMENT APPLICABLE FOR PILOTS/ CABIN CREW, FLIGHT DISPATCHERS, ENGINEERS / PLANNING", tracking=True)
    onboarding_licenses_remarks = fields.Char(string="Remarks", tracking=True)

    onboarding_cv = fields.Boolean(string="CV AND CREDENTIALS RECEIVED AND DOCUMENTED", tracking=True)
    onboarding_cv_remarks = fields.Char(string="Remarks", tracking=True)

    # onboarding_account = fields.Boolean(string="ACCOUNT DETAILS WITH TIN AND RSA SUPPLIED", tracking=True)
    onboarding_account = fields.Selection(
    [('yes', 'Yes'), ('no', 'No')],
    string="ACCOUNT DETAILS WITH TIN AND RSA SUPPLIED",
    tracking=True
)
    onboarding_account_remarks = fields.Char(string="Remarks", tracking=True)

    # onboarding_tools = fields.Boolean(string="WORKING TOOLS PROVIDED (computer, desk etc)", tracking=True)
    onboarding_tools = fields.Selection(
    [('yes', 'Yes'), ('no', 'No')],
    string="WORKING TOOLS PROVIDED (computer, desk etc)",
    tracking=True
) 
    onboarding_tools_remarks = fields.Char(string="Remarks", tracking=True)

    # onboarding_handbook = fields.Boolean(string="HANDBOOK ACKNOWLEDGMENT COPY", tracking=True)
    onboarding_handbook = fields.Selection(
    [('yes', 'Yes'), ('no', 'No')],
    string="HANDBOOK ACKNOWLEDGMENT COPY",
    tracking=True
)
    onboarding_handbook_remarks = fields.Char(string="Remarks", tracking=True)

    # onboarding_email = fields.Boolean(string="EMAIL CREATION BY IT DEPARTMENT FROM HR", tracking=True)
    onboarding_email = fields.Selection(
    [('yes', 'Yes'), ('no', 'No')],
    string="EMAIL CREATION BY IT DEPARTMENT FROM HR",
    tracking=True
)

    onboarding_email_remarks = fields.Char(string="Remarks", tracking=True)

    copies_recieved_from = fields.Many2one('res.users', string="COPIES RECEIVED FROM: ", tracking=True)
    station_office = fields.Many2one('res.users',string="STATION/OFFICE: ", tracking=True)
    it_dept = fields.Many2one('res.users',string="IT DEPT: ", tracking=True)
    admin_dept = fields.Many2one('res.users',string="ADMIN DEPT: ", tracking=True)
    processed_by = fields.Many2one('res.users',string="PROCESSED BY: ", tracking=True)
    checked_by = fields.Many2one('res.users',string="CHECKED BY: ", tracking=True)
    hrm_head = fields.Many2one('res.users',string="HEAD HRM: ", tracking=True)

    onboarding_background_check_attachment_ids = fields.Many2many(
    'ir.attachment',
    'employee_background_check_attachment_rel',
    'employee_id',
    'attachment_id',
    string="Background Check Attachments"
)

    onboarding_background_check_status_html = fields.Html(
        compute='_compute_onboarding_background_check_status_html',
        sanitize=True
    )

    @api.depends('onboarding_background_check_attachment_ids')
    def _compute_onboarding_background_check_status_html(self):
        for rec in self:
            if rec.onboarding_background_check_attachment_ids:
                rec.onboarding_background_check_status_html = """
                <div style="margin-top: 8px; padding: 10px; background-color: #d4edda;
                    color: #155724; border: 1px solid #c3e6cb; border-radius: 5px;
                    display: flex; align-items: center; gap: 10px;">
                    <i class="fa fa-check-circle" style="color: #28a745; font-size: 18px;"></i>
                    <span>File(s) uploaded successfully.</span>
                </div>
                """
            else:
                rec.onboarding_background_check_status_html = """
                <div style="margin-top: 8px; padding: 10px; background-color: #fff3cd;
                    color: #856404; border: 1px solid #ffeeba; border-radius: 5px;
                    display: flex; align-items: center; gap: 10px;">
                    <i class="fa fa-info-circle" style="color: #856404; font-size: 18px;"></i>
                    <span>No file uploaded yet.</span>
                </div>
                """


    # Add these fields to your HrEmployee model

    onboarding_bond_ack_attachment_ids = fields.Many2many(
        'ir.attachment',
        'employee_bond_ack_attachment_rel',
        'employee_id',
        'attachment_id',
        string="Bond Letter Attachments"
    )

    onboarding_bond_ack_status_html = fields.Html(
        compute='_compute_onboarding_bond_ack_status_html',
        sanitize=True
    )

    @api.depends('onboarding_bond_ack_attachment_ids')
    def _compute_onboarding_bond_ack_status_html(self):
        for rec in self:
            if rec.onboarding_bond_ack_attachment_ids:
                rec.onboarding_bond_ack_status_html = """
                <div style="margin-top: 8px; padding: 10px; background-color: #d4edda;
                    color: #155724; border: 1px solid #c3e6cb; border-radius: 5px;
                    display: flex; align-items: center; gap: 10px;">
                    <i class="fa fa-check-circle" style="color: #28a745; font-size: 18px;"></i>
                    <span>File(s) uploaded successfully.</span>
                </div>
                """
            else:
                rec.onboarding_bond_ack_status_html = """
                <div style="margin-top: 8px; padding: 10px; background-color: #fff3cd;
                    color: #856404; border: 1px solid #ffeeba; border-radius: 5px;
                    display: flex; align-items: center; gap: 10px;">
                    <i class="fa fa-info-circle" style="color: #856404; font-size: 18px;"></i>
                    <span>No file uploaded yet.</span>
                </div>
                """

    onboarding_police_report_attachment_ids = fields.Many2many(
        'ir.attachment',
        'employee_police_report_attachment_rel',
        'employee_id',
        'attachment_id',
        string="POLICE REPORT COMPLETED FROM SECURITY DEPT"
    )

    onboarding_police_report_status_html = fields.Html(
        compute='_compute_onboarding_police_report_status_html',
        sanitize=True
    )

    last_onboarding_reminder_date = fields.Date(
        string='Last Onboarding Reminder Date',
        help='Date when the last onboarding reminder email was sent to the employee.'
    )

    # updated codes stay here:

    def _get_pending_documents(self):
        """Compute the list of pending onboarding documents."""
        document_fields = {
            'CV': ('onboarding_cv', 'onboarding_cv_attachment_ids'),
            'Letter of Employment Acknowledgement': ('onboarding_loe_ack', 'onboarding_loe_ack_attachment_ids'),
            'Bond Acknowledgement': ('onboarding_bond_ack', 'onboarding_bond_ack_attachment_ids'),
            'Background Check': ('onboarding_background_check', 'onboarding_background_check_attachment_ids'),
            'Police Report': ('onboarding_police_report', 'onboarding_police_report_attachment_ids'),
            'Medical Report': ('onboarding_medical', 'onboarding_medical_attachment_ids'),
            'Employment Form': ('onboarding_employment_form', 'onboarding_employment_form_attachment_ids'),
            'Passport Photo': ('onboarding_passport_photo', 'onboarding_passport_photo_attachment_ids'),
            'Credentials': ('onboarding_credentials', 'onboarding_credentials_attachment_ids'),
            # 'ID Card': ('onboarding_id_card', 'onboarding_id_card_attachment_ids'),
            'Licenses': ('onboarding_licenses', 'onboarding_licenses_attachment_ids'),
        }
        pending_documents = []
        for doc_name, (boolean_field, attachment_field) in document_fields.items():
            # Consider a document pending if the boolean is False or no attachments are uploaded
            if not self[boolean_field] or not self[attachment_field]:
                pending_documents.append(doc_name)
        return pending_documents
    


    def send_onboarding_reminder_email(self):
        """Send reminder email for pending onboarding documents."""
        template = self.env.ref('una_employee_details.onboarding_reminder_email_template')
        for employee in self:
            if not employee.work_email:
                _logger.warning(f"No work email defined for employee {employee.name}")
                continue
#stopping multiple emails
            if employee.last_onboarding_reminder_date == date.today():
                _logger.info(f"Reminder already sent today to {employee.name}, skipping.")
                continue

            pending_documents = employee._get_pending_documents()
            pending_count = len(pending_documents)
            if pending_count > 0:
                try:
                    template.with_context(
                        pending_documents=pending_documents,
                        pending_count=pending_count
                    ).send_mail(employee.id, force_send=True, raise_exception=True)
                   
                    # employee.last_onboarding_reminder_date = date.today()
                    
                except Exception as e:
                    _logger.error(f"Failed to send onboarding reminder email to {employee.name}: {str(e)}")
            else:
                _logger.info(f"No pending documents for {employee.name}, skipping email.")


    @api.model
    def cron_send_onboarding_reminders(self):
        _logger.info("CRON: Running onboarding reminder check")
        today = date.today()
        employees = self.search([
            ('active', '=', True),
            ('work_email', '!=', False),
            '|',
            ('last_onboarding_reminder_date', '=', False),
            ('last_onboarding_reminder_date', '!=', today),
        ])
        _logger.info(f"Found {len(employees)} employees to process.")
        employees.send_onboarding_reminder_email()             

    # @api.model
    # def cron_send_onboarding_reminders(self):
    #     """Cron job to send onboarding reminder emails to employees with pending documents."""
    #     employees = self.search([('active', '=', True), ('work_email', '!=', False)])
    #     employees.send_onboarding_reminder_email()


    @api.depends('onboarding_police_report_attachment_ids')
    def _compute_onboarding_police_report_status_html(self):
        for rec in self:
            if rec.onboarding_police_report_attachment_ids:
                rec.onboarding_police_report_status_html = """
                <div style="margin-top: 8px; padding: 10px; background-color: #d4edda;
                    color: #155724; border: 1px solid #c3e6cb; border-radius: 5px;
                    display: flex; align-items: center; gap: 10px;">
                    <i class="fa fa-check-circle" style="color: #28a745; font-size: 18px;"></i>
                    <span>File(s) uploaded successfully.</span>
                </div>
                """
            else:
                rec.onboarding_police_report_status_html = """
                <div style="margin-top: 8px; padding: 10px; background-color: #fff3cd;
                    color: #856404; border: 1px solid #ffeeba; border-radius: 5px;
                    display: flex; align-items: center; gap: 10px;">
                    <i class="fa fa-info-circle" style="color: #856404; font-size: 18px;"></i>
                    <span>No file uploaded yet.</span>
                </div>
                """
    onboarding_medical_attachment_ids = fields.Many2many(
        'ir.attachment',
        'employee_medical_attachment_rel',
        'employee_id',
        'attachment_id',
        string="Medical Report Attachments"
    )

    onboarding_medical_status_html = fields.Html(
        compute='_compute_onboarding_medical_status_html',
        sanitize=True
    )

    @api.depends('onboarding_medical_attachment_ids')
    def _compute_onboarding_medical_status_html(self):
        for rec in self:
            if rec.onboarding_medical_attachment_ids:
                rec.onboarding_medical_status_html = """
                <div style="margin-top: 8px; padding: 10px; background-color: #d4edda;
                    color: #155724; border: 1px solid #c3e6cb; border-radius: 5px;
                    display: flex; align-items: center; gap: 10px;">
                    <i class="fa fa-check-circle" style="color: #28a745; font-size: 18px;"></i>
                    <span>File(s) uploaded successfully.</span>
                </div>
                """
            else:
                rec.onboarding_medical_status_html = """
                <div style="margin-top: 8px; padding: 10px; background-color: #fff3cd;
                    color: #856404; border: 1px solid #ffeeba; border-radius: 5px;
                    display: flex; align-items: center; gap: 10px;">
                    <i class="fa fa-info-circle" style="color: #856404; font-size: 18px;"></i>
                    <span>No file uploaded yet.</span>
                </div>
                """

    onboarding_employment_form_attachment_ids = fields.Many2many(
        'ir.attachment',
        'employee_employment_form_attachment_rel',
        'employee_id',
        'attachment_id',
        string="Employment Form Attachments"
    )

    onboarding_employment_form_status_html = fields.Html(
        compute='_compute_onboarding_employment_form_status_html',
        sanitize=True
    )

    @api.depends('onboarding_employment_form_attachment_ids')
    def _compute_onboarding_employment_form_status_html(self):
        for rec in self:
            if rec.onboarding_employment_form_attachment_ids:
                rec.onboarding_employment_form_status_html = """
                <div style="margin-top: 8px; padding: 10px; background-color: #d4edda;
                    color: #155724; border: 1px solid #c3e6cb; border-radius: 5px;
                    display: flex; align-items: center; gap: 10px;">
                    <i class="fa fa-check-circle" style="color: #28a745; font-size: 18px;"></i>
                    <span>File(s) uploaded successfully.</span>
                </div>
                """
            else:
                rec.onboarding_employment_form_status_html = """
                <div style="margin-top: 8px; padding: 10px; background-color: #fff3cd;
                    color: #856404; border: 1px solid #ffeeba; border-radius: 5px;
                    display: flex; align-items: center; gap: 10px;">
                    <i class="fa fa-info-circle" style="color: #856404; font-size: 18px;"></i>
                    <span>No file uploaded yet.</span>
                </div>
                """
    onboarding_passport_photo_attachment_ids = fields.Many2many(
        'ir.attachment',
        'employee_passport_photo_attachment_rel',
        'employee_id',
        'attachment_id',
        string="Passport Photo Attachments"
    )

    onboarding_passport_photo_status_html = fields.Html(
        compute='_compute_onboarding_passport_photo_status_html',
        sanitize=True
    )

    @api.depends('onboarding_passport_photo_attachment_ids')
    def _compute_onboarding_passport_photo_status_html(self):
        for rec in self:
            if rec.onboarding_passport_photo_attachment_ids:
                rec.onboarding_passport_photo_status_html = """
                <div style="margin-top: 8px; padding: 10px; background-color: #d4edda;
                    color: #155724; border: 1px solid #c3e6cb; border-radius: 5px;
                    display: flex; align-items: center; gap: 10px;">
                    <i class="fa fa-check-circle" style="color: #28a745; font-size: 18px;"></i>
                    <span>File(s) uploaded successfully.</span>
                </div>
                """
            else:
                rec.onboarding_passport_photo_status_html = """
                <div style="margin-top: 8px; padding: 10px; background-color: #fff3cd;
                    color: #856404; border: 1px solid #ffeeba; border-radius: 5px;
                    display: flex; align-items: center; gap: 10px;">
                    <i class="fa fa-info-circle" style="color: #856404; font-size: 18px;"></i>
                    <span>No file uploaded yet.</span>
                </div>
                """

    onboarding_credentials_attachment_ids = fields.Many2many(
        'ir.attachment',
        'employee_credentials_attachment_rel',
        'employee_id',
        'attachment_id',
        string="Credentials Attachments"
    )

    onboarding_credentials_status_html = fields.Html(
        compute='_compute_onboarding_credentials_status_html',
        sanitize=True
    )

    @api.depends('onboarding_credentials_attachment_ids')
    def _compute_onboarding_credentials_status_html(self):
        for rec in self:
            if rec.onboarding_credentials_attachment_ids:
                rec.onboarding_credentials_status_html = """
                <div style="margin-top: 8px; padding: 10px; background-color: #d4edda;
                    color: #155724; border: 1px solid #c3e6cb; border-radius: 5px;
                    display: flex; align-items: center; gap: 10px;">
                    <i class="fa fa-check-circle" style="color: #28a745; font-size: 18px;"></i>
                    <span>File(s) uploaded successfully.</span>
                </div>
                """
            else:
                rec.onboarding_credentials_status_html = """
                <div style="margin-top: 8px; padding: 10px; background-color: #fff3cd;
                    color: #856404; border: 1px solid #ffeeba; border-radius: 5px;
                    display: flex; align-items: center; gap: 10px;">
                    <i class="fa fa-info-circle" style="color: #856404; font-size: 18px;"></i>
                    <span>No file uploaded yet.</span>
                </div>
                """
    onboarding_documented_attachment_ids = fields.Many2many(
        'ir.attachment',
        'employee_documented_attachment_rel',
        'employee_id',
        'attachment_id',
        string="Documented Information Attachments"
    )

    onboarding_documented_status_html = fields.Html(
        compute='_compute_onboarding_documented_status_html',
        sanitize=True
    )

    @api.depends('onboarding_documented_attachment_ids')
    def _compute_onboarding_documented_status_html(self):
        for rec in self:
            if rec.onboarding_documented_attachment_ids:
                rec.onboarding_documented_status_html = """
                <div style="margin-top: 8px; padding: 10px; background-color: #d4edda;
                    color: #155724; border: 1px solid #c3e6cb; border-radius: 5px;
                    display: flex; align-items: center; gap: 10px;">
                    <i class="fa fa-check-circle" style="color: #28a745; font-size: 18px;"></i>
                    <span>File(s) uploaded successfully.</span>
                </div>
                """
            else:
                rec.onboarding_documented_status_html = """
                <div style="margin-top: 8px; padding: 10px; background-color: #fff3cd;
                    color: #856404; border: 1px solid #ffeeba; border-radius: 5px;
                    display: flex; align-items: center; gap: 10px;">
                    <i class="fa fa-info-circle" style="color: #856404; font-size: 18px;"></i>
                    <span>No file uploaded yet.</span>
                </div>
                """
                
    onboarding_licenses_attachment_ids = fields.Many2many(
        'ir.attachment',
        'employee_licenses_attachment_rel',
        'employee_id',
        'attachment_id',
        string="License Attachments"
    )

    onboarding_licenses_status_html = fields.Html(
        compute='_compute_onboarding_licenses_status_html',
        sanitize=True
    )

    @api.depends('onboarding_licenses_attachment_ids')
    def _compute_onboarding_licenses_status_html(self):
        for rec in self:
            if rec.onboarding_licenses_attachment_ids:
                rec.onboarding_licenses_status_html = """
                <div style="margin-top: 8px; padding: 10px; background-color: #d4edda;
                    color: #155724; border: 1px solid #c3e6cb; border-radius: 5px;
                    display: flex; align-items: center; gap: 10px;">
                    <i class="fa fa-check-circle" style="color: #28a745; font-size: 18px;"></i>
                    <span>File(s) uploaded successfully.</span>
                </div>
                """
            else:
                rec.onboarding_licenses_status_html = """
                <div style="margin-top: 8px; padding: 10px; background-color: #fff3cd;
                    color: #856404; border: 1px solid #ffeeba; border-radius: 5px;
                    display: flex; align-items: center; gap: 10px;">
                    <i class="fa fa-info-circle" style="color: #856404; font-size: 18px;"></i>
                    <span>No file uploaded yet.</span>
                </div>
                """
    onboarding_cv_attachment_ids = fields.Many2many(
        'ir.attachment',
        'employee_cv_attachment_rel',
        'employee_id',
        'attachment_id',
        string="CV Attachments"
    )

    onboarding_cv_status_html = fields.Html(
        compute='_compute_onboarding_cv_status_html',
        sanitize=True
    )

    @api.depends('onboarding_cv_attachment_ids')
    def _compute_onboarding_cv_status_html(self):
        for rec in self:
            if rec.onboarding_cv_attachment_ids:
                rec.onboarding_cv_status_html = """
                <div style="margin-top: 8px; padding: 10px; background-color: #d4edda;
                    color: #155724; border: 1px solid #c3e6cb; border-radius: 5px;
                    display: flex; align-items: center; gap: 10px;">
                    <i class="fa fa-check-circle" style="color: #28a745; font-size: 18px;"></i>
                    <span>File(s) uploaded successfully.</span>
                </div>
                """
            else:
                rec.onboarding_cv_status_html = """
                <div style="margin-top: 8px; padding: 10px; background-color: #fff3cd;
                    color: #856404; border: 1px solid #ffeeba; border-radius: 5px;
                    display: flex; align-items: center; gap: 10px;">
                    <i class="fa fa-info-circle" style="color: #856404; font-size: 18px;"></i>
                    <span>No file uploaded yet.</span>
                </div>
                """


    onboarding_id_card_attachment_ids = fields.Many2many(
        'ir.attachment',
        'employee_onboarding_attachment_rel',
        'employee_id',
        'attachment_id',
        string="Onboarding ID Card Attachments"
    )
            



    # Attachment field for LOE Acknowledgement
    onboarding_loe_ack_attachment_ids = fields.Many2many(
        'ir.attachment',
        'employee_loe_ack_attachment_rel',
        'employee_id',
        'attachment_id',
        string="LOE Acknowledgement Attachments"
    )

    # Computed status HTML
    onboarding_loe_ack_status_html = fields.Html(
        compute='_compute_onboarding_loe_ack_status_html',
        sanitize=True
    )

    @api.depends('onboarding_loe_ack_attachment_ids')
    def _compute_onboarding_loe_ack_status_html(self):
        for rec in self:
            if rec.onboarding_loe_ack_attachment_ids:
                rec.onboarding_loe_ack_status_html = """
                <div style="margin-top: 8px; padding: 10px; background-color: #d4edda;
                    color: #155724; border: 1px solid #c3e6cb; border-radius: 5px;
                    display: flex; align-items: center; gap: 10px;">
                    <i class="fa fa-check-circle" style="color: #28a745; font-size: 18px;"></i>
                    <span>File(s) uploaded successfully.</span>
                </div>
                """
            else:
                rec.onboarding_loe_ack_status_html = """
                <div style="margin-top: 8px; padding: 10px; background-color: #fff3cd;
                    color: #856404; border: 1px solid #ffeeba; border-radius: 5px;
                    display: flex; align-items: center; gap: 10px;">
                    <i class="fa fa-info-circle" style="color: #856404; font-size: 18px;"></i>
                    <span>No file uploaded yet.</span>
                </div>
                """


class OnboardingReminder(models.Model):
    _name = 'onboarding.reminder'
    _description = 'Onboarding Document Reminder Tracker'

    employee_id = fields.Many2one('hr.employee', string="Employee", required=True, ondelete='cascade')
    document_type = fields.Selection([
        ('loe_ack', 'LOE Acknowledgement'),
        ('bond_ack', 'Bond Letter'),
        ('background_check', 'Background Check'),
        ('police_report', 'Police Report'),
        ('medical', 'Medical Report'),
        ('employment_form', 'Employment Form'),
        ('passport_photo', 'Passport Photo'),
        ('credentials', 'Credentials'),
        ('documented', 'Documented Information'),
        ('id_card', 'ID Card'),
        ('licenses', 'Licenses'),
        ('cv', 'CV'),
    ], string="Document Type", required=True)
    last_reminder_date = fields.Date(string="Last Reminder Sent")
    reminder_count = fields.Integer(string="Reminders Sent", default=0)
    is_completed = fields.Boolean(string="Completed", default=False)

    _sql_constraints = [
        ('unique_employee_document', 'unique(employee_id, document_type)',
         'Only one reminder record per document type per employee is allowed.')
    ]
