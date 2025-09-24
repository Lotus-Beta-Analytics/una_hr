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

    # WACE
    wace_attachment = fields.Boolean('WAEC/NECO Certificate')
    wace_filename = fields.Char('WAEC')

    # NECO
    neco_attachment = fields.Boolean('NECO Certificate')
    neco_filename = fields.Char('NECO Filename')

    # BSc
    bsc_attachment = fields.Boolean('B.Sc. Certificate')
    bsc_filename = fields.Char('BSc Filename')

    # MSc
    msc_attachment = fields.Boolean('Master’s Certificate')
    msc_filename = fields.Char('Master’s Filename')

    # PhD
    phd_attachment = fields.Boolean('PhD Certificate')
    phd_filename = fields.Char('PhD Filename')


    onboarding_documented = fields.Boolean(string="ACKNOWLEDGED CYBERSECURITY POLICY", tracking=True)
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
    onboarding_account= fields.Selection(
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


    onboarding_referees_attachment_ids = fields.Many2many(
        'ir.attachment',
        'employee_referees_attachment_rel',
        'employee_id',
        'attachment_id',
        string="Referees / Guarantor Form Attachments"
    )


    onboarding_referees_status_html = fields.Html(
        compute='_compute_onboarding_referees_status_html',
        sanitize=True
    )

    # ✅ Compute method
    @api.depends('onboarding_referees_attachment_ids')
    def _compute_onboarding_referees_status_html(self):
        for rec in self:
            if rec.onboarding_referees_attachment_ids:
                rec.onboarding_referees_status_html = """
                <div style="margin-top: 8px; padding: 10px; background-color: #d4edda;
                    color: #155724; border: 1px solid #c3e6cb; border-radius: 5px;
                    display: flex; align-items: center; justify-content: space-between;">
                    
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <i class="fa fa-check-circle" style="color: #28a745; font-size: 18px;"></i>
                        <span>Referees file(s) uploaded successfully.</span>
                    </div>

                    <span style="background-color: #28a745; color: white; padding: 4px 12px;
                        border-radius: 12px; font-weight: bold;">Done</span>
                </div>
                """
            else:
                rec.onboarding_referees_status_html = """
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
        string="Licenses Attachments"
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
                    <span>Licenses file(s) uploaded successfully.</span>
                </div>
                """
            else:
                rec.onboarding_licenses_status_html = """
                <div style="margin-top: 8px; padding: 10px; background-color: #fff3cd;
                    color: #856404; border: 1px solid #ffeeba; border-radius: 5px;
                    display: flex; align-items: center; gap: 10px;">
                    <i class="fa fa-info-circle" style="color: #856404; font-size: 18px;"></i>
                    <span>No license document uploaded yet.</span>
                </div>
                """
        # WACE
    onboarding_wace_attachment_ids = fields.Many2many(
        'ir.attachment',
        'employee_wace_attachment_rel',
        'employee_id',
        'attachment_id',
        string="WACE Attachments"
    )
    onboarding_wace_status_html = fields.Html(compute='_compute_credentials_status_html', sanitize=True)

    # NECO
    onboarding_neco_attachment_ids = fields.Many2many(
        'ir.attachment',
        'employee_neco_attachment_rel',
        'employee_id',
        'attachment_id',
        string="NECO Attachments"
    )
    onboarding_neco_status_html = fields.Html(compute='_compute_credentials_status_html', sanitize=True)

    # BSc
    onboarding_bsc_attachment_ids = fields.Many2many(
        'ir.attachment',
        'employee_bsc_attachment_rel',
        'employee_id',
        'attachment_id',
        string="BSc Attachments"
    )
    onboarding_bsc_status_html = fields.Html(compute='_compute_credentials_status_html', sanitize=True)

    # MSc
    onboarding_msc_attachment_ids = fields.Many2many(
        'ir.attachment',
        'employee_msc_attachment_rel',
        'employee_id',
        'attachment_id',
        string="MSc Attachments"
    )
    onboarding_msc_status_html = fields.Html(compute='_compute_credentials_status_html', sanitize=True)

    # PhD
    onboarding_phd_attachment_ids = fields.Many2many(
        'ir.attachment',
        'employee_phd_attachment_rel',
        'employee_id',
        'attachment_id',
        string="PhD Attachments"
    )
    onboarding_phd_status_html = fields.Html(compute='_compute_credentials_status_html', sanitize=True)

    @api.depends(
    'onboarding_wace_attachment_ids',
    'onboarding_neco_attachment_ids',
    'onboarding_bsc_attachment_ids',
    'onboarding_msc_attachment_ids',
    'onboarding_phd_attachment_ids'
    )
    def _compute_credentials_status_html(self):
        for rec in self:
            def get_status_html(files, label):
                if files:
                    return f"""
                    <div style="margin-top: 4px; padding: 8px; background-color: #d4edda;
                        color: #155724; border: 1px solid #c3e6cb; border-radius: 5px;
                        display: flex; align-items: center; gap: 8px;">
                        <i class="fa fa-check-circle" style="color: #28a745; font-size: 16px;"></i>
                        <span>{label} uploaded successfully.</span>
                    </div>
                    """
                else:
                    return f"""
                    <div style="margin-top: 4px; padding: 8px; background-color: #fff3cd;
                        color: #856404; border: 1px solid #ffeeba; border-radius: 5px;
                        display: flex; align-items: center; gap: 8px;">
                        <i class="fa fa-info-circle" style="color: #856404; font-size: 16px;"></i>
                        <span>{label} not uploaded yet.</span>
                    </div>
                    """

            rec.onboarding_wace_status_html = get_status_html(rec.onboarding_wace_attachment_ids, "WACE Certificate")
            rec.onboarding_neco_status_html = get_status_html(rec.onboarding_neco_attachment_ids, "NECO Certificate")
            rec.onboarding_bsc_status_html = get_status_html(rec.onboarding_bsc_attachment_ids, "BSc Certificate")
            rec.onboarding_msc_status_html = get_status_html(rec.onboarding_msc_attachment_ids, "Master’s Certificate")
            rec.onboarding_phd_status_html = get_status_html(rec.onboarding_phd_attachment_ids, "PhD Certificate")


    onboarding_documented_status_html = fields.Html(compute='_compute_onboarding_status_html', sanitize=True)
  

    onboarding_documented_attachment_ids = fields.Many2many(
        'ir.attachment',
        'employee_documented_attachment_rel',
        'employee_id',
        'attachment_id',
        string="Document Attachments")
   

    @api.depends(
    'onboarding_documented_attachment_ids',
   
    )
    def _compute_onboarding_status_html(self):
        for rec in self:
            def get_status_html(value, label):
                if value:
                    return f"""
                    <div style="margin-top: 4px; padding: 8px; background-color: #d4edda;
                        color: #155724; border: 1px solid #c3e6cb; border-radius: 5px;
                        display: flex; align-items: center; gap: 8px;">
                        <i class="fa fa-check-circle" style="color: #28a745; font-size: 16px;"></i>
                        <span>{label} completed successfully.</span>
                    </div>
                    """
                else:
                    return f"""
                    <div style="margin-top: 4px; padding: 8px; background-color: #fff3cd;
                        color: #856404; border: 1px solid #ffeeba; border-radius: 5px;
                        display: flex; align-items: center; gap: 8px;">
                        <i class="fa fa-info-circle" style="color: #856404; font-size: 16px;"></i>
                        <span>{label} not completed yet.</span>
                    </div>
                    """

            rec.onboarding_documented_status_html = get_status_html(rec.onboarding_documented_attachment_ids, "Information documented in Human Manager")
          
