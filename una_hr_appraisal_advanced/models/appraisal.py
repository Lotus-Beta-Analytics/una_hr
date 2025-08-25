from odoo import models, fields, api,_
from odoo.exceptions import UserError 
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)
from odoo.tools.float_utils import float_compare
from odoo.exceptions import AccessError


class HrAppraisal(models.Model):
    _inherit = 'hr.appraisal'
    strategic_objective_line_ids = fields.One2many(
        'hr.appraisal.strategic.objective', 'appraisal_id', string="Strategic Objectives")
    behavioral_competency_line_ids = fields.One2many(
        'hr.appraisal.behavioral.competency', 'appraisal_id', string="Behavioral Competencies")
    personal_development_goal_line_ids = fields.One2many(
        'hr.appraisal.personal.development', 'appraisal_id', string="Personal Development Goals")
    functional_objective_weighted_avg = fields.Float(
        string='Functional Objective Weighted Average (70%)',
        compute='_compute_weighted_averages',
        store=True)

    behavioral_competency_weighted_avg = fields.Float(
        string='Behavioral Competency Weighted Average (20%)',
        compute='_compute_weighted_averages',
        store=True)
    personal_development_goal_weighted_avg = fields.Float(
        string="Personal Development Goal Weighted Average (10%)",
        compute='_compute_weighted_averages',
        store=True
    )
    final_score = fields.Float(
        string='Final Score',
        compute='_compute_weighted_averages',
        store=True)

    manager_ids = fields.Many2many(
    'hr.employee',
    string="Managers",
    default=lambda self: self.env['hr.employee'].browse([])
)   
    manager_rating = fields.Selection(
        [
            ('1', '1 = Unacceptable'),
            ('2', '2 = Partially Meets Expectation'),
            ('3', '3 = Meets Expectation'),
            ('4', '4 = Exceeds Expectation'),
            ('5', '5 = Exceptional'),
        ],
        string='Manager Rating (1-5)'
    )

    hr_rating = fields.Selection(
        [
            ('1', '1 = Unacceptable'),
            ('2', '2 = Partially Meets Expectation'),
            ('3', '3 = Meets Expectation'),
            ('4', '4 = Exceeds Expectation'),
            ('5', '5 = Exceptional'),
        ],
        string='HR Rating (1-5)'
    )


    @api.model
    def create(self, vals):
        record = super().create(vals)

        employee = record.employee_id or record.appraisal_id.employee_id
        current_user_employee = self.env.user.employee_id

        _logger.warning(f"[DEBUG] Creating appraisal line:")
        _logger.warning(f"  Logged-in user: {self.env.user.name} (Employee: {current_user_employee.name})")
        _logger.warning(f"  Target employee: {employee.name if employee else 'None'}")
        _logger.warning(f"  Direct manager: {employee.parent_id.name if employee else 'None'}")
        _logger.warning(f"  manager_rating: {record.manager_rating}")

        if record.manager_rating and employee:
            if employee.parent_id != current_user_employee:
                _logger.warning(f"[BLOCKED] Unauthorized user tried to set manager_rating.")
                raise AccessError(_("Only the direct manager can set the manager rating."))

        return record

    
    def write(self, vals):
        for record in self:
            if 'manager_rating' in vals:
                new_rating = vals.get('manager_rating')
                old_rating = record.manager_rating
                if new_rating != old_rating:
                    if record.employee_id.parent_id != self.env.user.employee_id:
                        raise AccessError(_("Only the direct manager can update the manager rating."))
        return super().write(vals)

    state = fields.Selection([
        ('new', 'Pending Submission'),
        ('submitted', 'Pending Line Manager Approval'),
        ('manager_approved', 'Pending Hr Manager Approval'),
        ('hr_approved', 'Approved'),
        ('cancel', 'Cancelled'),
    ], string="Status", default='new', tracking=True)

    def _statusbar_colors(self):
        return {
            'new': 'blue',
            'submitted': 'orange',
            'manager_approved': 'purple',
            'hr_approved': 'green',
            'cancel': 'red'
        }


    final_rating_label = fields.Char(
        string='Final Appraisal Rating',
        compute='_compute_rating_label',
        store=True
    )
    is_line_manager = fields.Boolean(string="Is Line Manager", compute="_compute_is_line_manager", store=False)

    manager_id = fields.Many2one(
        'hr.employee',
        string='Manager',
        compute='_compute_manager_id',
        store=True,
        readonly=False,
    )

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        if self.employee_id:
            manager = self.employee_id.parent_id
            if manager and manager != self.employee_id:
                self.manager_ids = [(6, 0, [manager.id])]
            else:
                self.manager_ids = [(5, 0, 0)]  # Clears the Many2many field
        else:
            self.manager_ids = [(5, 0, 0)]



    date = fields.Date(string="Date")
    @api.depends('employee_id')
    def _compute_manager_id(self):
        for rec in self:
            rec.manager_id = rec.employee_id.parent_id

    @api.depends('manager_ids')
    def _compute_is_line_manager(self):
        current_employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        for rec in self:
            rec.is_line_manager = current_employee and current_employee.id in rec.manager_ids.ids


    @api.depends('final_score')
    def _compute_rating_label(self):
        for rec in self:
            score = rec.final_score
            if score >= 90:
                rec.final_rating_label = "5 = Exceptional"
            elif score >= 75:
                rec.final_rating_label = "4 = Exceeds Expectation"
            elif score >= 60:
                rec.final_rating_label = "3 = Meets Expectation"
            elif score >= 40:
                rec.final_rating_label = "2 = Partially Meets Expectation"
            else:
                rec.final_rating_label = "1 = Unacceptable"


    def action_submit(self):
        for rec in self:
            rec.state = 'submitted'
            template = self.env.ref(
                'una_hr_appraisal_advanced.mail_template_employee_appraisal_submitted',
                raise_if_not_found=False
            )
            if template and rec.manager_id and rec.manager_id.work_email:
                try:
                    template.send_mail(rec.id, force_send=True)
                except Exception as e:
                    _logger.warning("Failed to send appraisal submission email to manager %s: %s", rec.manager_id.name, e)
            rec.message_post(
                body=_("Appraisal submitted by %s. Notification sent to manager: %s (%s).") % (
                    rec.employee_id.name, rec.manager_id.name, rec.manager_id.work_email),
                subtype_id=self.env.ref('mail.mt_note').id
            )


    @api.constrains('manager_rating')
    def _check_manager_rating_edit(self):
        for rec in self:
            if rec.manager_rating:
                if rec.state != 'submitted' or rec.manager_id.user_id != self.env.user:
                    raise UserError("Only the line manager can set a rating when the appraisal is in 'submitted' state.")
        


    def action_manager_approve(self):
        for rec in self:
            rec.state = 'manager_approved'
            template = self.env.ref('una_hr_appraisal_advanced.mail_template_appraisal_manager_approved_notify_hr',
                raise_if_not_found=False
            )
            if template:
                try:
                    template.send_mail(rec.id, force_send=True)
                    _logger.info("Manager approval email sent to HR for employee %s", rec.employee_id.name)
                    rec.message_post(
                        body="Appraisal approved by Manager. Notification sent to HR.",
                        subtype_id=self.env.ref('mail.mt_note').id
                    )
                except Exception as e:
                    _logger.warning("Failed to send manager approval email to HR for %s: %s", rec.employee_id.name, e)
            else:
                _logger.warning("Email template 'mail_template_appraisal_manager_approved_notify_hr' not found.")


            
           

    def action_hr_approve(self):
        for rec in self:
            rec.state = 'hr_approved'
            template = self.env.ref('una_hr_appraisal_advanced.mail_template_employee_appraisal_approved', raise_if_not_found=False)
            if template:
                try:
                    template.send_mail(rec.id, force_send=False)  # force_send=True to send immediately
                except Exception as e:
                    _logger.warning("Failed to send HR approval email to employee %s: %s", rec.employee_id.name, e)
            rec.message_post(
                body=f"Appraisal approved by HR. Notification sent to employee: {rec.employee_id.name} ({rec.employee_id.work_email}).",
                subtype_id=self.env.ref('mail.mt_note').id
            )


    def action_cancel(self):
        self.write({'state': 'cancel'})

    def action_reopen(self):
        self.write({'state': 'new'})

   
    @api.model
    def default_get(self, fields_list):
        res = super(HrAppraisal, self).default_get(fields_list)

        if 'manager_ids' in fields_list and 'manager_ids' not in res:
            res['manager_ids'] = [(6, 0, [])]

        employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        _logger.info(">>> Default Get Triggered for Appraisal <<<")

        if employee:
            _logger.info(f">>> Found Employee: {employee.name}")
            res['employee_id'] = employee.id

            if employee.parent_id:
                _logger.info(f">>> Found Manager: {employee.parent_id.name}")
                res['manager_ids'] = [(6, 0, [employee.parent_id.id])]
        else:
            _logger.warning(f">>> No employee found for user_id={self.env.uid}")

        return res
        
    @api.depends(
    'strategic_objective_line_ids.score',
    'strategic_objective_line_ids.weight',
    'behavioral_competency_line_ids.score',
    'behavioral_competency_line_ids.weight',
    'personal_development_goal_line_ids.score',
    'personal_development_goal_line_ids.weight'
    )
    def _compute_weighted_averages(self):
        for appraisal in self:
            # === Functional Objective Weighted Average (70%) ===
            scores = []
            total_weighted_score = 0.0
            for line in appraisal.strategic_objective_line_ids:
                if line.score is not None and line.weight:
                    scores.append(line.score)
                    total_weighted_score += line.score

            if scores:
                # Excel formula logic: (Total Score / 100) * 70 / Number of Items
                avg_score = (total_weighted_score / 100.0) * 70.0 / 5.0
            else:
                avg_score = 0.0

            appraisal.functional_objective_weighted_avg = avg_score

            # === Behavioral Competency Weighted Average (20%) ===
            behav_scores = []
            total_behav_score = 0.0
            for line in appraisal.behavioral_competency_line_ids:
                if line.score is not None and line.weight:
                    behav_scores.append(line.score)
                    total_behav_score += line.score

            if behav_scores:
                avg_behav = (total_behav_score / 100.0) * 20.0 / 5.0
            else:
                avg_behav = 0.0

            appraisal.behavioral_competency_weighted_avg = avg_behav

            # === Personal Development Goal Weighted Average (10%) ===
            dev_scores = []
            total_dev_score = 0.0
            for line in appraisal.personal_development_goal_line_ids:
                if line.score is not None and line.weight:
                    dev_scores.append(line.score)
                    total_dev_score += line.score

            if dev_scores:
                avg_dev = (total_dev_score / 100.0) * 10.0 / 5.0
            else:
                avg_dev = 0.0

            appraisal.personal_development_goal_weighted_avg = avg_dev

            # === Final Score ===
            appraisal.final_score = (
                appraisal.functional_objective_weighted_avg +
                appraisal.behavioral_competency_weighted_avg +
                appraisal.personal_development_goal_weighted_avg
            )

   
