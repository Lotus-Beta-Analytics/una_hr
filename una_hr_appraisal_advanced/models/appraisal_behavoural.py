from odoo import models, fields, api

class HrAppraisal(models.Model):
    _inherit = 'hr.appraisal'

    behavioral_competency_line_ids = fields.One2many(
        'hr.appraisal.behavioral.competency', 'appraisal_id',
        string="Behavioral Competencies"
    )
    emp_id = fields.Char(
        string="Employee ID Number",
        related='employee_id.emp_id',
        store=True,
        readonly=True  # Optional: Set to True to make it readonly in UI
    )
    job_id = fields.Many2one(
        'hr.job',
        string="Job Position",
        related='employee_id.job_id',
        store=True,
        readonly=False  # Optional
    )
    appraisal_month = fields.Selection(
        selection=[
            ('01', 'January'),
            ('02', 'February'),
            ('03', 'March'),
            ('04', 'April'),
            ('05', 'May'),
            ('06', 'June'),
            ('07', 'July'),
            ('08', 'August'),
            ('09', 'September'),
            ('10', 'October'),
            ('11', 'November'),
            ('12', 'December'),
        ],
        string="Appraisal Month"
    )
    review_period = fields.Selection(
    selection=[
        ('first_half', 'First Half'),
        ('second_half', 'Second Half'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ],
    string="Review Period"
)


    def _populate_default_behavioral_competencies(self):
        BehavioralLine = self.env['hr.appraisal.behavioral.competency']
        for record in self:
            default_competencies = [
                {
                    'competency_name': "Behavioral Competency",
                    'key_initiative_ids': "Customer Satisfaction",
                    'kpi_ids': "Ensures top-notch Internal & External customers satisfaction",
                    'weight': 20.0,
                    'employee_id': record.employee_id.id,
                    'appraisal_id': record.id,
                },
                {
                    'competency_name': "Behavioral Competency",
                    'key_initiative_ids': "Innovation & Creativity",
                    'kpi_ids': "Encourage rapid development & unconventional thinking",
                    'weight': 30.0,
                    'employee_id': record.employee_id.id,
                    'appraisal_id': record.id,
                },
                {
                    'competency_name': "Behavioral Competency",
                    'key_initiative_ids': "Honesty & Integrity",
                    'kpi_ids': "Encourage employees to model ethical behaviour consistently",
                    'weight': 20.0,
                    'employee_id': record.employee_id.id,
                    'appraisal_id': record.id,
                },
                {
                    'competency_name': "Behavioral Competency",
                    'key_initiative_ids': "Respect for Internal & External Customers",
                    'kpi_ids': "Encourage and embed customer first mindset across departments",
                    'weight': 30.0,
                    'employee_id': record.employee_id.id,
                    'appraisal_id': record.id,
                },
                {
                    'competency_name': "Behavioral Competency",
                    'key_initiative_ids': "Safety",
                    'kpi_ids': "Encourage and embed safety consciousness among employee (Safety is everyone's business)",
                    'weight': 0.0,
                    'employee_id': record.employee_id.id,
                    'appraisal_id': record.id,
                },
            ]
            BehavioralLine.create(default_competencies)

    @api.model
    def create(self, vals):
        record = super(HrAppraisal, self).create(vals)
        if record.employee_id and not record.behavioral_competency_line_ids:
            record._populate_default_behavioral_competencies()
        return record

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if self.env.context.get('default_employee_id'):
            res['behavioral_competency_line_ids'] = [(0, 0, line) for line in [
                {
                    'competency_name': "Behavioral Competency",
                    'key_initiative_ids': "Customer Satisfaction",
                    'kpi_ids': "Ensures top-notch Internal & External customers satisfaction",
                    'weight': 20.0,
                    'employee_id': self.env.context['default_employee_id'],
                },
                {
                    'competency_name': "Behavioral Competency",
                    'key_initiative_ids': "Innovation & Creativity",
                    'kpi_ids': "Encourage rapid development & unconventional thinking",
                    'weight': 30.0,
                    'employee_id': self.env.context['default_employee_id'],
                },
                {
                    'competency_name': "Behavioral Competency",
                    'key_initiative_ids': "Honesty & Integrity",
                    'kpi_ids': "Encourage employees to model ethical behaviour consistently",
                    'weight': 20.0,
                    'employee_id': self.env.context['default_employee_id'],
                },
                {
                    'competency_name': "Behavioral Competency",
                    'key_initiative_ids': "Respect for Internal & External Customers",
                    'kpi_ids': "Encourage and embed customer first mindset across departments",
                    'weight': 30.0,
                    'employee_id': self.env.context['default_employee_id'],
                },
                {
                    'competency_name': "Behavioral Competency",
                    'key_initiative_ids': "Safety",
                    'kpi_ids': "Encourage and embed safety consciousness among employee (Safety is everyone's business)",
                    'weight': 0.0,
                    'employee_id': self.env.context['default_employee_id'],
                },
            ]]
        return res

