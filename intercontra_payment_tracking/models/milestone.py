from datetime import timedelta
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class IntercontraMilestone(models.Model):
    _name = "intercontra.milestone"
    _description = "Milestone Instance"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "site_id, role, id"

    ROLE_SEL = [("client","Client (AR)"), ("contractor","Contractor (AP)")]
    STATUS_SEL = [
        ("draft","Draft"),
        ("submitted","Submitted"),
        ("approved","Approved"),
        ("invoiced","Invoiced"),
        ("paid","Paid"),
        ("closed","Closed"),
    ]

    site_id = fields.Many2one("intercontra.site.project", required=True, ondelete="cascade", tracking=True)
    role = fields.Selection(ROLE_SEL, required=True, tracking=True)
    code = fields.Char(tracking=True)
    name = fields.Char(required=True, tracking=True)

    percent = fields.Float(digits=(16,2), tracking=True)
    # New formatted percent field for display with percentage widget
    percent_formatted = fields.Float(
        compute="_compute_percent_formatted",
        inverse="_inverse_percent_formatted",
        string="Percent",
        digits=(16,2),
        help="Percentage (will be displayed with % sign)"
    )
    
    base_amount = fields.Monetary(currency_field="currency_id", help="Base used to compute milestone amount (site contract or contractor budget)")
    amount = fields.Monetary(compute="_compute_amount", store=True, currency_field="currency_id")
    currency_id = fields.Many2one(related="site_id.currency_id", store=True, readonly=True)

    planned_date = fields.Date()
    achieved_date = fields.Date()
    approved_date = fields.Date()
    rfi_date = fields.Date(string="RFI Date")
    fac_eligible_date = fields.Date(compute="_compute_fac_eligible_date", store=True)

    status = fields.Selection(STATUS_SEL, default="draft", tracking=True)
    eligible_to_pay = fields.Boolean(compute="_compute_eligible", store=True)
    
    # Related field to access contractor from project (useful for filtering)
    contractor_id = fields.Many2one(
        related="site_id.contractor_id", 
        string="Contractor",
        store=True,
        readonly=True
    )

    # Accounting links
    invoice_id = fields.Many2one("account.move", domain=[("move_type","=","out_invoice")])
    vendor_bill_id = fields.Many2one("account.move", domain=[("move_type","=","in_invoice")])

    # Splits (for contractor role)
    split_ids = fields.One2many("intercontra.milestone.split", "milestone_id", string="Contractor Splits")

    requires_docs = fields.Boolean()
    required_doc_list = fields.Text()
    attachment_count = fields.Integer(compute="_compute_attachment_count")

    @api.depends("percent", "base_amount")
    def _compute_amount(self):
        for rec in self:
            rec.amount = round((rec.base_amount or 0.0) * (rec.percent or 0.0) / 100.0, 2)

    @api.depends("rfi_date")
    def _compute_fac_eligible_date(self):
        for rec in self:
            rec.fac_eligible_date = rec.rfi_date + timedelta(days=180) if rec.rfi_date else False
    
    @api.depends("percent")
    def _compute_percent_formatted(self):
        """Convert stored percent (30.0) to display format (0.3) for percentage widget"""
        for rec in self:
            rec.percent_formatted = (rec.percent or 0.0) / 100.0
    
    def _inverse_percent_formatted(self):
        """Convert display format (0.3) back to stored format (30.0) when user edits"""
        for rec in self:
            rec.percent = (rec.percent_formatted or 0.0) * 100.0
    
    def action_open_attachments(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Documents"),
            "res_model": "ir.attachment",
            "view_mode": "kanban,tree,form",
            "domain": [("res_model", "=", self._name), ("res_id", "=", self.id)],
            "context": {
                "default_res_model": self._name,
                "default_res_id": self.id,
            },
        }

    @api.depends("status", "approved_date", "fac_eligible_date", "role", "code", "rfi_date")
    def _compute_eligible(self):
        for rec in self:
            eligible = False
            if rec.role == "client":
                eligible = rec.status in ("approved","invoiced","paid")
            else:
                if rec.status in ("approved","invoiced","paid"):
                    if rec.code and rec.code.upper() in ("FAC","FAC PASS"):
                        eligible = fields.Date.context_today(self) >= (rec.fac_eligible_date or fields.Date.today())
                    else:
                        eligible = True
            rec.eligible_to_pay = eligible

    @api.constrains("percent")
    def _check_percent(self):
        for rec in self:
            if rec.percent is not None and (rec.percent < 0 or rec.percent > 100):
                raise ValidationError(_("Percent must be between 0 and 100."))

    def _compute_attachment_count(self):
        for rec in self:
            rec.attachment_count = self.env["ir.attachment"].search_count([
                ("res_model","=",self._name),
                ("res_id","=",rec.id)
            ])

    # Workflow for milestones
    def action_submit(self):
        self.write({"status":"submitted"})
        return True

    def action_approve(self):
        self.write({"status":"approved", "approved_date": fields.Date.context_today(self)})
        return True

    def action_create_move(self):
        for rec in self:
            if rec.role == "client":
                rec._create_customer_invoice()
            else:
                rec._create_vendor_bill()
        return True

    def _get_income_expense_accounts(self):
        company = self.env.company
        income = self.env["account.account"].search([
            ("deprecated","=",False), 
            ("company_id","=",company.id), 
            ("internal_group","=","income")
        ], limit=1)
        expense = self.env["account.account"].search([
            ("deprecated","=",False), 
            ("company_id","=",company.id), 
            ("internal_group","=","expense")
        ], limit=1)
        return income, expense

    def _create_customer_invoice(self):
        for rec in self:
            if rec.invoice_id or rec.amount <= 0:
                continue
            income_account, _ = rec._get_income_expense_accounts()
            if not income_account:
                raise UserError(_("Please configure an income account in your chart of accounts."))
                
            partner_id = self.env.company.partner_id.id
            move = self.env["account.move"].create({
                "move_type": "out_invoice",
                "partner_id": partner_id,
                "invoice_date": fields.Date.context_today(self),
                "invoice_origin": f"{rec.site_id.code or ''} {rec.name}",
                "invoice_line_ids": [(0,0,{
                    "name": rec.name,
                    "quantity": 1.0,
                    "price_unit": rec.amount,
                    "account_id": income_account.id,
                })],
            })
            rec.invoice_id = move.id
            rec.status = "invoiced"

    def _create_vendor_bill(self):
        for rec in self:
            if rec.vendor_bill_id or rec.amount <= 0:
                continue
            _, expense_account = rec._get_income_expense_accounts()
            if not expense_account:
                raise UserError(_("Please configure an expense account in your chart of accounts."))
                
            partner = rec.site_id.contractor_id.id or self.env.company.partner_id.id
            move = self.env["account.move"].create({
                "move_type": "in_invoice",
                "partner_id": partner,
                "invoice_date": fields.Date.context_today(self),
                "invoice_origin": f"{rec.site_id.code or ''} {rec.name}",
                "invoice_line_ids": [(0,0,{
                    "name": rec.name,
                    "quantity": 1.0,
                    "price_unit": rec.amount,
                    "account_id": expense_account.id,
                })],
            })
            rec.vendor_bill_id = move.id
            rec.status = "invoiced"

    def action_paid(self):
        self.write({"status": "paid"})
        return True

    def action_close(self):
        self.write({"status": "closed"})
        return True