class HrAppraisalLine(models.Model):
    _name = 'hr.appraisal.line'
    _description = 'Appraisal Line'
    name = fields.Char(string="Name")
    key_initiative_ids = fields.Char(string="Key Initiative")
    kpi_ids = fields.Char(string="Key Initiative")

class HrAppraisalStrategicObjective(models.Model):
    _name = 'hr.appraisal.strategic.objective'
    _description = 'Strategic Objective Line'
    appraisal_id = fields.Many2one('hr.appraisal', string='Appraisal Reference', required=True, ondelete='cascade')

    name = fields.Char(string='Functional Objective')
    key_initiative_ids = fields.Many2one(
    comodel_name='appraisal.key.initiative',
    string='Key Initiative',
    # domain="[('department_id', '=', employee_department_id)]",
)

    kpi_ids = fields.Many2one(
        comodel_name='appraisal.kpi',
        string='KPI',
        # domain="[('department_id', '=', employee_department_id)]",
    )
   

    weight = fields.Float(string='Weight(70%)', required=True, default=0.0)

    employee_self_rating = fields.Selection(
        [(str(i), str(i)) for i in range(1, 6)], string='Employee Self-Rating (1-5)')
    manager_rating = fields.Selection([
        ('1', '1 = Unacceptable'),
        ('2', '2 = Partially Meets Expectation'),
        ('3', '3 = Meets Expectation'),
        ('4', '4 = Exceeds Expectation'),
        ('5', '5 = Exceptional'),
    ], string='Manager Rating (1-5)')

    @api.model
    def create(self, vals):
        record = super().create(vals)

        employee = record.employee_id or record.appraisal_id.employee_id
        current_user_employee = self.env.user.employee_id

        _logger.warning(f"[DEBUG] Creating appraisal line:")
        _logger.warning(f"  Logged-in user: {self.env.user.name} (Employee: {current_user_employee.name})")
        _logger.warning(f"  Target employee: {employee.name if employee else 'None'}")
        _logger.warning(f"  Direct manager: {employee.parent_id.name if employee else 'None'}")
        _logger.warning(f"  manager_rating: {record.manager_rating}")

        if record.manager_rating and employee:
            if employee.parent_id != current_user_employee:
                _logger.warning(f"[BLOCKED] Unauthorized user tried to set manager_rating.")
                raise AccessError(_("Only the direct manager can set the manager rating."))

        return record
    
    def write(self, vals):
        for record in self:
            if 'manager_rating' in vals:
                new_rating = vals.get('manager_rating')
                old_rating = record.manager_rating
                if new_rating != old_rating:
                    if record.employee_id.parent_id != self.env.user.employee_id:
                        raise AccessError(_("Only the direct manager can update the manager rating."))
        return super().write(vals)

   

    score = fields.Float(string='Score', compute='_compute_score', store=True)
    comments = fields.Text(string='Comments')

    config_id = fields.Many2one('appraisal.strategic.objective.config', string="Select from Config")
    employee_id = fields.Many2one('hr.employee', string="Employee")  # if not already defined

    employee_department_id = fields.Many2one(
        'hr.department',
        string='Employee Department',
        compute='_compute_employee_department_id',
        store=True
    )


    @api.depends('employee_id.department_id')
    def _compute_employee_department_id(self):
        for record in self:
            record.employee_department_id = record.employee_id.department_id

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        domain = {}
        if self.employee_id and self.employee_id.department_id:
            dept_id = self.employee_id.department_id.id
            domain['key_initiative_ids'] = [('department_id', '=', dept_id)]
            domain['kpi_ids'] = [('department_id', '=', dept_id)]
        return {'domain': domain}         
    
    @api.onchange('config_id')
    def _onchange_config_id(self):
        if self.config_id:
            self.name = self.config_id.name
            self.weight = self.config_id.weight
            # self.kpi_ids = self.config_id.kpi_ids
            # self.key_initiative_ids = self.config_id.key_initiative_ids

    @api.depends('weight', 'employee_self_rating', 'manager_rating')
    def _compute_score(self):
        for line in self:
            # emp_rating = float(line.employee_self_rating) if line.employee_self_rating else 0.0
            mgr_rating = float(line.manager_rating) if line.manager_rating else 0.0
            # avg_rating = (emp_rating + mgr_rating) / 2 if (emp_rating and mgr_rating) else 0.0
            line.score = line.weight * mgr_rating 

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        domain = {}
        current_employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)

        if current_employee:
            if self.env.user.has_group('una_hr_appraisal_advanced.group_hr_appraisal_employee'):
                domain['employee_id'] = [('id', '=', current_employee.id)]
            elif self.env.user.has_group('una_hr_appraisal_advanced.group_hr_appraisal_manager'):
                if current_employee.department_id:
                    domain['employee_id'] = [('department_id', '=', current_employee.department_id.id)]
            elif self.env.user.has_group('una_hr_appraisal_advanced.group_hr_team_appraisal_manager'):
                domain['employee_id'] = []  # or leave unset for full access
            if current_employee.department_id:
                domain['config_id'] = [('department_id', '=', current_employee.department_id.id)]
    
