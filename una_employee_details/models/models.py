# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

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

    onboarding_id_card = fields.Boolean(string="ID CARD PRODUCED", tracking=True)
    onboarding_id_card_remarks = fields.Char(string="Remarks", tracking=True)

    onboarding_uniforms = fields.Boolean(string="UNIFORMS ISSUED", tracking=True)
    onboarding_uniforms_remarks = fields.Char(string="Remarks", tracking=True)

    onboarding_referees = fields.Boolean(string="REFEREES /GUARANTOR FORM FILLED/ COLLECTED", tracking=True)
    onboarding_referees_remarks = fields.Char(string="Remarks", tracking=True)

    onboarding_licenses = fields.Boolean(string="LICENSES COLLECTD AND DOCUMENT APPLICABLE FOR PILOTS/ CABIN CREW, FLIGHT DISPATCHERS, ENGINEERS / PLANNING", tracking=True)
    onboarding_licenses_remarks = fields.Char(string="Remarks", tracking=True)

    onboarding_cv = fields.Boolean(string="CV AND CREDENTIALS RECEIVED AND DOCUMENTED", tracking=True)
    onboarding_cv_remarks = fields.Char(string="Remarks", tracking=True)

    onboarding_account = fields.Boolean(string="ACCOUNT DETAILS WITH TIN AND RSA SUPPLIED", tracking=True)
    onboarding_account_remarks = fields.Char(string="Remarks", tracking=True)

    onboarding_tools = fields.Boolean(string="WORKING TOOLS PROVIDED (computer, desk etc)", tracking=True)
    onboarding_tools_remarks = fields.Char(string="Remarks", tracking=True)

    onboarding_handbook = fields.Boolean(string="HANDBOOK ACKNOWLEDGMENT COPY", tracking=True)
    onboarding_handbook_remarks = fields.Char(string="Remarks", tracking=True)

    onboarding_email = fields.Boolean(string="EMAIL CREATION BY IT DEPARTMENT FROM HR", tracking=True)
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
        string="Police Report Attachments"
    )

    onboarding_police_report_status_html = fields.Html(
        compute='_compute_onboarding_police_report_status_html',
        sanitize=True
    )

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

    onboarding_id_card_attachment_ids = fields.Many2many(
        'ir.attachment',
        'employee_id_card_attachment_rel',
        'employee_id',
        'attachment_id',
        string="ID Card Attachments"
    )

    onboarding_id_card_status_html = fields.Html(
        compute='_compute_onboarding_id_card_status_html',
        sanitize=True
    )

    @api.depends('onboarding_id_card_attachment_ids')
    def _compute_onboarding_id_card_status_html(self):
        for rec in self:
            if rec.onboarding_id_card_attachment_ids:
                rec.onboarding_id_card_status_html = """
                <div style="margin-top: 8px; padding: 10px; background-color: #d4edda;
                    color: #155724; border: 1px solid #c3e6cb; border-radius: 5px;
                    display: flex; align-items: center; gap: 10px;">
                    <i class="fa fa-check-circle" style="color: #28a745; font-size: 18px;"></i>
                    <span>File(s) uploaded successfully.</span>
                </div>
                """
            else:
                rec.onboarding_id_card_status_html = """
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
