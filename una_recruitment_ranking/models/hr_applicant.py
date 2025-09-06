# -*- coding: utf-8 -*-
from odoo import api, fields, models
import re
from html import unescape

def _edu_rank(val):
    """Helper to rank education levels numerically for comparison."""
    order = {'none': 0, 'bachelor': 1, 'master': 2, 'phd': 3}
    return order.get((val or 'none').lower(), 0)

class HrApplicant(models.Model):
    _inherit = "hr.applicant"

    applicant_experience = fields.Char("Experience")
    applicant_education = fields.Char("Education") 
    certifications_text = fields.Text("Certifications")
    skills_text = fields.Text("Skills")                  

    fit_score = fields.Float("Fit Score", compute="_compute_fit_score", store=True)
    rank_order = fields.Integer("Rank Order", compute="_compute_rank_order", store=True)
    date_obtained = fields.Date("Date Obtained")
    expiration_date = fields.Date("Expiration Date")

    applicant_source = fields.Selection(
        [
            ("linkedin", "LinkedIn"),
            ("indeed", "Indeed"),
            ("glassdoor", "Glassdoor"),
            ("monster", "Monster"),
            ("ziprecruiter", "ZipRecruiter"),
            ("naukri", "Naukri"),
            ("careerbuilder", "CareerBuilder"),
            ("others", "Others"),
        ],
        string="Source",
        help="Where the applicant found this job posting.",
    )

    applicant_medium = fields.Selection(
        [
            ("linkedin", "LinkedIn"),
            ("indeed", "Indeed"),
            ("glassdoor", "Glassdoor"),
            ("monster", "Monster"),
            ("ziprecruiter", "ZipRecruiter"),
            ("naukri", "Naukri"),
            ("careerbuilder", "CareerBuilder"),
            ("others", "Others"),
        ],
        string="Medium",
        help="Where the applicant found this job posting.",
    )

    # -------------------------------
    # Extract structured info from description
    # -------------------------------
    def _extract_other_info(self):
        for app in self:
            if not app.description:
                continue
            # Remove HTML tags and decode entities
            text = re.sub(r'<[^>]+>', '\n', app.description or '')
            text = unescape(text)

            updates = {}
            for line in text.splitlines():
                if ":" not in line:
                    continue
                key, value = line.split(":", 1)
                key, value = key.strip().lower(), value.strip()

                if key == "applicant_experience":
                    updates["applicant_experience"] = re.sub(r'\D', '', value)
                elif key == "applicant_education":
                    updates["applicant_education"] = value.lower()
                elif key == "certifications_text":
                    updates["certifications_text"] = value
                elif key == "date_obtained":
                    updates["date_obtained"] = value 
                elif key == "expiration_date":
                    updates["expiration_date"] = value     
                elif key == "skills_text":
                    updates["skills_text"] = value
                elif key == "applicant_source":
                    if value.lower() in ["linkedin", "indeed", "glassdoor", "monster", 
                                        "ziprecruiter", "naukri", "careerbuilder", "others"]:
                        updates["applicant_source"] = value.lower()    
                elif key == "applicant_medium":
                    if value.lower() in ["linkedin", "indeed", "glassdoor", "monster", 
                                        "ziprecruiter", "naukri", "careerbuilder", "others"]:
                        updates["applicant_medium"] = value.lower()             

            if updates:
                app.with_context(skip_extract=True).sudo().write(updates)

    # -------------------------------
    # Compute Fit Score
    # -------------------------------
    @api.depends(
        "applicant_experience", "applicant_education", "skills_text", "certifications_text", "date_obtained", "expiration_date",'applicant_medium','applicant_source',
        "job_id.skill_ids", "job_id.min_experience", "job_id.education_level", "job_id.certification_ids",
        "job_id.weight_skills", "job_id.weight_experience", "job_id.weight_education", "job_id.weight_certifications"
    )
    def _compute_fit_score(self):
        for app in self:
            job = app.job_id
            if not job:
                app.fit_score = 0.0
                continue

            # --- Skills ---
            if job.skill_ids:
                applicant_skills = [s.strip().lower() for s in (app.skills_text or "").split(",") if s.strip()]
                required_skills = [r.lower() for r in job.skill_ids.mapped("name")]
                matched = sum(1 for s in applicant_skills if s in required_skills)
                skills_score = (matched / max(len(required_skills), 1)) * (job.weight_skills or 0)
            else:
                skills_score = 0.0

            # --- Experience ---
            try:
                exp_years = int(app.applicant_experience or 0)
            except ValueError:
                exp_years = 0
            exp_score = (job.weight_experience or 0) if exp_years >= (job.min_experience or 0) else 0.0

            # --- Education ---
            edu_score = 0.0
            if app.applicant_education and job.education_level:
                if _edu_rank(app.applicant_education) >= _edu_rank(job.education_level):
                    edu_score = job.weight_education or 0

            # --- Certifications ---
            if job.certification_ids:
                applicant_certs = [c.strip().lower() for c in (app.certifications_text or "").split(",") if c.strip()]
                required_certs = [r.lower() for r in job.certification_ids.mapped("name")]
                matched = sum(1 for c in applicant_certs if c in required_certs)
                cert_score = (matched / max(len(required_certs), 1)) * (job.weight_certifications or 0)
            else:
                cert_score = 0.0

            total_score = skills_score + exp_score + edu_score + cert_score
            app.fit_score = max(0.0, min(100.0, total_score))

    # -------------------------------
    # Compute Rank Order (within job)
    # -------------------------------
    @api.depends("fit_score", "job_id")
    def _compute_rank_order(self):
        for job in self.mapped("job_id"):
            apps = job.application_ids.filtered(lambda a: a.id)
            apps_sorted = apps.sorted(key=lambda a: (a.fit_score, a.id), reverse=True)
            for idx, app in enumerate(apps_sorted, start=1):
                app.rank_order = idx

    # -------------------------------
    # Overrides to trigger extraction
    # -------------------------------
    @api.model
    def create(self, vals):
        app = super().create(vals)
        if not self.env.context.get("skip_extract"):
            app._extract_other_info()
        return app

    def write(self, vals):
        res = super().write(vals)
        if not self.env.context.get("skip_extract"):
            for app in self:
                app._extract_other_info()
        return res
