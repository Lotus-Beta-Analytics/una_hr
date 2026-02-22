from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class IntercontraSiteProject(models.Model):
    _name = "intercontra.site.project"
    _description = "Intercontra Site Project"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(required=True, tracking=True)
    code = fields.Char(string="Site Code", tracking=True)
    client = fields.Selection([("atc", "ATC"), ("ihs", "IHS")], required=True, tracking=True)
    contract_value = fields.Monetary(string="Contract Value (Client)", currency_field="currency_id", tracking=True)
    contractor_budget = fields.Monetary(string="Contractor Budget", currency_field="currency_id", tracking=True)
    currency_id = fields.Many2one("res.currency", default=lambda self: self.env.company.currency_id.id, required=True)
    contractor_id = fields.Many2one("res.partner", domain=[("supplier_rank", ">", 0)], string="Primary Contractor")

    state = fields.Selection([
        ("draft", "Draft"),
        ("submitted", "Submitted"),
        ("manager_approved", "Manager Approved"),
        ("finance_approved", "Finance Approved"),
        ("active", "Active"),
        ("done", "Closed"),
        ("cancel", "Cancelled"),
    ], default="draft", tracking=True)

    milestone_ids = fields.One2many("intercontra.milestone", "site_id", string="Milestones")
    variation_ids = fields.One2many("intercontra.variation", "site_id")

    # Total allocation fields (for validation)
    total_client_percent = fields.Float(compute="_compute_totals", store=False, string="Total Client Allocation")
    total_contractor_percent = fields.Float(compute="_compute_totals", store=False, string="Total Contractor Allocation")
    
    # Progress fields (raw values - 30.0 for 30%)
    client_progress = fields.Float(compute="_compute_progress", store=False, string="Client Progress (raw)")
    contractor_progress = fields.Float(compute="_compute_progress", store=False, string="Contractor Progress (raw)")
    
    # Formatted progress fields for display (0.3 for 30%)
    client_progress_formatted = fields.Float(
        compute="_compute_progress_formatted", 
        string="Client Progress",
        digits=(16,2)
    )
    contractor_progress_formatted = fields.Float(
        compute="_compute_progress_formatted", 
        string="Contractor Progress",
        digits=(16,2)
    )
    
    has_fac_gate = fields.Boolean(compute="_compute_totals", store=False)

    @api.depends("milestone_ids.percent", "milestone_ids.role", "milestone_ids.code")
    def _compute_totals(self):
        """Compute total allocation percentages (all milestones regardless of status)"""
        for rec in self:
            client_pct = sum(m.percent or 0.0 for m in rec.milestone_ids if m.role == "client")
            contractor_pct = sum(m.percent or 0.0 for m in rec.milestone_ids if m.role == "contractor")
            has_fac = any((m.code or "").upper() in ("FAC", "FAC PASS") for m in rec.milestone_ids)
            rec.total_client_percent = client_pct
            rec.total_contractor_percent = contractor_pct
            rec.has_fac_gate = has_fac

    @api.depends("milestone_ids.percent", "milestone_ids.role", "milestone_ids.status")
    def _compute_progress(self):
        """Compute actual progress based on completed milestones (invoiced/paid/closed)"""
        for rec in self:
            client_completed = sum(
                m.percent or 0.0 for m in rec.milestone_ids 
                if m.role == "client" and m.status in ['invoiced', 'paid', 'closed']
            )
            contractor_completed = sum(
                m.percent or 0.0 for m in rec.milestone_ids 
                if m.role == "contractor" and m.status in ['invoiced', 'paid', 'closed']
            )
            rec.client_progress = client_completed
            rec.contractor_progress = contractor_completed

    @api.depends("client_progress", "contractor_progress")
    def _compute_progress_formatted(self):
        """Convert progress values (30.0) to format expected by percentage widget (0.3)"""
        for rec in self:
            rec.client_progress_formatted = (rec.client_progress or 0.0) / 100.0
            rec.contractor_progress_formatted = (rec.contractor_progress or 0.0) / 100.0

    @api.constrains("contract_value")
    def _check_contract_value(self):
        for rec in self:
            if rec.contract_value and rec.contract_value < 0:
                raise ValidationError(_("Contract value cannot be negative."))

    # Permission helpers
    def _check_can_pm(self):
        if not self.env.user.has_group("intercontra_payment_tracking.group_intercontra_project_manager"):
            raise UserError(_("Only Intercontra Project Managers can perform this action."))

    def _check_can_manager(self):
        if not self.env.user.has_group("intercontra_payment_tracking.group_intercontra_manager"):
            raise UserError(_("Only Intercontra Managers can perform this action."))

    def _check_can_finance(self):
        if not self.env.user.has_group("intercontra_payment_tracking.group_intercontra_finance"):
            raise UserError(_("Only Intercontra Finance Officers can perform this action."))

    def _ensure_required_basic_fields(self):
        for rec in self:
            missing = []
            if not rec.name:
                missing.append(_("Name"))
            if not rec.code:
                missing.append(_("Site Code"))
            if not rec.client:
                missing.append(_("Client"))
            if rec.contract_value is None:
                missing.append(_("Contract Value"))
            if missing:
                raise UserError(_("Please set required fields before submitting: %s") % ", ".join(missing))

    def _ensure_milestones_make_sense(self):
        """Validate that total allocation percentages are correct (using total fields)"""
        for rec in self:
            if not rec.milestone_ids:
                raise UserError(_("Add milestones before continuing."))
            if rec.total_client_percent <= 0 or rec.total_client_percent > 110:
                raise UserError(_("Client milestones look incorrect (sum=%.2f%%). Please review.") % rec.total_client_percent)
            if rec.total_contractor_percent < 0 or rec.total_contractor_percent > 110:
                raise UserError(_("Contractor milestones look incorrect (sum=%.2f%%). Please review.") % rec.total_contractor_percent)

    # Actions
    def action_generate_milestones(self):
        self._check_can_pm()
        for site in self:
            if site.state != "draft":
                raise UserError(_("You can only generate milestones in Draft."))
            if not site.contract_value:
                raise ValidationError(_("Set Contract Value before generating milestones."))

            tmpl_client = self.env["intercontra.milestone.template"].search([("client", "=", site.client), ("role", "=", "client")])
            tmpl_contractor = self.env["intercontra.milestone.template"].search([("client", "=", site.client), ("role", "=", "contractor")])
            lines = tmpl_client + tmpl_contractor
            if not lines:
                sel = dict(self._fields["client"].selection).get(site.client)
                raise ValidationError(_("No milestone templates found for client %s") % (sel or site.client))

            created = self.env["intercontra.milestone"]
            for t in lines:
                created |= created.create({
                    "site_id": site.id,
                    "role": t.role,
                    "code": t.code,
                    "name": t.name,
                    "percent": t.percent,
                    "base_amount": site.contract_value if t.role == "client" else site.contractor_budget or site.contract_value,
                })
            site.message_post(body=_("Milestones generated from templates (%s records).") % len(created))

            return {
                "type": "ir.actions.act_window",
                "res_model": "intercontra.milestone",
                "view_mode": "tree,form",
                "domain": [("site_id", "=", site.id)],
                "name": _("Milestones for %s") % site.name
            }

    def action_submit(self):
        self._check_can_pm()
        for rec in self:
            if rec.state != "draft":
                raise UserError(_("Only Draft projects can be submitted."))
            rec._ensure_required_basic_fields()
            rec._ensure_milestones_make_sense()
            rec.state = "submitted"
            rec.message_post(body=_("Project submitted for Manager approval."))

    def action_manager_approve(self):
        self._check_can_manager()
        for rec in self:
            if rec.state != "submitted":
                raise UserError(_("Only Submitted projects can be manager-approved."))
            rec.state = "manager_approved"
            rec.message_post(body=_("Manager approved. Awaiting Finance approval."))

    def action_finance_approve(self):
        self._check_can_finance()
        for rec in self:
            if rec.state != "manager_approved":
                raise UserError(_("Only Manager-approved projects can be finance-approved."))
            rec.state = "finance_approved"
            rec.message_post(body=_("Finance approved. Ready to Activate."))

    def action_activate(self):
        self._check_can_manager()
        for rec in self:
            if rec.state != "finance_approved":
                raise UserError(_("Only Finance-approved projects can be activated."))
            rec.state = "active"
            rec.message_post(body=_("Project activated."))

    def action_close(self):
        self._check_can_manager()
        for rec in self:
            if rec.state != "active":
                raise UserError(_("Only Active projects can be closed."))
            rec.state = "done"
            rec.message_post(body=_("Project closed."))

    def action_cancel(self):
        for rec in self:
            if rec.state == "cancel":
                continue
            rec.state = "cancel"
            rec.message_post(body=_("Project cancelled."))