class HrAppraisalBehavioralCompetency(models.Model):
    _name = 'hr.appraisal.behavioral.competency'
    _description = 'Behavioral Competency Line'
    appraisal_id = fields.Many2one('hr.appraisal', string='Appraisal Reference', required=True, ondelete='cascade')

    competency_name = fields.Char(string='Behavioral Competency')
    key_initiative_ids = fields.Char(string='Key Initiative')
    kpi_ids = fields.Char(string='KPI')
    weight = fields.Float(string='Weight(20%)', required=True, default=0.0)

    employee_self_rating = fields.Selection(
        [(str(i), str(i)) for i in range(1, 6)], string='Employee Self-Rating (1-5)')
    manager_rating = fields.Selection([
        ('1', '1 = Unacceptable'),
        ('2', '2 = Partially Meets Expectation'),
        ('3', '3 = Meets Expectation'),
        ('4', '4 = Exceeds Expectation'),
        ('5', '5 = Exceptional'),
    ], string='Manager Rating (1-5)')
    
    @api.model
    def create(self, vals):
        record = super().create(vals)

        employee = record.employee_id or record.appraisal_id.employee_id
        current_user_employee = self.env.user.employee_id

        _logger.warning(f"[DEBUG] Creating appraisal line:")
        _logger.warning(f"  Logged-in user: {self.env.user.name} (Employee: {current_user_employee.name})")
        _logger.warning(f"  Target employee: {employee.name if employee else 'None'}")
        _logger.warning(f"  Direct manager: {employee.parent_id.name if employee else 'None'}")
        _logger.warning(f"  manager_rating: {record.manager_rating}")

        if record.manager_rating and employee:
            if employee.parent_id != current_user_employee:
                _logger.warning(f"[BLOCKED] Unauthorized user tried to set manager_rating.")
                raise AccessError(_("Only the direct manager can set the manager rating."))

        return record
    
    def write(self, vals):
        for record in self:
            if 'manager_rating' in vals:
                new_rating = vals.get('manager_rating')
                old_rating = record.manager_rating
                if new_rating != old_rating:
                    if record.employee_id.parent_id != self.env.user.employee_id:
                        raise AccessError(_("Only the direct manager can update the manager rating."))
        return super().write(vals)

    score = fields.Float(string='Score', compute='_compute_score', store=True)
    comments = fields.Text(string='Comments')

    config_id = fields.Many2one('appraisal.behavioral.competency.config', string="Select from Config")
    employee_id = fields.Many2one('hr.employee', string="Employee")  # if not already defined

    employee_department_id = fields.Many2one(
        'hr.department',
        string='Employee Department',
        # compute='_compute_employee_department_id',
        store=True
    )

    @api.depends('weight', 'employee_self_rating', 'manager_rating')
    def _compute_score(self):
        for line in self:
            mgr_rating = float(line.manager_rating) if line.manager_rating else 0.0
            line.score = line.weight * mgr_rating

    def _onchange_employee_id(self):
        domain = {}
        current_employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)

        if current_employee:
            if self.env.user.has_group('una_hr_appraisal_advanced.group_hr_appraisal_employee'):
                domain['employee_id'] = [('id', '=', current_employee.id)]
            elif self.env.user.has_group('una_hr_appraisal_advanced.group_hr_team_appraisal_manager'):
                if current_employee.department_id:
                    domain['employee_id'] = [('department_id', '=', current_employee.department_id.id)]
            elif self.env.user.has_group('una_hr_appraisal_advanced.group_hr_appraisal_manager'):
                domain['employee_id'] = []  # or leave unset for full access
            if current_employee.department_id:
                domain['config_id'] = [('department_id', '=', current_employee.department_id.id)]

        return {'domain': domain}
        
    @api.onchange('config_id')
    def _onchange_config_id(self):
        if self.config_id:
            self.competency_name = self.config_id.competency_name
            self.weight = self.config_id.weight
            self.kpi_ids = self.config_id.kpi_ids
            self.key_initiative_ids = self.config_id.key_initiative_ids



