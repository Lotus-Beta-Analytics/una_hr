# -*- coding: utf-8 -*-
from odoo import models, fields

class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    # _name = 'hr.employee'  # Explicitly keep the same model name

    # Each item below is a boolean field + a remarks field
    onboarding_loe_ack = fields.Boolean(string="ACKNOWLEDGED COPY OF LOE RECEIVED/EXECUTED", tracking=True)
    onboarding_loe_ack_remarks = fields.Char(string="Remarks", tracking=True)
    loe_onboarding_attachment = fields.Binary(string="Uploaded LOE Document", attachment=True)
    loe_onboarding_attachment_filename = fields.Char(string="File Name")

    onboarding_bond_ack = fields.Boolean(string="THE BOND LETTER ACKNOWLEDGED RECEIVED/EXECUTED AND NOTARIZED", tracking=True)
    onboarding_bond_ack_remarks = fields.Char(string="Remarks", tracking=True)
    ack_onboarding_attachment = fields.Binary(string="Uploaded ACK Document", attachment=True)
    ack_onboarding_attachment_filename = fields.Char(string="File Name")

    onboarding_background_check = fields.Boolean(string="BACKGROUND FORM COMPLETED/ RETURNED/ AND VERIFICATION CHECKED", tracking=True)
    onboarding_background_check_remarks = fields.Char(string="Remarks", tracking=True)
    background_onboarding_attachment = fields.Binary(string="Uploaded BACKGROUND CHECK Document", attachment=True)
    background_onboarding_attachment_filename = fields.Char(string="File Name")

    onboarding_police_report = fields.Boolean(string="POLICE REPORT COMPLETED FROM SECURITY DEPT", tracking=True)
    onboarding_police_report_remarks = fields.Char(string="Remarks", tracking=True)
    police_onboarding_attachment = fields.Binary(string="Uploaded POLICE REPORT", attachment=True)
    police_onboarding_attachment_filename = fields.Char(string="File Name")

    onboarding_medical = fields.Boolean(string="MEDICAL REPORT COMPLETED", tracking=True)
    onboarding_medical_remarks = fields.Char(string="Remarks", tracking=True)
    medical_onboarding_attachment = fields.Binary(string="Uploaded MEDICAL Document", attachment=True)
    medical_onboarding_attachment_filename = fields.Char(string="File Name")

    onboarding_employment_form = fields.Boolean(string="ONBOARDING EMPLOYMENT FORM EXECUTED", tracking=True)
    onboarding_employment_form_remarks = fields.Char(string="Remarks", tracking=True)
    employment_form_onboarding_attachment = fields.Binary(string="Uploaded EMPLOYMENT FORM", attachment=True)
    employment_form_onboarding_attachment_filename = fields.Char(string="File Name")

    onboarding_passport_photo = fields.Boolean(string="PASSPORT PHOTOGRAPHS RECEIVED", tracking=True)
    onboarding_passport_photo_remarks = fields.Char(string="Remarks", tracking=True)
    passport_onboarding_attachment = fields.Binary(string="Uploaded PASSPORT Document", attachment=True)
    passport_onboarding_attachment_filename = fields.Char(string="File Name")

    onboarding_credentials = fields.Boolean(string="COPIES OF CREDENTIALS RECEIVED", tracking=True)
    onboarding_credentials_remarks = fields.Char(string="Remarks", tracking=True)
    credentials_onboarding_attachment = fields.Binary(string="Uploaded CREDENTIALS", attachment=True)
    credentials_onboarding_attachment_filename = fields.Char(string="File Name")

    onboarding_documented = fields.Boolean(string="INFORMATION DOCUMENTED IN THE HUMAN MANAGER PORTAL", tracking=True)
    onboarding_documented_remarks = fields.Char(string="Remarks", tracking=True)
    document_onboarding_attachment = fields.Binary(string="Uploaded HR Document", attachment=True)
    document_onboarding_attachment_filename = fields.Char(string="File Name")

    onboarding_id_card = fields.Boolean(string="ID CARD PRODUCED", tracking=True)
    onboarding_id_card_remarks = fields.Char(string="Remarks", tracking=True)
    id_card_onboarding_attachment = fields.Binary(string="Uploaded ID CARD", attachment=True)
    id_card_onboarding_attachment_filename = fields.Char(string="File Name")

    onboarding_uniforms = fields.Boolean(string="UNIFORMS ISSUED", tracking=True)
    onboarding_uniforms_remarks = fields.Char(string="Remarks", tracking=True)
    uniforms_onboarding_attachment = fields.Binary(string="Uploaded UNIFORMS", attachment=True)
    uniforms_onboarding_attachment_filename = fields.Char(string="File Name")

    onboarding_referees = fields.Boolean(string="REFEREES /GUARANTOR FORM FILLED/ COLLECTED", tracking=True)
    onboarding_referees_remarks = fields.Char(string="Remarks", tracking=True)
    referees_onboarding_attachment = fields.Binary(string="Uploaded REFEREES Document", attachment=True)
    referees_onboarding_attachment_filename = fields.Char(string="File Name")

    onboarding_licenses = fields.Boolean(string="LICENSES COLLECTD AND DOCUMENT APPLICABLE FOR PILOTS/ CABIN CREW, FLIGHT DISPATCHERS, ENGINEERS / PLANNING", tracking=True)
    onboarding_licenses_remarks = fields.Char(string="Remarks", tracking=True)
    licenses_onboarding_attachment = fields.Binary(string="Uploaded LICENSES", attachment=True)
    licenses_onboarding_attachment_filename = fields.Char(string="File Name")

    onboarding_cv = fields.Boolean(string="CV AND CREDENTIALS RECEIVED AND DOCUMENTED", tracking=True)
    onboarding_cv_remarks = fields.Char(string="Remarks", tracking=True)
    cv_onboarding_attachment = fields.Binary(string="Uploaded CV Document", attachment=True)
    cv_onboarding_attachment_filename = fields.Char(string="File Name")

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