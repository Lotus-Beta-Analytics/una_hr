from odoo import models, fields,api,_
import logging
_logger = logging.getLogger(__name__)
# _logger.info("Application Values: %s", values)


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    degree_class = fields.Selection([
        ('first', 'First Class'),
        ('second_upper', 'Second Class Upper'),
        ('second_lower', 'Second Class Lower'),
        ('third', 'Third Class'),
        ('pass', 'Pass'),
        ('other', 'Other')
    ], string="Class of Degree")

    certifications = fields.Text(string="Professional Certifications")
    skills = fields.Text(string="Skills")
    cover_letter = fields.Text(string="Cover Letter")
    certifications_file = fields.Binary(string="Certifications File")
    certifications_filename = fields.Char(string="Certifications Filename")
    cover_letter_file = fields.Binary(string="Cover Letter File")
    cover_letter_filename = fields.Char(string="Cover Letter Filename")
    # degree = fields.Char(string="Degree")
    degree = fields.Selection([
    ('graduate', 'Graduate'),
    ('bachelor', 'Bachelor Degree'),
    ('master', 'Master Degree'),
    ('doctoral', 'Doctoral Degree'),
    ('other', 'Other'),
], string="Degree", default='bachelor')

    field_of_study = fields.Char(string="Field of Study")

    cover_letter_file = fields.Binary("Cover Letter File")
    cover_letter_filename = fields.Char("Cover Letter Filename")
    
    certificate_file = fields.Binary("Professional Certificate File")
    certificate_filename = fields.Char("Professional Certificate Filename")

    def _run_ocr_on_file(self, file_data, filename):
        if not file_data or not filename:
            return ''
        try:
            ext = filename.lower().split('.')[-1]
            content = ''
            file_bytes = base64.b64decode(file_data)
            if ext == 'pdf':
                reader = PdfReader(io.BytesIO(file_bytes))
                for page in reader.pages:
                    content += page.extract_text() or ''
            elif ext in ['png', 'jpg', 'jpeg']:
                image = Image.open(io.BytesIO(file_bytes))
                content = pytesseract.image_to_string(image)
            return content.strip()
        except Exception as e:
            return f"Failed to extract: {str(e)}"

    def _extract_cover_letter_text(self):
        text = self._run_ocr_on_file(self.cover_letter_file, self.cover_letter_filename)
        self.extracted_cover_letter_text = text
        self._assign_extracted_degree(text)

    def _assign_extracted_degree(self, text):
        degree = self._extract_degree_from_text(text)
        if degree:
            self.degree = degree

    def _extract_degree_from_text(self, text):
        if not text:
            return False
        degree_keywords = {
            'graduate': ['graduate diploma', 'graduated'],
            'bachelor': ['b.sc', 'bachelor', 'b.a'],
            'master': ['m.sc', 'master', 'mba', 'm.a'],
            'doctoral': ['phd', 'doctoral', 'doctorate'],
        }
        text_lower = text.lower()
        for degree_value, keywords in degree_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return degree_value
        return 'other'

    @api.model
    def create(self, vals):
        applicant = super().create(vals)
        if applicant.cover_letter_file:
            applicant._extract_cover_letter_text()
        return applicant



    extracted_cover_letter_text = fields.Text("Extracted Cover Letter Text")
    extracted_certificate_text = fields.Text("Extracted Certificate Text")

    # @api.model
    # def create(self, vals):
    #     applicant = super().create(vals)
    #     job = applicant.job_id
    #     if job:
    #         if job.cover_letter_digitization == 'auto' and vals.get('cover_letter_file'):
    #             applicant._extract_cover_letter_text()
    #         if job.certificate_digitization == 'auto' and vals.get('certifications_file'):
    #             applicant._extract_certificate_text()
    #     return applicant


    def _extract_cover_letter_text(self):
        self.extracted_cover_letter_text = self._run_ocr_on_file(
            self.cover_letter_file, self.cover_letter_filename
        )

    def _extract_certificate_text(self):
        self.extracted_certificate_text = self._run_ocr_on_file(
            self.certificate_file, self.certificate_filename
        )

    def _run_ocr_on_file(self, file_data, filename):
        if not file_data or not filename:
            return ''
        try:
            ext = filename.lower().split('.')[-1]
            content = ''
            file_bytes = base64.b64decode(file_data)
            if ext == 'pdf':
                reader = PdfReader(io.BytesIO(file_bytes))
                for page in reader.pages:
                    content += page.extract_text() or ''
            elif ext in ['png', 'jpg', 'jpeg']:
                image = Image.open(io.BytesIO(file_bytes))
                content = pytesseract.image_to_string(image)
            # Optional: parse .docx using docx library
            return content.strip()
        except Exception as e:
            return f"Failed to extract: {str(e)}"