class HrAppraisalPersonalDevelopment(models.Model):
    _name = 'hr.appraisal.personal.development'
    _description = 'Personal Development Goal Line'

    appraisal_id = fields.Many2one('hr.appraisal', string='Appraisal Reference', required=True, ondelete='cascade')

    goal = fields.Char(string='Personal Development Goal')
    weight = fields.Float(string='Weight(10%)', required=True, default=0.0)
   
    results = fields.Text(string='Results')
    # score = fields.Float(string='Score', default=0)

    employee_self_rating = fields.Selection(
        [(str(i), str(i)) for i in range(1, 6)], string='Employee Self-Rating (1-5)')
    manager_rating = fields.Selection([
    ('1', '1 = Unacceptable'),
    ('2', '2 = Partially Meets Expectation'),
    ('3', '3 = Meets Expectation'),
    ('4', '4 = Exceeds Expectation'),
    ('5', '5 = Exceptional'),
], string='Manager Rating (1-5)')
    
    @api.model
    def create(self, vals):
        record = super().create(vals)

        employee = record.employee_id or record.appraisal_id.employee_id
        current_user_employee = self.env.user.employee_id

        _logger.warning(f"[DEBUG] Creating appraisal line:")
        _logger.warning(f"  Logged-in user: {self.env.user.name} (Employee: {current_user_employee.name})")
        _logger.warning(f"  Target employee: {employee.name if employee else 'None'}")
        _logger.warning(f"  Direct manager: {employee.parent_id.name if employee else 'None'}")
        _logger.warning(f"  manager_rating: {record.manager_rating}")

        if record.manager_rating and employee:
            if employee.parent_id != current_user_employee:
                _logger.warning(f"[BLOCKED] Unauthorized user tried to set manager_rating.")
                raise AccessError(_("Only the direct manager can set the manager rating."))

        return record
    score = fields.Float(string='Score', compute='_compute_score', store=True)

    config_id = fields.Many2one('appraisal.personal.development.config', string="Select from Config")
    odoo_goal_id = fields.Many2one('hr.appraisal.goal')
    employee_id = fields.Many2one('hr.employee', string="Employee")  # if not already defined

    employee_department_id = fields.Many2one(
        'hr.department',
        string='Employee Department',
        compute='_compute_employee_department_id',
        store=True
    )
    progression = fields.Selection(related='odoo_goal_id.progression', string="Progress", store=True)

    # Fields
    progress = fields.Float(related='odoo_goal_id.progress', string='Progress (%)', store=True)

    goal_progress_cache = fields.Float(
    string="Goal Progress Cache",
    compute='_compute_goal_progress_cache',
    store=True
)

    @api.depends('odoo_goal_id.progress')
    def _compute_goal_progress_cache(self):
        for rec in self:
            rec.goal_progress_cache = rec.odoo_goal_id.progress or 0.0

    rating_scale = fields.Selection([
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ], string='Rating Scale', compute='_compute_rating_scale', store=True)

    @api.depends('goal_progress_cache')
    def _compute_rating_scale(self):
        for rec in self:
            progress = rec.goal_progress_cache
            if progress == 0:
                rec.rating_scale = 'not_started'
            elif progress == 100:
                rec.rating_scale = 'completed'
            else:
                rec.rating_scale = 'in_progress'

    # 🆕 HTML Label Field
    rating_scale_label_html = fields.Html(
        string="Rating Scale",
        compute='_compute_rating_label_html',
        sanitize=False,
        store = True
    )

    @api.depends('rating_scale')
    def _compute_rating_label_html(self):
        for rec in self:
            if rec.rating_scale == 'completed':
                color = '#28a745'
                icon = 'fa-check'
                label = 'COMPLETED'
            elif rec.rating_scale == 'in_progress':
                color = '#ffc107'
                icon = 'fa-spinner'
                label = 'IN PROGRESS'
            else:
                color = '#dc3545'
                icon = 'fa-times'
                label = 'NOT STARTED'

            rec.rating_scale_label_html = f"""
                <div style="
                    position: relative;
                    display: inline-block;
                    background-color: {color};
                    color: white;
                    font-weight: bold;
                    padding: 5px 15px;
                    border-radius: 20px;
                    font-size: 12px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
                    ">
                    <i class="fa {icon}" aria-hidden="true"></i> {label}
                </div>
            """


    @api.depends('employee_id.department_id')
    def _compute_employee_department_id(self):
        for record in self:
            record.employee_department_id = record.employee_id.department_id

    
    @api.onchange('config_id')
    def _onchange_config_id(self):
        if self.config_id:
            self.goal= self.config_id.goal
            self.weight = self.config_id.weight

    @api.onchange('odoo_goal_id')
    def _onchange_odoo_goal_id(self):
        if self.odoo_goal_id:
            self.weight = self.odoo_goal_id.weight
            #self.progression = 'Not started'
        else:
            self.weight = 0.0 

    @api.onchange('odoo_goal_id')
    def _onchange_odoo_goal_id(self):
        if self.odoo_goal_id:
            self.goal = self.odoo_goal_id.name
            self.weight = self.odoo_goal_id.weight
            # Optional if you want to pull more fields like status or progress
            self.results = f"Progress: {self.odoo_goal_id.progression or 'N/A'}"
        else:
            self.goal = ''
            self.weight = 0.0
            self.results = ''
            
    def action_refresh_progress(self):
        for rec in self:
            rec._compute_rating_scale()
            rec._compute_rating_label_html()
        return True
    
    score = fields.Float(string='Score', compute='_compute_score', store=True)

    @api.depends('weight', 'employee_self_rating', 'manager_rating')
    def _compute_score(self):
        for line in self:
            # emp_rating = float(line.employee_self_rating) if line.employee_self_rating else 0.0
            mgr_rating = float(line.manager_rating) if line.manager_rating else 0.0
            # avg_rating = (emp_rating + mgr_rating) / 2 if (emp_rating and mgr_rating) else 0.0
            line.score = line.weight * mgr_rating 

    def _onchange_employee_id(self):
        domain = {}
        current_employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)

        if current_employee:
            if self.env.user.has_group('una_hr_appraisal_advanced.group_hr_appraisal_employee'):
                domain['employee_id'] = [('id', '=', current_employee.id)]
            elif self.env.user.has_group('una_hr_appraisal_advanced.group_hr_team_appraisal_manager'):
                if current_employee.department_id:
                    domain['employee_id'] = [('department_id', '=', current_employee.department_id.id)]
            elif self.env.user.has_group('una_hr_appraisal_advanced.group_hr_appraisal_manager'):
                domain['employee_id'] = []  # or leave unset for full access
            if current_employee.department_id:
                domain['config_id'] = [('department_id', '=', current_employee.department_id.id)]

        return {'domain': domain}

