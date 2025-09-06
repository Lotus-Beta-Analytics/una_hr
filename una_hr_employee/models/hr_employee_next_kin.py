# models/hr_employee_next_kin.py

from odoo import models, fields,api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    next_of_kin_name = fields.Char(string='Next of Kin Name')
    next_of_kin_relationship = fields.Char(string='Relationship')
    next_of_kin_phone = fields.Char(string='Phone')
    next_of_kin_email = fields.Char(string='Email')
    next_of_kin_address = fields.Text(string='Address')
    birth_certificate = fields.Binary(string='Birth Certificate (PDF)')
    birth_certificate_filename = fields.Char(string='Filename')
    education_certificate = fields.Binary("Education Certificate (PDF)")
    education_certificate_filename = fields.Char("Education Certificate Filename")

   

    education_certificate_status_html = fields.Html(
        string="Upload Status",
        compute="_compute_education_certificate_status_html",
        sanitize=False,
    )

    birth_certificate_status_html = fields.Html(
        string="Birth Certificate Upload Status",
        compute="_compute_birth_certificate_status_html",
        sanitize=False,
    )

    

    @api.depends('birth_certificate', 'birth_certificate_filename')
    def _compute_birth_certificate_status_html(self):
        for rec in self:
            if rec.birth_certificate and rec.birth_certificate_filename and rec.birth_certificate_filename.lower().endswith('.pdf'):
                rec.birth_certificate_status_html = """
                <div style="
                    margin-top: 8px;
                    padding: 10px;
                    background-color: #d4edda;
                    color: #155724;
                    border: 1px solid #c3e6cb;
                    border-radius: 5px;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                ">
                    <i class="fa fa-check-circle" style="color: #28a745; font-size: 18px;"></i>
                    <span>Birth Certificate uploaded successfully.</span>
                </div>
                """
            elif rec.birth_certificate or rec.birth_certificate_filename:
                rec.birth_certificate_status_html = """
                <div style="
                    margin-top: 8px;
                    padding: 10px;
                    background-color: #f8d7da;
                    color: #721c24;
                    border: 1px solid #f5c6cb;
                    border-radius: 5px;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                ">
                    <i class="fa fa-times-circle" style="color: #dc3545; font-size: 18px;"></i>
                    <span>Invalid file. Please upload a PDF file only.</span>
                </div>
                """
            else:
                rec.birth_certificate_status_html = False


    @api.depends('education_certificate', 'education_certificate_filename')
    def _compute_education_certificate_status_html(self):
        for rec in self:
            if rec.education_certificate and rec.education_certificate_filename and rec.education_certificate_filename.lower().endswith('.pdf'):
                rec.education_certificate_status_html = """
                <div style="
                    margin-top: 8px;
                    padding: 10px;
                    background-color: #d4edda;
                    color: #155724;
                    border: 1px solid #c3e6cb;
                    border-radius: 5px;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                ">
                    <i class="fa fa-check-circle" style="color: #28a745; font-size: 18px;"></i>
                    <span>Education Certificate uploaded successfully.</span>
                </div>
                """
            elif rec.education_certificate or rec.education_certificate_filename:
                rec.education_certificate_status_html = """
                <div style="
                    margin-top: 8px;
                    padding: 10px;
                    background-color: #f8d7da;
                    color: #721c24;
                    border: 1px solid #f5c6cb;
                    border-radius: 5px;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                ">
                    <i class="fa fa-times-circle" style="color: #dc3545; font-size: 18px;"></i>
                    <span>Invalid file. Please upload a PDF file only.</span>
                </div>
                """
            else:
                rec.education_certificate_status_html = False

