from odoo import fields, models, _,SUPERUSER_ID
from odoo.exceptions import UserError


class HrExpenseSheet(models.Model):
    _inherit = "hr.expense.sheet"

    state = fields.Selection(selection_add=[
        ('manager_approved', "Manager Approved"),
        ('cos_approved', "Corporate Service Approved"),
        ('finance_approved', "Finance Approved"),
    ], ondelete={
        'manager_approved': 'set default',
        'cos_approved': 'set default',
        'finance_approved': 'set default',
    })

    def _do_approve(self):
        """ Line manager approval step (default Odoo approve overridden) """
        self.ensure_one()
        self.write({'state': 'manager_approved'})
        self.notify(
            body=_("Expense request %s has been approved by the Line Manager and requires Corporate Service approval.") % self.name,
            group='una_expense.corporate_service_user'
        )

    def cos_approve_sheet(self):
        """ COS Approval -> Moves to Finance """
        self.ensure_one()
        self.write({'state': 'cos_approved'})
        self.notify(
            body=_("Expense request %s has been approved by Corporate Service and requires Finance approval.") % self.name,
            group='una_expense.finance_user'
        )

    def finance_approve_sheet(self):
        """ Final Approval by Finance """
        self.ensure_one()
        if not self.env.user.has_group('una_expense.finance_user'):
            raise UserError(_("You do not have permission to approve as Finance."))

        self.write({"state": "approve"})  # Odoo's final approved state

        # Determine if the user is approving their own expense
        is_self_approval = self.employee_id.user_id == self.env.user

        if is_self_approval:
            body = _("Expense request %s has been approved by Finance (self-approved).") % self.name
        else:
            body = _("Expense request %s has been fully approved by Finance.") % self.name

        self.notify(body=body)

    
    def _check_can_approve(self):
        for sheet in self:
            if sheet.employee_id.user_id == self.env.user:
                if not self.env.user.has_group('una_expense.finance_user'):
                    raise UserError(_("You cannot approve: %s: It is your own expense") % sheet.name)
    


    def notify(self, body='', users=None, group=False):
        """ Notify partners in group or user list """
        if users is None:
            users = []
        partners = []
        if group:
            group_users = self.env['res.users'].search([
                ('active', '=', True),
                ('company_id', '=', self.env.user.company_id.id)
            ])
            for user in group_users:
                if user.has_group(group) and user.id != SUPERUSER_ID:
                    partners.append(user.partner_id.id)
        else:
            partners = users

        if partners:
            self.message_post(body=body, partner_ids=partners)
        return True