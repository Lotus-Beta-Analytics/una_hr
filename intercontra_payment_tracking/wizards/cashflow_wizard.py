
from odoo import api, fields, models, _

class IntercontraCashflowWizard(models.TransientModel):
    _name = "intercontra.cashflow.wizard"
    _description = "Cashflow Projection Wizard"

    client = fields.Selection([("atc","ATC"),("ihs","IHS")], required=False)
    date_from = fields.Date()
    date_to = fields.Date()

    def action_compute(self):
        # Demo action: open milestones filtered by client through site
        domain = []
        if self.client:
            site_ids = self.env["intercontra.site.project"].search([("client","=",self.client)]).ids
            domain.append(("site_id","in",site_ids or [0]))
        return {
            "type":"ir.actions.act_window",
            "name": _("Milestones (Cashflow View)"),
            "res_model":"intercontra.milestone",
            "view_mode":"tree,form,pivot,graph",
            "domain": domain,
        }