class AppraisalStrategicObjectiveConfig(models.Model):
    _name = 'appraisal.strategic.objective.config'
    _description = 'Strategic Objective Configuration'

    name = fields.Char(required=True, string= 'Functional Objective')
    key_initiative_ids = fields.Many2many(
        comodel_name='appraisal.key.initiative',
        relation='rel_strategic_objective_key_initiative',
        column1='strategic_objective_id',
        column2='key_initiative_id',
        string='Key Initiatives',
)

    kpi_ids = fields.Many2many(
        comodel_name='appraisal.kpi',
        relation='rel_strategic_objective_kpi',
        column1='strategic_objective_id',
        column2='kpi_id',
        string='KPIs',
    )
    # key_initiative_ids = fields.Char(required=True, string = 'Key Initiatives')
    # kpi_ids = fields.Char(required=True)
    weight = fields.Float(string='Weight (70%)', required=True, default=0.0)
    department_id = fields.Many2one('hr.department', string='Department', default=lambda self: self._default_department_id())

    @api.model
    def _default_department_id(self):
        """Fetch the department of the logged-in user's employee."""
        user = self.env.user
        employee = self.env['hr.employee'].search([('user_id', '=', user.id)], limit=1)
        if employee and employee.department_id:
            return employee.department_id.id
        return None
   

