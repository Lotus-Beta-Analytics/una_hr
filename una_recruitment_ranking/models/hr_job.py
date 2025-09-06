# -*- coding: utf-8 -*-
from odoo import models, fields, api
from statistics import mean

class HrJob(models.Model):
    _inherit = 'hr.job'

    # Fit criteria
    skill_ids = fields.Many2many('hr.skill', string="Required Skills")
    min_experience = fields.Integer(string="Minimum Experience (Years)", default=0)
    education_level = fields.Selection([
        ('none', 'None'),
        ('bachelor', 'Bachelor'),
        ('master', 'Master'),
        ('phd', 'PhD'),
    ], string="Minimum Education", default='none')
    certification_ids = fields.Many2many('hr.certification', string="Required Certifications")

    # Weights (sum ideally to 100)
    weight_skills = fields.Integer(string="Weight: Skills (%)", default=50)
    weight_experience = fields.Integer(string="Weight: Experience (%)", default=20)
    weight_education = fields.Integer(string="Weight: Education (%)", default=20)
    weight_certifications = fields.Integer(string="Weight: Certifications (%)", default=10)

    # Dashboard KPIs
    applicant_count = fields.Integer(string="Applicants", compute="_compute_applicant_stats", store=False)
    top_fit_score = fields.Float(string="Top Score", compute="_compute_applicant_stats", store=False)
    avg_fit_score = fields.Float(string="Average Score", compute="_compute_applicant_stats", store=False)
    strong_fit_count = fields.Integer(string="Strong Fits (>=75)", compute="_compute_applicant_stats", store=False)

    # Top applicants preview (HTML)
    top_applicants_html = fields.Html(string="Top Applicants", compute="_compute_applicant_stats", sanitize=False)

    @api.depends('application_ids.fit_score')
    def _compute_applicant_stats(self):
        for job in self:
            apps = job.application_ids.sorted(key=lambda a: (a.fit_score, a.id), reverse=True)
            scores = [a.fit_score for a in apps if a.fit_score]
            job.applicant_count = len(apps)
            job.top_fit_score = scores[0] if scores else 0.0
            job.avg_fit_score = round(mean(scores), 2) if scores else 0.0
            job.strong_fit_count = len([s for s in scores if s >= 75])

            # Build HTML table for top 3
            top = apps[:3]
            rows = "".join(f"<tr><td>{a.partner_name or a.name}</td><td style='text-align:right'>{round(a.fit_score or 0, 2)}</td><td style='text-align:center'>{a.rank_order or ''}</td></tr>" for a in top)
            job.top_applicants_html = f'''
                <div class="oe_title">
                    <h3>Top Applicants</h3>
                </div>
                <table class="o_list_view table table-sm">
                    <thead><tr><th>Name</th><th style="text-align:right">Fit Score</th><th style="text-align:center">Rank</th></tr></thead>
                    <tbody>{rows or '<tr><td colspan="3">No applicants yet.</td></tr>'}</tbody>
                </table>
            '''
