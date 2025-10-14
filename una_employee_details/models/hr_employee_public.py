# models/hr_employee_public.py

from odoo import models, fields,api, _

class HrEmployeePublic(models.Model):
    _inherit = 'hr.employee.public'

    employee_id = fields.Many2one(
        'hr.employee',
        string="New Staff Name",
        required=True,
        ondelete='cascade',
        default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
    )

    bank_account_id = fields.Many2one(
        'res.partner.bank',
        string="Bank Account",
        domain="[('partner_id', '=', partner_id)]",
        context="{'default_partner_id': partner_id}",
        options="{'no_quick_create': True}"
    )

    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        compute='_compute_partner_id',
        store=False
    )

    address_home_id = fields.Many2one(
    'res.partner',
    string='Private Address',
    help='Enter here the private address of the employee, not the one linked to your company.'
)


    @api.depends('employee_id')
    def _compute_partner_id(self):
        for wizard in self:
            wizard.partner_id = wizard.employee_id.address_home_id

    # def action_update_bank_account(self):
    #     if self.bank_account_id and self.employee_id:
    #         self.employee_id.bank_account_id = self.bank_account_id

    staff_number = fields.Char(string='Staff Number')
    pfa = fields.Char(string='PFA')
    pfa_boolean = fields.Boolean(stringn='PFA Submitted', default =False)
    rsa_pin = fields.Char(string='RSA PIN')
    tin = fields.Char(string='TIN PIN')
    sort_code = fields.Char(string='Sort Code')
    state_irs = fields.Selection([
        ('abia', 'Abia'),
        ('adamawa', 'Adamawa'),
        ('akwa ibom', 'Akwa Ibom'),
        ('anambra', 'Anambra'),
        ('bauchi', 'Bauchi'),
        ('bayelsa', 'Bayelsa'),
        ('benin', 'Benin'),
        ('benue', 'Benue'),
        ('borno', 'Borno'),
        ('cross river', 'Cross River'),
        ('delta', 'Asaba'),
        ('ebonyi', 'Ebonyi'),
        ('edo', 'Edo'),
        ('ekiti', 'Ekiti'),
        ('enugu', 'Enugu'),
        ('gombe', 'Gombe'),
        ('imo', 'Imo'),
        ('jigawa', 'Jigawa'),
        ('kaduna', 'Kaduna'),
        ('kano', 'Kano'),
        ('katsina', 'Katsina'),
        ('kogi', 'Kogi'),
        ('kwara', 'Kwara'),
        ('lagos', 'Lagos'),
        ('nasarawa', 'Nasarawa'),
        ('niger', 'Niger'),
        ('ogun', 'Ogun'),
        ('ondo', 'Ondo'),
        ('osun', 'Osun'),
        ('osubi', 'Osubi'),
        ('owerri', 'Owerri'),
        ('oyo', 'Oyo'),
        ('plateau', 'Plateau'),
        ('phc', 'PHC'),
        ('rivers', 'Rivers'),
        ('sokoto', 'Sokoto'),
        ('taraba', 'Taraba'),
        ('yobe', 'Yobe'),
        ('zamfara', 'Zamfara'),
        ('fct', 'FCT'),
    ], string='State IRS')

    mobile_phone = fields.Char(string='Work Mobile', store=True)
    work_phone= fields.Char(string='Work Phone', store=True)


    staff_number_readonly = fields.Boolean(compute='_compute_readonly_fields')
    pfa_readonly = fields.Boolean(compute='_compute_readonly_fields')
    pfa_boolean_readonly = fields.Boolean(compute='_compute_readonly_fields')
    rsa_pin_readonly = fields.Boolean(compute='_compute_readonly_fields')
    tin_readonly = fields.Boolean(compute='_compute_readonly_fields')
    sort_code_readonly = fields.Boolean(compute='_compute_readonly_fields')
    state_irs_readonly = fields.Boolean(compute='_compute_readonly_fields')

    @api.depends('employee_id')
    def _compute_readonly_fields(self):
        for wizard in self:
            employee = wizard.employee_id
            wizard.staff_number_readonly = bool(employee.staff_number)
            wizard.pfa_readonly = bool(employee.pfa)
            wizard.pfa_boolean_readonly = bool(employee.pfa_boolean)
            wizard.rsa_pin_readonly = bool(employee.rsa_pin)
            wizard.tin_readonly = bool(employee.tin)
            wizard.sort_code_readonly = bool(employee.sort_code)
            wizard.state_irs_readonly = bool(employee.state_irs)


    onboarding_cv_attachment_ids = fields.Many2many(
        comodel_name='ir.attachment',
        related='employee_id.onboarding_cv_attachment_ids',
        readonly=True
    )
    onboarding_loe_ack_attachment_ids = fields.Many2many(
        comodel_name='ir.attachment',
        related='employee_id.onboarding_loe_ack_attachment_ids',
        readonly=True
    )
    onboarding_bond_ack_attachment_ids = fields.Many2many(
        comodel_name='ir.attachment',
        related='employee_id.onboarding_bond_ack_attachment_ids',
        readonly=True
    )
    onboarding_background_check_attachment_ids = fields.Many2many(
        comodel_name='ir.attachment',
        related='employee_id.onboarding_background_check_attachment_ids',
        readonly=True
    )
    onboarding_police_report_attachment_ids = fields.Many2many(
        comodel_name='ir.attachment',
        related='employee_id.onboarding_police_report_attachment_ids',
        readonly=True
    )
    onboarding_medical_attachment_ids = fields.Many2many(
        comodel_name='ir.attachment',
        related='employee_id.onboarding_medical_attachment_ids',
        readonly=True
    )
    onboarding_employment_form_attachment_ids = fields.Many2many(
        comodel_name='ir.attachment',
        related='employee_id.onboarding_employment_form_attachment_ids',
        readonly=True
    )
    onboarding_passport_photo_attachment_ids = fields.Many2many(
        comodel_name='ir.attachment',
        related='employee_id.onboarding_passport_photo_attachment_ids',
        readonly=True
    )
    onboarding_credentials_attachment_ids = fields.Many2many(
        comodel_name='ir.attachment',
        related='employee_id.onboarding_credentials_attachment_ids',
        readonly=True
    )

    
    onboarding_documented_attachment_ids = fields.Many2many(
        comodel_name='ir.attachment',
        related='employee_id.onboarding_documented_attachment_ids',
        readonly=True
    )
    
    onboarding_licenses_attachment_ids = fields.Many2many(
        comodel_name='ir.attachment',
        related='employee_id.onboarding_licenses_attachment_ids',
        readonly=True
    )
    onboarding_referees_attachment_ids = fields.Many2many(
        comodel_name='ir.attachment',
        related='employee_id.onboarding_referees_attachment_ids',
        readonly=True
    )

    onboarding_licenses_attachment_ids = fields.Many2many(
        comodel_name='ir.attachment',
        related='employee_id.onboarding_licenses_attachment_ids',
        readonly=True
    )

        # WACE
    onboarding_wace_attachment_ids = fields.Many2many(
        comodel_name='ir.attachment',
        related='employee_id.onboarding_wace_attachment_ids',
        readonly=True
)
    onboarding_wace_status_html = fields.Html(compute='_compute_credentials_status_html', sanitize=True)

    # NECO
    onboarding_neco_attachment_ids = fields.Many2many(
        
        comodel_name='ir.attachment',
        related='employee_id.onboarding_neco_attachment_ids',
        readonly=True
    )
    onboarding_neco_status_html = fields.Html(compute='_compute_credentials_status_html', sanitize=True)

    # BSc
    onboarding_bsc_attachment_ids = fields.Many2many(
        comodel_name='ir.attachment',
        related='employee_id.onboarding_bsc_attachment_ids',
        readonly=True
    )
    onboarding_bsc_status_html = fields.Html(compute='_compute_credentials_status_html', sanitize=True)

    # MSc
    onboarding_msc_attachment_ids = fields.Many2many(
        comodel_name='ir.attachment',
        related='employee_id.onboarding_msc_attachment_ids',
        readonly=True
    )
    onboarding_msc_status_html = fields.Html(compute='_compute_credentials_status_html', sanitize=True)

    # PhD
    onboarding_phd_attachment_ids = fields.Many2many(
        comodel_name='ir.attachment',
        related='employee_id.onboarding_phd_attachment_ids',
        readonly=True
    )
    onboarding_phd_status_html = fields.Html(compute='_compute_credentials_status_html', sanitize=True)


    onboarding_documented_attachment_ids= fields.Many2many(
        comodel_name='ir.attachment',
        related='employee_id.onboarding_documented_attachment_ids',
        readonly=True)
   

    onboarding_loe_ack = fields.Boolean(related='employee_id.onboarding_loe_ack', readonly=True)
    onboarding_loe_ack_remarks = fields.Char(related='employee_id.onboarding_loe_ack_remarks', readonly=True)
    # processed_by = fields.Many2one('res.users', related='employee_id.processed_by', readonly=True)
    # admin_dept = fields.Char(related='employee_id.admin_dept', readonly=True)

    onboarding_bond_ack = fields.Boolean(related='employee_id.onboarding_bond_ack', readonly=True)
    onboarding_bond_ack_remarks = fields.Char(related='employee_id.onboarding_bond_ack_remarks', readonly=True)
    onboarding_background_check = fields.Boolean(related='employee_id.onboarding_background_check', readonly=True)
    onboarding_background_check_remarks = fields.Char(related='employee_id.onboarding_background_check_remarks', readonly=True)
    onboarding_police_report = fields.Boolean(related='employee_id.onboarding_police_report', readonly=True)
    onboarding_police_report_remarks = fields.Char(related='employee_id.onboarding_police_report_remarks', readonly=True)
    onboarding_medical = fields.Boolean(related='employee_id.onboarding_medical', readonly=True)
    onboarding_medical_remarks = fields.Char(related='employee_id.onboarding_medical_remarks', readonly=True)
    onboarding_employment_form = fields.Boolean(related='employee_id.onboarding_employment_form', readonly=True)
    onboarding_employment_form_remarks = fields.Char(related='employee_id.onboarding_employment_form_remarks', readonly=True)
    onboarding_passport_photo = fields.Boolean(related='employee_id.onboarding_passport_photo', readonly=True)
    onboarding_passport_photo_remarks = fields.Char(related='employee_id.onboarding_passport_photo_remarks', readonly=True)
    onboarding_credentials = fields.Boolean(related='employee_id.onboarding_credentials', readonly=True)
    onboarding_credentials_remarks = fields.Char(related='employee_id.onboarding_credentials_remarks', readonly=True)
    onboarding_documented = fields.Boolean(related='employee_id.onboarding_documented', readonly=True)
    onboarding_documented_remarks = fields.Char(related='employee_id.onboarding_documented_remarks', readonly=True)
    onboarding_id_card = fields.Selection(
    [('yes', 'Yes'), ('no', 'No')],
    string="ID CARD PRODUCED",
    tracking=True
)
    onboarding_id_card_remarks = fields.Char(related='employee_id.onboarding_id_card_remarks', readonly=True)
    onboarding_uniforms = fields.Selection([('yes', 'Yes'), ('no', 'No')],
    string="UNIFORMS ISSUED",
    tracking=True
)
    onboarding_uniforms_remarks = fields.Char(related='employee_id.onboarding_uniforms_remarks', readonly=True)
    onboarding_referees = fields.Boolean(related='employee_id.onboarding_referees', readonly=True)
    onboarding_referees_remarks = fields.Char(related='employee_id.onboarding_referees_remarks', readonly=True)
    onboarding_licenses = fields.Boolean(related='employee_id.onboarding_licenses', readonly=True)
    onboarding_licenses_remarks = fields.Char(related='employee_id.onboarding_licenses_remarks', readonly=True)
    onboarding_cv = fields.Boolean(related='employee_id.onboarding_cv', readonly=True)
    onboarding_cv_remarks = fields.Char(related='employee_id.onboarding_cv_remarks', readonly=True)
    # onboarding_account = fields.Boolean(related='employee_id.onboarding_account', readonly=True)
    onboarding_account_remarks = fields.Char(related='employee_id.onboarding_account_remarks', readonly=True)
    # onboarding_tools = fields.Boolean(related='employee_id.onboarding_tools', readonly=True)
    onboarding_tools_remarks = fields.Char(related='employee_id.onboarding_tools_remarks', readonly=True)
    # onboarding_handbook = fields.Boolean(related='employee_id.onboarding_handbook', readonly=True)

    onboarding_account  = fields.Selection(
    [('yes', 'Yes'), ('no', 'No')],
    string="ACCOUNT DETAILS WITH TIN AND RSA SUPPLIED",
    tracking=True
)
    onboarding_tools  = fields.Selection(
    [('yes', 'Yes'), ('no', 'No')],
    string="WORKING TOOLS PROVIDED (computer, desk etc)",
    tracking=True
) 
    onboarding_handbook = fields.Selection(
    [('yes', 'Yes'), ('no', 'No')],
    string="HANDBOOK ACKNOWLEDGMENT COPY",
    tracking=True
)
    onboarding_handbook_remarks = fields.Char(related='employee_id.onboarding_handbook_remarks', readonly=True)
    # onboarding_email = fields.Boolean(related='employee_id.onboarding_email', readonly=True)
    onboarding_email = fields.Selection(
    [('yes', 'Yes'), ('no', 'No')],
    string="EMAIL CREATION BY IT DEPARTMENT FROM HR",
    tracking=True
)
    onboarding_email_remarks = fields.Char(related='employee_id.onboarding_email_remarks', readonly=True)
    copies_recieved_from = fields.Many2one(
        'res.users',
        related='employee_id.copies_recieved_from',
        readonly=True
    )
    station_office = fields.Many2one(
        'res.users',
        related='employee_id.station_office',
        readonly=True
    )
    it_dept = fields.Many2one(
        'res.users',
        related='employee_id.it_dept',
        readonly=True
    )
    admin_dept = fields.Many2one(
        'res.users',
        related='employee_id.admin_dept',
        readonly=True
    )
    processed_by = fields.Many2one(
        'res.users',
        related='employee_id.processed_by',
        readonly=True
    )
    checked_by = fields.Many2one(
        'res.users',
        related='employee_id.checked_by',
        readonly=True
    )
    hrm_head = fields.Many2one(
        'res.users',
        related='employee_id.hrm_head',
        readonly=True
    )

   