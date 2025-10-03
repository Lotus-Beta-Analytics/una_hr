from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class OnboardingUploadWizard(models.TransientModel):
    _name = 'onboarding.upload.wizard'
    _description = 'Upload Multiple Onboarding Documents'

  

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


    staff_number = fields.Char(string='Staff Number')
    pfa = fields.Char(string='PFA')
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
    # These are the readonly flags needed for your view logic
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
            emp = wizard.employee_id
            wizard.staff_number_readonly = bool(emp.staff_number)
            wizard.pfa_readonly = bool(emp.pfa)
            wizard.pfa_boolean_readonly = bool(emp.pfa_boolean)
            wizard.rsa_pin_readonly = bool(emp.rsa_pin)
            wizard.tin_readonly = bool(emp.tin)
            wizard.sort_code_readonly = bool(emp.sort_code)
            wizard.state_irs_readonly = bool(emp.state_irs)


    cv_attachment = fields.Many2many(
        'ir.attachment', 'wizard_onboarding_cv_rel', 'wizard_id', 'attachment_id',
        string="SELECT YOUR FILES TO UPLOAD"
    )
    cv_readonly = fields.Boolean(string="CV Readonly", compute="_compute_cv_readonly")

    @api.depends('employee_id')
    def _compute_cv_readonly(self):
        for wizard in self:
            wizard.cv_readonly = bool(wizard.employee_id.onboarding_cv_attachment_ids)
   

    medical_attachment = fields.Many2many(
        'ir.attachment', 'wizard_onboarding_medical_rel', 'wizard_id', 'attachment_id',
        string="SELECT YOUR FILES TO UPLOAD"
    )
    police_report_attachment = fields.Many2many(
        'ir.attachment', 'wizard_onboarding_police_report_rel', 'wizard_id', 'attachment_id',
        string="SELECT YOUR FILES TO UPLOAD"
    )
    credentials_attachment = fields.Many2many(
        'ir.attachment', 'wizard_onboarding_credentials_rel', 'wizard_id', 'attachment_id',
        string="SELECT YOUR FILES TO UPLOAD"
    )
    passport_photo_attachment = fields.Many2many(
        'ir.attachment', 'wizard_onboarding_passport_photo_rel', 'wizard_id', 'attachment_id',
        string="SELECT YOUR PROFILE PHOTO TO UPLOAD"
    )
    bond_ack_attachment = fields.Many2many(
        'ir.attachment', 'wizard_onboarding_bond_ack_rel', 'wizard_id', 'attachment_id',
        string="SELECT YOUR FILES TO UPLOAD"
    )
    loe_ack_attachment = fields.Many2many(
        'ir.attachment', 'wizard_onboarding_loe_ack_rel', 'wizard_id', 'attachment_id',
        string="SELECT YOUR FILES TO UPLOAD"
    )
    employment_form_attachment = fields.Many2many(
        'ir.attachment', 'wizard_onboarding_employment_form_rel', 'wizard_id', 'attachment_id',
        string="SELECT YOUR FILES TO UPLOAD"
    )
    background_attachment = fields.Many2many(
        'ir.attachment', 'wizard_onboarding_background_rel', 'wizard_id', 'attachment_id',
        string="SELECT YOUR FILES TO UPLOAD"
    )
    referees_attachment = fields.Many2many(
        'ir.attachment', 'wizard_onboarding_referees_rel', 'wizard_id', 'attachment_id',
        string="SELECT YOUR FILES TO UPLOAD"
    )
    licenses_attachment = fields.Many2many(
        'ir.attachment', 'wizard_onboarding_licenses_rel', 'wizard_id', 'attachment_id',
        string="SELECT YOUR FILES TO UPLOAD"
    )
    wace_attachment = fields.Many2many(
        'ir.attachment', 'wizard_onboarding_wace_rel', 'wizard_id', 'attachment_id',
        string="SELECT YOUR FILES TO UPLOAD"
    )
    neco_attachment = fields.Many2many(
        'ir.attachment', 'wizard_onboarding_neco_rel', 'wizard_id', 'attachment_id',
        string="SELECT YOUR FILES TO UPLOAD"
    )
    bsc_attachment = fields.Many2many(
        'ir.attachment', 'wizard_onboarding_bsc_rel', 'wizard_id', 'attachment_id',
        string="SELECT YOUR FILES TO UPLOAD"
    )
    msc_attachment = fields.Many2many(
        'ir.attachment', 'wizard_onboarding_msc_rel', 'wizard_id', 'attachment_id',
        string="SELECT YOUR FILES TO UPLOAD"
    )
    phd_attachment = fields.Many2many(
        'ir.attachment', 'wizard_onboarding_phd_rel', 'wizard_id', 'attachment_id',
        string="SELECT YOUR FILES TO UPLOAD"
    )
    documented_attachment = fields.Many2many(
        'ir.attachment', 'wizard_onboarding_documented_rel', 'wizard_id', 'attachment_id',
        string="SELECT YOUR FILES TO UPLOAD"
    )
    
    onboarding_uniforms = fields.Selection(
    [('yes', 'Yes'), ('no', 'No')],
    string="UNIFORMS ISSUED",
    tracking=True
)
    onboarding_id_card = fields.Selection(
    [('yes', 'Yes'), ('no', 'No')],
    string="ID CARD PRODUCED",
    tracking=True
)
    onboarding_account = fields.Selection(
    [('yes', 'Yes'), ('no', 'No')],
    string="ACCOUNT DETAILS WITH TIN AND RSA SUPPLIED",
    tracking=True
) 
    onboarding_tools = fields.Selection(
    [('yes', 'Yes'), ('no', 'No')],
    string="WORKING TOOLS PROVIDED (computer, desk etc)",
    tracking=True
)
   


    onboarding_handbook = fields.Selection(
    [('yes', 'Yes'), ('no', 'No')],
    string="HANDBOOK ACKNOWLEDGMENT COPY",
    tracking=True
)
    onboarding_email = fields.Selection(
    [('yes', 'Yes'), ('no', 'No')],
    string="EMAIL CREATION BY IT DEPARTMENT FROM HR",
    tracking=True
)
   
    def action_upload(self):
        employee = self.employee_id
        field_map = {
            'cv': ('cv_attachment', 'onboarding_cv_attachment_ids', 'onboarding_cv'),
            'medical': ('medical_attachment', 'onboarding_medical_attachment_ids', 'onboarding_medical'),
            'police_report': ('police_report_attachment', 'onboarding_police_report_attachment_ids', 'onboarding_police_report'),
            'credentials': ('credentials_attachment', 'onboarding_credentials_attachment_ids', 'onboarding_credentials'),
            'passport_photo': ('passport_photo_attachment', 'onboarding_passport_photo_attachment_ids', 'onboarding_passport_photo'),
            'bond_ack': ('bond_ack_attachment', 'onboarding_bond_ack_attachment_ids', 'onboarding_bond_ack'),
            'loe_ack': ('loe_ack_attachment', 'onboarding_loe_ack_attachment_ids', 'onboarding_loe_ack'),
            'employment_form': ('employment_form_attachment', 'onboarding_employment_form_attachment_ids', 'onboarding_employment_form'),
            'background': ('background_attachment', 'onboarding_background_check_attachment_ids', 'onboarding_background_check'),
            'referees': ('referees_attachment', 'onboarding_referees_attachment_ids', 'onboarding_referees'),
            'licenses': ('licenses_attachment', 'onboarding_licenses_attachment_ids', 'onboarding_licenses'),
            'wace': ('wace_attachment', 'onboarding_wace_attachment_ids', 'wace_attachment'),
            'neco': ('neco_attachment', 'onboarding_neco_attachment_ids', 'neco_attachment'),
            'bsc': ('bsc_attachment', 'onboarding_bsc_attachment_ids', 'bsc_attachment'),
            'msc': ('msc_attachment', 'onboarding_msc_attachment_ids', 'msc_attachment'),
            'phd': ('phd_attachment', 'onboarding_phd_attachment_ids', 'phd_attachment'),
            'documented': ('documented_attachment', 'onboarding_documented_attachment_ids', 'onboarding_documented'),
            
           
        }

        selection_fields = {
        'onboarding_email': self.onboarding_email,
        'onboarding_handbook': self.onboarding_handbook,
        'onboarding_tools': self.onboarding_tools,
        'onboarding_account': self.onboarding_account,
        'onboarding_id_card': self.onboarding_id_card,
        'onboarding_uniforms': self.onboarding_uniforms,
        'state_irs':self.state_irs,
        }

        custom_fields = {
        'pfa': self.pfa,
        'rsa_pin': self.rsa_pin,
        'tin': self.tin,
        'sort_code': self.sort_code,
        'staff_number': self.staff_number,
        }

        update_vals = {}
        uploaded_docs = []

        for doc_key, (wizard_field, emp_field, bool_field) in field_map.items():
            attachments = getattr(self, wizard_field)
            if attachments:
                # Link attachments to employee
                # Use (4, id) to add to many2many without removing old ones
                update_vals.setdefault(emp_field, [])
                for att in attachments:
                    update_vals[emp_field].append((4, att.id))
                update_vals[bool_field] = True
                uploaded_docs.append(doc_key.upper())
       
        if self.bank_account_id:
            update_vals['bank_account_id'] = self.bank_account_id.id
            uploaded_docs.append("BANK ACCOUNT")

        for field_name, value in custom_fields.items():
            if value:
                update_vals[field_name] = value
                uploaded_docs.append(field_name.replace('_', ' ').upper())

                # if field_name == "pfa":
                #             update_vals["pfa_boolean"] = True            
                

        for field_name, value in selection_fields.items():
            if value:
                update_vals[field_name] = value
                uploaded_docs.append(field_name.replace('_', ' ').upper())  
            
                   

          
        # SET EMPLOYEE AVATAR FROM PASSPORT PHOTO
        passport_photos = self.passport_photo_attachment
        if passport_photos:
            # Find the first image-type attachment
            image_attachment = next(
                (att for att in passport_photos if att.mimetype and 'image' in att.mimetype.lower()),
                None
            )

            # If no mimetype, assume first one is an image anyway (fallback)
            if not image_attachment:
                image_attachment = passport_photos[0]
                _logger.warning(f"Using first passport photo without mimetype: {image_attachment.name}")

            if image_attachment:
                update_vals['image_1920'] = image_attachment.datas
                uploaded_docs.append("AVATAR (FROM PASSPORT PHOTO)")
                _logger.info(f"✅ Set image_1920 for employee {employee.name} using {image_attachment.name}")
            else:
                _logger.warning(f"⚠️ No valid passport image found for {employee.name}")
      

        if update_vals:
            try:
                employee.write(update_vals)
                employee.onboarding_completed = True
            except Exception as e:
                _logger.error(f"Failed to update employee {employee.name}: {e}")
                raise UserError(_("Failed to update employee record: %s") % e)

        if not uploaded_docs:
            raise UserError(_("No documents were uploaded. Please select at least one document."))

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('You have Updated Successful'),
                'message': _('Documents uploaded: %s' % ', '.join(uploaded_docs)),
                'type': 'success',
                'next': {'type': 'ir.actions.act_window_close'}
            }
        }
    

    cv_attachment_status_html = fields.Html(
        string="CV Attachment Status",
        compute="_compute_cv_attachment_status",
        sanitize=True,
        readonly=True
    )

    @api.depends('cv_attachment')
    def _compute_cv_attachment_status(self):
        for rec in self:
            if  rec.employee_id.onboarding_cv_attachment_ids:
                rec.cv_attachment_status_html = """
                <div style="
                    background-color: #28a745;
                    color: white;
                    font-weight: bold;
                    padding: 4px 10px;
                    border-radius: 4px;
                    display: inline-block;
                ">UPLOADED</div>
                """
            else:
                rec.cv_attachment_status_html = "<div>Not Upload</div>"




   
    medical_attachment_status_html = fields.Html(string="Medical Report Status", compute="_compute_medical_attachment_status", sanitize=True, readonly=True)
    
    @api.depends('medical_attachment')
    def _compute_medical_attachment_status(self):
        for rec in self:
            if  rec.employee_id.onboarding_medical_attachment_ids:
                rec.medical_attachment_status_html = """
                <div style="
                    background-color: #28a745;
                    color: white;
                    font-weight: bold;
                    padding: 4px 10px;
                    border-radius: 4px;
                    display: inline-block;
                ">UPLOADED</div>
                """
            else:
                rec.medical_attachment_status_html = "<div>NOT UPLOAD</div>"

    police_report_attachment_status_html = fields.Html(string="Police Report Status", compute="_compute_POLICE_attachment_status", sanitize=True, readonly=True)
    
    @api.depends('police_report_attachment')
    def _compute_POLICE_attachment_status(self):
        for rec in self:
            if  rec.employee_id.onboarding_police_report_attachment_ids:
                rec.police_report_attachment_status_html = """
                <div style="
                    background-color: #28a745;
                    color: white;
                    font-weight: bold;
                    padding: 4px 10px;
                    border-radius: 4px;
                    display: inline-block;
                ">UPLOADED</div>
                """
            else:
                rec.police_report_attachment_status_html = "<div>NOT UPLOAD</div>"
    
    credentials_attachment_status_html = fields.Html(string="Credentials Status", compute="_compute_credentials_attachment_status", sanitize=True, readonly=True)
    
    @api.depends('credentials_attachment')
    def _compute_credentials_attachment_status(self):
        for rec in self:
            if  rec.employee_id.onboarding_credentials_attachment_ids:
                rec.credentials_attachment_status_html = """
                <div style="
                    background-color: #28a745;
                    color: white;
                    font-weight: bold;
                    padding: 4px 10px;
                    border-radius: 4px;
                    display: inline-block;
                ">UPLOADED</div>
                """
            else:
                rec.credentials_attachment_status_html = "<div>NOT UPLOAD</div>"
    passport_photo_attachment_status_html = fields.Html(string="Passport Photo Status", compute="_compute_passport_attachment_status", sanitize=True, readonly=True)
      
    @api.depends('passport_photo_attachment')
    def _compute_passport_attachment_status(self):
        for rec in self:
            if  rec.employee_id.onboarding_passport_photo_attachment_ids:
                rec.passport_photo_attachment_status_html = """
                <div style="
                    background-color: #28a745;
                    color: white;
                    font-weight: bold;
                    padding: 4px 10px;
                    border-radius: 4px;
                    display: inline-block;
                ">UPLOADED</div>
                """
            else:
                rec.passport_photo_attachment_status_html  = "<div>NOT UPLOAD</div>"
    bond_ack_attachment_status_html = fields.Html(string="Bond Acknowledgment Status", compute="_compute_bond_attachment_status", sanitize=True, readonly=True)
    
    @api.depends('bond_ack_attachment')
    def _compute_bond_attachment_status(self):
        for rec in self:
            if  rec.employee_id.onboarding_bond_ack_attachment_ids:
                rec.bond_ack_attachment_status_html = """
                <div style="
                    background-color: #28a745;
                    color: white;
                    font-weight: bold;
                    padding: 4px 10px;
                    border-radius: 4px;
                    display: inline-block;
                ">UPLOADED</div>
                """
            else:
                rec.bond_ack_attachment_status_html  = "<div>NOT UPLOAD</div>"
    loe_ack_attachment_status_html = fields.Html(string="NOT UPLOAD", compute="_compute_loe_attachment_status", sanitize=True, readonly=True)
    
    @api.depends('loe_ack_attachment')
    def _compute_loe_attachment_status(self):
        for rec in self:
            if  rec.employee_id.onboarding_loe_ack_attachment_ids:
                rec.loe_ack_attachment_status_html = """
                <div style="
                    background-color: #28a745;
                    color: white;
                    font-weight: bold;
                    padding: 4px 10px;
                    border-radius: 4px;
                    display: inline-block;
                ">UPLOADED</div>
                """
            else:
                rec.loe_ack_attachment_status_html  = "<div>NOT UPLOAD</div>"
    employment_form_attachment_status_html = fields.Html(string="Employment Form Status", compute="_compute_employee_form_attachment_status", sanitize=True, readonly=True)
    @api.depends('employment_form_attachment')
    def _compute_employee_form_attachment_status(self):
        for rec in self:
            if  rec.employee_id.onboarding_employment_form_attachment_ids:
                rec.employment_form_attachment_status_html = """
                <div style="
                    background-color: #28a745;
                    color: white;
                    font-weight: bold;
                    padding: 4px 10px;
                    border-radius: 4px;
                    display: inline-block;
                ">UPLOADED</div>
                """
            else:
                rec.employment_form_attachment_status_html  = "<div>NOT UPLOAD</div>"

                
    background_attachment_status_html = fields.Html(string="Background Check Status", compute="_compute_background_Check_attachment_status", sanitize=True, readonly=True)
    
    @api.depends('background_attachment')
    def _compute_background_Check_attachment_status(self):
        for rec in self:
            if  rec.employee_id.onboarding_background_check_attachment_ids:
                rec.background_attachment_status_html = """
                <div style="
                    background-color: #28a745;
                    color: white;
                    font-weight: bold;
                    padding: 4px 10px;
                    border-radius: 4px;
                    display: inline-block;
                ">UPLOADED</div>
                """
            else:
                rec.background_attachment_status_html  = "<div>NOT UPLOAD</div>"
    referees_attachment_status_html = fields.Html(string="Referees Form Status", compute="_compute_Referees_Form_attachment_status", sanitize=True, readonly=True)
    @api.depends('referees_attachment')
    def _compute_Referees_Form_attachment_status(self):
        for rec in self:
            if  rec.employee_id.onboarding_referees_attachment_ids:
                rec.referees_attachment_status_html = """
                <div style="
                    background-color: #28a745;
                    color: white;
                    font-weight: bold;
                    padding: 4px 10px;
                    border-radius: 4px;
                    display: inline-block;
                ">UPLOADED</div>
                """
            else:
                rec.referees_attachment_status_html  = "<div>NOT UPLOAD</div>"
   
    licenses_attachment_status_html = fields.Html(string="Licenses Status", compute="_compute_license_attachment_status", sanitize=True, readonly=True)
    @api.depends('licenses_attachment')
    def _compute_license_attachment_status(self):
        for rec in self:
            if  rec.employee_id.onboarding_licenses_attachment_ids:
                rec.licenses_attachment_status_html = """
                <div style="
                    background-color: #28a745;
                    color: white;
                    font-weight: bold;
                    padding: 4px 10px;
                    border-radius: 4px;
                    display: inline-block;
                ">UPLOADED</div>
                """
            else:
                rec.licenses_attachment_status_html = "<div>NOT UPLOAD</div>"
    
    wace_attachment_status_html = fields.Html(string="WAEC Status", compute="_compute_waec_attachment_status", sanitize=True, readonly=True)

    @api.depends('wace_attachment')
    def _compute_waec_attachment_status(self):
        for rec in self:
            if  rec.employee_id.onboarding_wace_attachment_ids:
                rec.wace_attachment_status_html = """
                <div style="
                    background-color: #28a745;
                    color: white;
                    font-weight: bold;
                    padding: 4px 10px;
                    border-radius: 4px;
                    display: inline-block;
                ">UPLAODED</div>
                """
            else:
                rec.wace_attachment_status_html = "<div>NOT UPLOAD</div>"
    # neco_attachment_status_html = fields.Html(string="NECO Status", compute="_compute_all_status_html", sanitize=True, readonly=True)
    bsc_attachment_status_html = fields.Html(string="BSc Status", compute="_compute_bsc_attachment_status", sanitize=True, readonly=True)
   
    @api.depends('bsc_attachment')
    def _compute_bsc_attachment_status(self):
        for rec in self:
            if  rec.employee_id.onboarding_bsc_attachment_ids:
                rec.bsc_attachment_status_html  = """
                <div style="
                    background-color: #28a745;
                    color: white;
                    font-weight: bold;
                    padding: 4px 10px;
                    border-radius: 4px;
                    display: inline-block;
                ">UPLOADED</div>
                """
            else:
                rec.bsc_attachment_status_html = "<div>NOT UPLOAD</div>"
    msc_attachment_status_html = fields.Html(string="MSc Status", compute="_compute_msc_attachment_status", sanitize=True, readonly=True)
    
    @api.depends('msc_attachment')
    def _compute_msc_attachment_status(self):
        for rec in self:
            if  rec.employee_id.onboarding_msc_attachment_ids:
                rec.msc_attachment_status_html  = """
                <div style="
                    background-color: #28a745;
                    color: white;
                    font-weight: bold;
                    padding: 4px 10px;
                    border-radius: 4px;
                    display: inline-block;
                ">UPLOADED</div>
                """
            else:
                rec.msc_attachment_status_html = "<div>NOT UPLOAD</div>"
    phd_attachment_status_html = fields.Html(string="PhD Status", compute="_compute_phd_attachment_status", sanitize=True, readonly=True)
    @api.depends('phd_attachment')
    def _compute_phd_attachment_status(self):
        for rec in self:
            if  rec.employee_id.onboarding_phd_attachment_ids:
                rec.phd_attachment_status_html  = """
                <div style="
                    background-color: #28a745;
                    color: white;
                    font-weight: bold;
                    padding: 4px 10px;
                    border-radius: 4px;
                    display: inline-block;
                ">UPLOADED</div>
                """
            else:
                rec.phd_attachment_status_html = "<div>NOT UPLOAD</div>"

    documented_attachment_status_html = fields.Html(string="Documented Forms Status", compute="_compute_doc_attachment_status", sanitize=True, readonly=True)
    @api.depends('documented_attachment')
    def _compute_doc_attachment_status(self):
        for rec in self:
            if  rec.employee_id.onboarding_documented_attachment_ids:
                rec.documented_attachment_status_html  = """
                <div style="
                    background-color: #28a745;
                    color: white;
                    font-weight: bold;
                    padding: 4px 10px;
                    border-radius: 4px;
                    display: inline-block;
                ">UPLOADED</div>
                """
            else:
                rec.documented_attachment_status_html = "<div>NOT UPLOAD</div>"
  
