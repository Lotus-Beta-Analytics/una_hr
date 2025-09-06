from odoo import models, fields, api,_, exceptions
import logging
_logger = logging.getLogger(__name__)
from odoo.exceptions import ValidationError

class EmployeeTicketRequest(models.Model):
    _name = 'employee.ticket.request'
    _description = 'Employee Ticket Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    

    name = fields.Char(string='Request Reference', required=True, copy=False, default='New')
    employee_id = fields.Many2one('hr.employee', 
                                  string='STAFF NAME:',
                                    required=True, default=lambda self: self.env.user.employee_id)
    email = fields.Char(
            string="EMAIL ADDRESS: ",
            related='employee_id.work_email',
            store=True,
            readonly=True
        )
    mobile = fields.Char(
        string="MOBILE NUMBER",
        related='employee_id.mobile_phone',
        store=True,
        readonly=True
    )
    call_relationship = fields.Selection(
        selection=[
            ('mother', 'Mother'),
            ('father', 'Father'),
            ('son', 'Son'),
            ('daughter', 'Daughter'),
            ('brother', 'Brother'),
            ('sister', 'Sister'),
            ('others', 'Others'),
            ('wife','Wife'),
            ('husband','Husband')
        ],
        string='Passager Relationship',
        store=True
        
    )
    outbound_trip = fields.Text(string="FIRST LEG TRIP DETAILS: ",store=True)
    inbound_trip = fields.Text(string="SECOND LEG TRIP DETAILS: ",store=True)


    work_location = fields.Char(
        string="WORK LOCATION: ",
        related='employee_id.work_location_id.name',
        store=True,
        readonly=True
    )
    department_id = fields.Many2one(related='employee_id.department_id', store=True, string ='DEPARTMENT:')
    pax_name = fields.Char(string="Name of Pax")
    proposed_itinerary = fields.Text(string="PROPOSED INTENARY")
    travel_date = fields.Date(string='DATE OF TRAVEL', required=True, store=True)
    return_date = fields.Date(string='RETURN DATE', store=True)
    purpose = fields.Text(string='PURPOSE/DESCRIPTION OF REQUEST: ')
    pnr = fields.Char(string="Booking Reference [PNR]")
    state = fields.Selection([
        ('draft', 'Pending Submission'),
        ('line_manager', 'Pending Manager Approval'),
        ('hr_team', 'Pending HR Team Approval'),
        ('cco', 'Pending CCO Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='Status', default='draft', tracking=True)
    request_date = fields.Datetime(string='DATE OF REQUEST:', default=fields.Datetime.now)
    ticket_issued = fields.Boolean(string='Ticket Issued', default=False)
    approved_ticket_count = fields.Integer(
        string='Approved Tickets',
        related='employee_id.ticket_approved_count',
        store=False,
        readonly=True
    )
    approved_ticket_count = fields.Integer(related='employee_id.ticket_approved_count')
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
   
    department_id = fields.Many2one(
        'hr.department',
        string="DEPARTMENT",
        compute='_compute_line_manager_and_department',
        store=True
    )
    line_manager_id = fields.Many2one(
        'hr.employee',
        string="Name of Line Manager: ",
        compute='_compute_line_manager_and_department',
        store=True
    )

    ticket_approved_count = fields.Integer(
        string="Total No Of Approved Tickets",
        related='employee_id.ticket_approved_count',
        readonly=True,
        store=False,
    )


    state_summary = fields.Char(string="State Summary", compute="_compute_state_summary", store=False)

    ticket_count = fields.Integer(string='Ticket Count', compute='_compute_ticket_count', store=True)
    # used_ticket_count = sum(t.ticket_count for t in tickets_used)

    duration = fields.Integer(string='Duration (Days)', compute='_compute_duration', store=True)
    # requested_ticket_count = 2  
    
    

    @api.depends('travel_date', 'return_date')
    def _compute_duration(self):
        for rec in self:
            if rec.travel_date and rec.return_date:
                delta = rec.return_date - rec.travel_date
                if delta.days < 0:
                    raise ValidationError("Return Date cannot be before Travel Date.")
                rec.duration = delta.days + 1  
            else:
                rec.duration = 0


    @api.depends('outbound_trip', 'inbound_trip')
    def _compute_ticket_count(self):
        for rec in self:
            has_outbound = bool(rec.outbound_trip and rec.outbound_trip.strip())
            has_inbound = bool(rec.inbound_trip and rec.inbound_trip.strip())

            if has_outbound and has_inbound:
                rec.ticket_count = 2
            elif has_outbound or has_inbound:
                rec.ticket_count = 1
            else:
                rec.ticket_count = 0

            
    @api.constrains('outbound_trip', 'inbound_trip')
    def _check_trip_leg_presence(self):
        for rec in self:
            if not (rec.outbound_trip or rec.inbound_trip):
                raise ValidationError(_("Please provide at least one trip leg (outbound or inbound)."))
                    

    def action_mark_to_draft(self):
        for rec in self:
            old_state = rec.state
            rec.state = 'draft'
            rec.message_post(
                body=f"Ticket request was reset from <b>{old_state}</b> to <b>Draft</b> by {self.env.user.name}.",
                subtype_id=self.env.ref('mail.mt_note').id
            )

    @api.depends('state')
    def _compute_state_summary(self):
        status_dict = {
            'draft': 'Awaiting submission',
            'line_manager': 'Waiting for Line Manager approval',
            'hr_team': 'Pending HR Team Approval',
            'cco': 'Pending CCO approval',
            'approved': 'Approved and Ticket Issued',
            'rejected': 'Request was rejected'
        }
        for rec in self:
            rec.state_summary = status_dict.get(rec.state, 'Unknown')

    @api.depends('employee_id.ticket_request_ids.state', 'employee_id.ticket_request_ids.ticket_count')
    def _compute_ticket_approved_count(self):
        for rec in self:
            approved = rec.employee_id.ticket_request_ids.filtered(lambda r: r.state == 'approved')
            rec.ticket_approved_count = sum(r.ticket_count for r in approved)

        


    @api.depends('employee_id')
    def _compute_line_manager_and_department(self):
        for record in self:
            record.line_manager_id = record.employee_id.parent_id if record.employee_id else False
            record.department_id = record.employee_id.department_id if record.employee_id else False

    @api.model
    def create(self, vals):
        employee = self.env['hr.employee'].browse(vals.get('employee_id'))
        current_year = fields.Date.today().year

        # ✅ Safely coerce to string and strip to avoid crash
        outbound = str(vals.get('outbound_trip') or '').strip()
        inbound = str(vals.get('inbound_trip') or '').strip()

        has_outbound = bool(outbound)
        has_inbound = bool(inbound)

        if has_outbound and has_inbound:
            requested_ticket_count = 2
        elif has_outbound or has_inbound:
            requested_ticket_count = 1
        else:
            raise ValidationError(_("Please provide at least one trip leg (outbound or inbound)."))

        tickets_used = self.env['employee.ticket.request'].search([
            ('employee_id', '=', employee.id),
            ('state', '=', 'approved'),
            ('travel_date', '>=', f'{current_year}-01-01'),
            ('travel_date', '<=', f'{current_year}-12-31')
        ])
        used_ticket_count = sum(t.ticket_count for t in tickets_used)

        if (used_ticket_count + requested_ticket_count) > (employee.ticket_limit * 2):
            raise ValidationError(_(
                "Ticket request exceeds annual limit of %d tickets (%d round trips)."
            ) % (employee.ticket_limit * 2, employee.ticket_limit))

        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('employee.ticket.request') or 'New'

        return super().create(vals)



    def action_submit(self):
        for rec in self:
            current_year = fields.Date.today().year

            tickets_used = self.env['employee.ticket.request'].search([
                ('employee_id', '=', rec.employee_id.id),
                ('state', '=', 'approved'),
                ('travel_date', '>=', f'{current_year}-01-01'),
                ('travel_date', '<=', f'{current_year}-12-31')
            ])
            used_ticket_count = sum(t.ticket_count for t in tickets_used)  # ✅ added this

            # ✅ enforce ticket_limit * 2 rule
            if (used_ticket_count + rec.ticket_count) > (rec.employee_id.ticket_limit * 2):
                raise ValidationError(_(
                    "Submission blocked: %s has already reached the annual ticket limit of %d tickets (%d round trips)."
                ) % (rec.employee_id.name, rec.employee_id.ticket_limit * 2, rec.employee_id.ticket_limit))

            rec.state = 'line_manager'

            rec.message_post(
                body="Ticket request submitted. Awaiting Line Manager's approval.",
                subtype_id=self.env.ref('mail.mt_note').id
            )

            # Email notification to line manager
            template = self.env.ref(
                'una_employee_ticket_request.mail_template_ticket_request_submitted',
                raise_if_not_found=False
            )
            if template and rec.line_manager_id and rec.line_manager_id.work_email:
                try:
                    template.send_mail(rec.id, force_send=True)
                    rec.message_post(
                        body=f"Email notification sent to Line Manager: {rec.line_manager_id.name} "
                             f"({rec.line_manager_id.work_email}).",
                        subtype_id=self.env.ref('mail.mt_note').id
                    )
                except Exception as e:
                    _logger.warning("Failed to send submission email to Line Manager %s: %s", rec.line_manager_id.name, e)
                    rec.message_post(
                        body=f"⚠️ Failed to send email to Line Manager: {rec.line_manager_id.name}.",
                        subtype_id=self.env.ref('mail.mt_note').id
                    )
                    
        
    def action_approve_manager(self):
        for rec in self:
            rec.state = 'hr_team'
            rec.message_post(
                body="Ticket request approved by Line Manager. Forwarded to HR Team.",
                subtype_id=self.env.ref('mail.mt_note').id
            )
            template = self.env.ref(
                'una_employee_ticket_request.mail_template_ticket_request_manager_approved',
                raise_if_not_found=False
            )
            if template:
                try:
                    template.send_mail(rec.id, force_send=True)
                    rec.message_post(
                        body="Email notification sent to CCO for final approval.",
                        subtype_id=self.env.ref('mail.mt_note').id
                    )
                except Exception as e:
                    _logger.warning("Failed to send manager approval email to CCO: %s", e)
                    rec.message_post(
                        body="⚠️ Failed to send email to CCO after Line Manager approval.",
                        subtype_id=self.env.ref('mail.mt_note').id
                    )


    def action_approve_hr_team(self):
        template = self.env.ref('una_employee_ticket_request.mail_template_ticket_request_hr_approved', raise_if_not_found=False)
        cco_group = self.env.ref('una_employee_ticket_request.group_ticket_approval_cco', raise_if_not_found=False)

        for rec in self:
            # Update state
            rec.state = 'cco'

            # Post internal message to chatter
            rec.message_post(
                body="Ticket request approved by HR Team and notification sent to CCO team for further approval.",
                subtype_id=self.env.ref('mail.mt_note').id
            )

            # Send email if template and group are valid
            if not template:
                raise UserError("Email template 'mail_template_ticket_request_hr_approved' not found.")
            if not cco_group:
                raise UserError("CCO approval group not found.")

            # Get one user in the group who has an email
            cco_user = next((user for user in cco_group.users if user.email), None)
            if not cco_user:
                raise UserError("No user with a valid email found in the CCO approval group.")

            try:
                # Send email using template
                template.with_context(
                    cco_email=cco_user.email,
                    lang=rec.employee_id.user_id.lang if rec.employee_id.user_id else 'en_US',
                ).send_mail(rec.id, force_send=True)

                # Optionally log email in chatter
                rec.message_post(
                    body=f"Approval email sent to CCO ({cco_user.email}).",
                    subtype_id=self.env.ref('mail.mt_note').id
                )
            except Exception as e:
                _logger.warning(f"Failed to send approval email to CCO: {e}")
                rec.message_post(
                    body="Failed to send email to CCO team. Please check email configuration.",
                    subtype_id=self.env.ref('mail.mt_note').id
                )
                

                
    
    def action_approve_cco(self):
        for rec in self:
            rec.state = 'approved'
            rec.ticket_issued = True
            rec.employee_id.tickets_used_this_year += rec.ticket_count

            if rec.employee_id.tickets_used_this_year >= rec.employee_id.ticket_limit:
                rec.message_post(
                    body=_("You have reached your annual ticket request limit."),
                    subtype_id=self.env.ref('mail.mt_comment').id
                )
            template = self.env.ref(
                'una_employee_ticket_request.mail_template_ticket_request_approved',  # Replace with your actual module/template ID
                raise_if_not_found=False
            )
            if template:
                try:
                    template.send_mail(rec.id, force_send=True)
                    rec.message_post(
                        body=f"Ticket request approved and email sent to {rec.employee_id.name} ({rec.employee_id.work_email}).",
                        subtype_id=self.env.ref('mail.mt_note').id
                    )
                except Exception as e:
                    _logger.warning("Failed to send ticket approval email to %s: %s", rec.employee_id.name, e)
            else:
                _logger.warning("Ticket approval email template not found.")

            group = self.env.ref('una_employee_ticket_request.group_ticket_final_approval_notify', raise_if_not_found=False)
            if group:
                emails = [u.email for u in group.users if u.email]
            else:
                emails = []
    

            # distribution_users = self.env['ticket.distribution.list'].search([])
            # emails = []
            # for group in distribution_users:
            #     emails += [u.email for u in group.user_ids if u.email]

            if emails:
                notify_template = self.env.ref('una_employee_ticket_request.mail_template_notify_ticket_issuers', raise_if_not_found=False)
                if notify_template:
                    try:
                        for email in emails:
                            notify_template.sudo().send_mail(rec.id, email_values={'email_to': email}, force_send=True)
                        rec.message_post(
                            body="Notification email sent to ticket issuers.",
                            subtype_id=self.env.ref('mail.mt_note').id
                        )
                    except Exception as e:
                        _logger.warning("Failed to send ticket issuer notification emails: %s", e)    

     

    def action_reject(self):
        self.state = 'rejected'


class HREmployee(models.Model):
    _inherit = 'hr.employee'
    ticket_limit = fields.Integer(string='Annual Ticket Limit', default=5)
    tickets_used_this_year = fields.Integer(string='Tickets Used This Year', default=0)
    ticket_request_ids = fields.One2many('employee.ticket.request', 'employee_id', string='Ticket Requests')
    ticket_approved_count = fields.Integer(
        string='Total No Of Approved Tickets',
        compute='_compute_ticket_approved_count',
        store=True,
        readonly=True
    )

    travel_date = fields.Date(string='Travel Date', store=True)
    return_date = fields.Date(string='Return Date', store=True)


    @api.depends('ticket_request_ids.state', 'ticket_request_ids.ticket_count')
    def _compute_ticket_approved_count(self):
        for employee in self:
            approved_requests = employee.ticket_request_ids.filtered(lambda r: r.state == 'approved')
            employee.ticket_approved_count = sum(r.ticket_count for r in approved_requests)


    # @api.depends('ticket_request_ids.state')
    # def _compute_ticket_approved_count(self):
    #     for employee in self:
    #         approved_requests = employee.ticket_request_ids.filtered(lambda r: r.state == 'approved')
    #         # Each approved request = 2 tickets (round trip)
    #         employee.ticket_approved_count = len(approved_requests) * 2

    ticket_request_ids = fields.One2many(
        'employee.ticket.request',
        'employee_id',
        string='Ticket Requests'
    )


    @api.model
    def _update_tickets_used_this_year(self):
        current_year = fields.Date.today().year
        for employee in self:
            approved_tickets = self.env['employee.ticket.request'].search([
                ('employee_id', '=', employee.id),
                ('state', '=', 'approved'),
                ('travel_date', '>=', f'{current_year}-01-01'),
                ('travel_date', '<=', f'{current_year}-12-31')
            ])
            employee.tickets_used_this_year = sum(t.ticket_count for t in approved_tickets)