class AppraisalBehavioralCompetencyConfig(models.Model):
    _name = 'appraisal.behavioral.competency.config'
    _description = 'Behavioral Competency Configuration'
    _rec_name = 'competency_name'
    competency_name = fields.Char(string = "Behavioral Competency", required=True)
    key_initiative_ids = fields.Char(required=True)
    kpi_ids = fields.Char(required=True)
    weight = fields.Float(string='Weight (20%)', required=True, default=0.0)
    department_id = fields.Many2one('hr.department', string='Department')

class AppraisalPersonalDevelopmentConfig(models.Model):
    _name = 'appraisal.personal.development.config'
    _description = 'Personal Development Goal Configuration'
    _rec_name = 'goal'

    goal = fields.Char(required=True)
    weight = fields.Float(string='Weight (%)', required=True, default=0.0)
    department_id = fields.Many2one('hr.department', string='Department')

class HrAppraisalGoal(models.Model):
    _inherit = 'hr.appraisal.goal'

    weight = fields.Float(string='Weight (%)', required=True, default=0.0)
    progress = fields.Float(string='Progress (%)', default=0.0)

    def write(self, vals):
        res = super().write(vals)
        if 'progress' in vals:
            for goal in self:
                related_dev_lines = self.env['hr.appraisal.personal.development'].search([
                    ('odoo_goal_id', '=', goal.id)
                ])
                related_dev_lines.write({'goal_progress_cache': goal.progress})
        return res

    # Optional: Manual sync method
    def action_sync_progress_to_personal_goals(self):
        for goal in self:
            related_dev_lines = self.env['hr.appraisal.personal.development'].search([
                ('odoo_goal_id', '=', goal.id)
            ])
            related_dev_lines.write({'goal_progress_cache': goal.progress})

    @api.depends('weight', 'progress')
    def _compute_score(self):
        for line in self:
            # Scale score from 0–100 progress to 0–5 rating, then multiply by weight
            progress_score = (line.goal_progress_cache / 10.0)  # 100% → 5
            line.score = line.weight * line.progress         