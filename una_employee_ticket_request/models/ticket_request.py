from odoo import models, fields, api,_, exceptions
from datetime import timedelta
import logging
_logger = logging.getLogger(__name__)
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError


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
        string='Passager Relationship(PAX1)',
        store=True
        
    )
    
    call_relationship2 = fields.Selection(
        selection=[
            ('mother', 'Mother'),
            ('father', 'Father'),
            ('son', 'Son'),
            ('daughter', 'Daughter'),
            ('brother', 'Brother'),
            ('sister', 'Sister'),
            ('others', 'Others'),
            ('wife', 'Wife'),
            ('husband', 'Husband')
        ],
        string='Passager Relationship (PAX 2)',
        store=True
    )

    call_relationship3 = fields.Selection(
        selection=[
            ('mother', 'Mother'),
            ('father', 'Father'),
            ('son', 'Son'),
            ('daughter', 'Daughter'),
            ('brother', 'Brother'),
            ('sister', 'Sister'),
            ('others', 'Others'),
            ('wife', 'Wife'),
            ('husband', 'Husband')
        ],
        string='Passager Relationship (PAX 3)',
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
    pax_name = fields.Char(string="Passenger Name (PAX 1)", store = True)
    travel_date_pax1= fields.Date(string='Pax 1 Date of Travel', store=True)
    return_date_pax1 = fields.Date(string='Pax 1 Return Date', store=True)
    pax2_name = fields.Char(string="Passenger Name (PAX 2)", store =True)
    travel_date_pax2= fields.Date(string='Pax 2 Date of Travel', store=True)
    return_date_pax2 = fields.Date(string='Pax 2 Return Date', store=True)
    pax3_name = fields.Char(string="Passenger Name (PAX 3)", store = True)
    travel_date_pax3= fields.Date(string='Pax 3 Date of Travel', store=True)
    return_date_pax3 = fields.Date(string='Pax 3 Return Date', store=True)

    proposed_itinerary = fields.Text(string="PROPOSED INTENARY")
    travel_date = fields.Date(string='EMPLOYEE DATE OF TRAVEL', store=True)
    return_date = fields.Date(string='EMPLOYEE RETURN DATE', store=True)
    purpose = fields.Text(string='PURPOSE/DESCRIPTION OF REQUEST: ')
    pnr = fields.Char(string="Booking Reference [PNR]")
    destination = fields.Text(string="Destination")
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

    employee_self_travel = fields.Boolean(
        string="Indictate if you as an Employee is Traveling",
        default=False,
        help="Check if the employee themselves is traveling."
    )

    traveler_name = fields.Char(
        string="Traveler Name",
        store=True,
        readonly=True
    )

    @api.onchange('employee_self_travel', 'employee_id')
    def _onchange_employee_self_travel(self):
        """
        Auto-populate traveler_name with employee's name if checkbox is checked.
        """
        for rec in self:
            if rec.employee_self_travel and rec.employee_id:
                rec.traveler_name = rec.employee_id.name
            else:
                rec.traveler_name = False    

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


    @api.depends(
    'outbound_trip',
    'inbound_trip',
    'employee_self_travel',
    'pax_name',
    'pax2_name',
    'pax3_name'
)
    def _compute_ticket_count(self):
        """
        Compute total ticket count based on:
         - number of legs (1 for single, 2 for round trip)
         - number of travelers (employee + pax1–pax3)
        """
        for rec in self:
            # Determine legs
            has_outbound = bool(rec.outbound_trip and rec.outbound_trip.strip())
            has_inbound = bool(rec.inbound_trip and rec.inbound_trip.strip())

            if has_outbound and has_inbound:
                leg_count = 2
            elif has_outbound or has_inbound:
                leg_count = 1
            else:
                leg_count = 0

            # Determine traveler count
            traveler_count = 0
            if rec.employee_self_travel:
                traveler_count += 1
            if rec.pax_name:
                traveler_count += 1
            if rec.pax2_name:
                traveler_count += 1
            if rec.pax3_name:
                traveler_count += 1

            # Multiply by leg count
            rec.ticket_count = leg_count * traveler_count
            
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

        # Determine legs
        outbound = (vals.get('outbound_trip') or '').strip()
        inbound = (vals.get('inbound_trip') or '').strip()
        has_outbound = bool(outbound)
        has_inbound = bool(inbound)

        if has_outbound and has_inbound:
            leg_count = 2
        elif has_outbound or has_inbound:
            leg_count = 1
        else:
            raise ValidationError(_("Please provide at least one trip leg (outbound or inbound)."))

        # Determine traveler count
        traveler_count = 0
        if vals.get('employee_self_travel'):
            traveler_count += 1
        if vals.get('pax_name'):
            traveler_count += 1
        if vals.get('pax2_name'):
            traveler_count += 1
        if vals.get('pax3_name'):
            traveler_count += 1

        requested_ticket_count = leg_count * traveler_count

        # Check used tickets for the current year
        tickets_used = self.env['employee.ticket.request'].search([
            ('employee_id', '=', employee.id),
            ('state', '=', 'approved'),
            ('travel_date', '>=', f'{current_year}-01-01'),
            ('travel_date', '<=', f'{current_year}-12-31')
        ])
        used_ticket_count = sum(t.ticket_count for t in tickets_used)

        # Enforce ticket limit
        if (used_ticket_count + requested_ticket_count) > (employee.ticket_limit * 2):
            raise ValidationError(_(
                "Ticket request exceeds annual limit of %d tickets (%d round trips)."
            ) % (employee.ticket_limit * 2, employee.ticket_limit))

        # Generate name sequence if needed
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('employee.ticket.request') or 'New'

        vals['ticket_count'] = requested_ticket_count  # store computed ticket count

        return super().create(vals)
    

    def _validate_travel_selection(self):
        """Ensure that either self-travel is checked or at least one PAX is added."""
        for rec in self:
            has_self = bool(rec.employee_self_travel)
            has_pax = bool(rec.pax_name or rec.pax2_name or rec.pax3_name)
            if not (has_self or has_pax):
                raise ValidationError(_(
                    "You must either check 'Indicate if you as an Employee are Traveling' "
                    "or add at least one Passenger (PAX) before submitting the request."
                ))
            # --- 2️⃣ For each PAX entered, check that relationship is selected ---
            if rec.pax_name and not rec.call_relationship:
                raise ValidationError(_("Please select a relationship for Passenger (PAX 1)."))
            if rec.pax2_name and not rec.call_relationship2:
                raise ValidationError(_("Please select a relationship for Passenger (PAX 2)."))
            if rec.pax3_name and not rec.call_relationship3:
                raise ValidationError(_("Please select a relationship for Passenger (PAX 3)."))
            
            if rec.pax_name and not rec.travel_date_pax1:
                raise ValidationError(_("Please select a travel date for Passenger (PAX 1)."))
            if rec.pax2_name and not rec.travel_date_pax2:
                raise ValidationError(_("Please select a travel date for Passenger (PAX 2)."))
            if rec.pax3_name and not rec.travel_date_pax3:
                raise ValidationError(_("Please select a travel date for Passenger (PAX 3)."))
            if rec.employee_self_travel and not rec.travel_date:
                raise ValidationError(_("Please Enter Your Travel Date as an Employee."))



    def action_submit(self):
        for rec in self:
            rec._validate_travel_selection()


            # --- ✅ Enforce 48-hour notice before travel ---
            if rec.travel_date:
                now = fields.Datetime.now()
                min_allowed_date = now + timedelta(hours=48)
                if rec.travel_date < min_allowed_date.date():
                    raise ValidationError(_(
                        "Ticket request must be submitted at least 48 hours before the travel date.\n"
                        f"Requested Travel Date: {rec.travel_date.strftime('%Y-%m-%d')}\n"
                        f"Earliest Allowed Date: {min_allowed_date.strftime('%Y-%m-%d %H:%M')}"
                    ))
            
            if rec.travel_date_pax1:
                now = fields.Datetime.now()
                min_allowed_date = now + timedelta(hours=48)
                if rec.travel_date_pax1 < min_allowed_date.date():
                    raise ValidationError(_(
                        "Ticket request must be submitted at least 48 hours before the travel date.\n"
                        f"Requested Travel Date: {rec.travel_date_pax1.strftime('%Y-%m-%d')}\n"
                        f"Earliest Allowed Date: {min_allowed_date.strftime('%Y-%m-%d %H:%M')}"
                    ))   

            if rec.travel_date_pax2:
                now = fields.Datetime.now()
                min_allowed_date = now + timedelta(hours=48)
                if rec.travel_date_pax2 < min_allowed_date.date():
                    raise ValidationError(_(
                        "Ticket request must be submitted at least 48 hours before the travel date.\n"
                        f"Requested Travel Date: {rec.travel_date_pax2.strftime('%Y-%m-%d')}\n"
                        f"Earliest Allowed Date: {min_allowed_date.strftime('%Y-%m-%d %H:%M')}"
                    )) 

            if rec.travel_date_pax3:
                now = fields.Datetime.now()
                min_allowed_date = now + timedelta(hours=48)
                if rec.travel_date_pax3 < min_allowed_date.date():
                    raise ValidationError(_(
                        "Ticket request must be submitted at least 48 hours before the travel date.\n"
                        f"Requested Travel Date: {rec.travel_date_pax3.strftime('%Y-%m-%d')}\n"
                        f"Earliest Allowed Date: {min_allowed_date.strftime('%Y-%m-%d %H:%M')}"
                    ))            
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


    def get_request_form_url(self):
        """Return the full URL to the record form view."""
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for record in self:
            record_url = f"{base_url}/web#id={record.id}&model=employee.ticket.request&view_type=form"
            return record_url
        

    def action_approve_manager(self):
        for rec in self:
            rec.state = 'hr_team'
            rec.message_post(
                body="Ticket request approved by Line Manager. Forwarded to HR Team.",
                subtype_id=self.env.ref('mail.mt_note').id
            )
            # ✅ Load email template
            template = self.env.ref(
                'una_employee_ticket_request.mail_template_ticket_request_manager_approved',
                raise_if_not_found=False
            )
            if not template:
                _logger.warning("❌ Mail template not found for manager approval.")
                return
            # ✅ Load HR team group
            group = self.env.ref('una_employee_ticket_request.group_ticket_approval_hr', raise_if_not_found=False)
            if not group:
                _logger.warning("❌ HR team group not found.")
                return
            # ✅ Collect HR team emails
            hr_emails = group.users.filtered(lambda u: u.email).mapped('email')
            if not hr_emails:
                _logger.warning("❌ No users in HR team group have email addresses.")
                return
            email_to = ','.join(hr_emails)
            _logger.info("📧 Sending HR notification for ticket approval to: %s", email_to)

            # ✅ Send email with dynamic context
            try:
                template.with_context(email_to=email_to).send_mail(rec.id, force_send=True)
                rec.message_post(
                    body="Email notification sent to HR Team for ticket request review.",
                    subtype_id=self.env.ref('mail.mt_note').id
                )
            except Exception as e:
                _logger.error("❌ Failed to send HR team email: %s", str(e))
                rec.message_post(
                    body=f"⚠️ Failed to send email to HR Team: {e}",
                    subtype_id=self.env.ref('mail.mt_note').id
                )
    
      
    def action_approve_hr_team(self):
        template = self.env.ref('una_employee_ticket_request.mail_template_ticket_request_cco_approved', raise_if_not_found=False)
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
                raise UserError("Email template 'mail_template_ticket_request_cco_approved' not found.")
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
    def action_reject(self):
        self.state = 'rejected'

    def action_approve_cco(self):
        for rec in self:
            rec.state = 'approved'
            rec.ticket_issued = True
            rec.employee_id.tickets_used_this_year += rec.ticket_count
            # rec.employee_id.sudo().tickets_used_this_year += rec.ticket_count
            group = self.env.ref('una_employee_ticket_request.group_ticket_final_approval_notify', raise_if_not_found=False)
            if not group:
                _logger.warning("❌ Ticket issuer group not found.")
                continue
            group_emails = group.users.filtered(lambda u: u.email).mapped('email')
            if not group_emails:
                _logger.warning("❌ No users in the ticket issuer group have emails.")
                continue
            email_to = ','.join(group_emails)
            _logger.info("📧 Sending CCO approval notification to: %s", email_to)
            has_outbound = bool(rec.outbound_trip and rec.outbound_trip.strip())
            has_inbound = bool(rec.inbound_trip and rec.inbound_trip.strip())
            leg_count = 2 if (has_outbound and has_inbound) else 1
            travelers = []
            if rec.employee_self_travel:
                travelers.append(f"• {rec.employee_id.name} (Employee) → 🎫 {leg_count} ticket(s)")
            if rec.pax_name:
                travelers.append(f"• {rec.pax_name} (PAX 1 - {rec.call_relationship or 'N/A'}) → 🎫 {leg_count} ticket(s)")
            if rec.pax2_name:
                travelers.append(f"• {rec.pax2_name} (PAX 2 - {rec.call_relationship2 or 'N/A'}) → 🎫 {leg_count} ticket(s)")
            if rec.pax3_name:
                travelers.append(f"• {rec.pax3_name} (PAX 3 - {rec.call_relationship3 or 'N/A'}) → 🎫 {leg_count} ticket(s)")
            traveler_summary = "<br/>".join(travelers)
            message_body = (
                f"✅ Notification sent to Ticket Issuers ({email_to}) "
                f"<br/><b>Travelers and Tickets:</b><br/>{traveler_summary}"
                f"<br/><b>Total Tickets Approved:</b> {rec.ticket_count}"
            )
            rec.message_post(
                body=message_body,
                subtype_id=self.env.ref('mail.mt_note').id
            )
            notify_template = self.env.ref(
                'una_employee_ticket_request.mail_template_notify_ticket_issuers',
                raise_if_not_found=False
            )
            if notify_template:
                try:
                    notify_template.with_context(email_to=email_to).send_mail(rec.id, force_send=True)
                    _logger.info("✅ Ticket Issuer notification sent for request %s", rec.name)
                except Exception as e:
                    _logger.error("❌ Failed to send ticket issuer email: %s", str(e))
                    rec.message_post(
                        body=f"⚠️ Failed to send email to Ticket Issuers: {str(e)}",
                        subtype_id=self.env.ref('mail.mt_note').id
                    )
            else:
                _logger.warning("❌ Notify template not found.")

                    # --- ✅ Send approval email to the employee ---
            employee_template = self.env.ref(
                'una_employee_ticket_request.mail_template_ticket_request_approved',
                raise_if_not_found=False
            )
            if employee_template and rec.employee_id and rec.employee_id.work_email:
                try:
                    employee_template.send_mail(rec.id, force_send=True)
                    _logger.info("✅ Approval email sent to employee %s (%s)", rec.employee_id.name, rec.employee_id.work_email)
                    rec.message_post(
                        body=f"🎉 Approval email sent to employee: {rec.employee_id.name} ({rec.employee_id.work_email})",
                        subtype_id=self.env.ref('mail.mt_note').id
                    )
                except Exception as e:
                    _logger.error("❌ Failed to send approval email to employee %s: %s", rec.employee_id.name, e)
                    rec.message_post(
                        body=f"⚠️ Failed to send approval email to employee: {rec.employee_id.name}. Error: {e}",
                        subtype_id=self.env.ref('mail.mt_note').id
                    )
            else:
                _logger.warning("❌ Employee approval template or email missing for request %s.", rec.name)
                rec.message_post(
                    body="⚠️ Employee email template or email address missing. Approval email not sent.",
                    subtype_id=self.env.ref('mail.mt_note').id
                )
    def unlink(self):
        """
        Prevent deletion of records that are approved.
        Only allow deletion when the state is 'draft' or 'rejected'.
        """
        for rec in self:
            if rec.state == 'approved':
                raise ValidationError(_(
                    "You cannot delete a ticket request that has been approved. "
                    "Please reset it to Draft before deletion."
                ))
        return super().unlink()

    # @api.constrains(
    #     'travel_date', 'travel_date_pax1', 'travel_date_pax2', 'travel_date_pax3',
    #     'return_date', 'return_date_pax1', 'return_date_pax2', 'return_date_pax3')
    # def _check_unique_travel_dates(self):
    #     """
    #     Ensure that the employee and all passengers (PAX 1–3) do not have the same travel date.
    #     """
    #     for rec in self:
    #         dates = []
    #         if rec.travel_date:
    #             dates.append(('Employee', rec.travel_date))
    #         if rec.travel_date_pax1:
    #             dates.append(('PAX 1', rec.travel_date_pax1))
    #         if rec.travel_date_pax2:
    #             dates.append(('PAX 2', rec.travel_date_pax2))
    #         if rec.travel_date_pax3:
    #             dates.append(('PAX 3', rec.travel_date_pax3))
    #         seen = {}
    #         for label, date in dates:
    #             if date in seen:
    #                 raise ValidationError(_(
    #                     "Travel date conflict detected:\n"
    #                     "%s and %s cannot have the same travel date (%s)."
    #                 ) % (seen[date], label, date.strftime('%Y-%m-%d')))
    #             seen[date] = label
     
            

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