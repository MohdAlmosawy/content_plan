from odoo import fields, models

class ContentPlan(models.Model):
    _name="content.plan"
    _description= "Content Plan"

    active = fields.Boolean(default=True)
    plan_title = fields.Char(required=True)
    description = fields.Text()
    partner_id = fields.Many2one('res.partner',string="Client",index= True,tracking=True,copy = False)
    status = fields.Selection(
        string="Status",
        selection= [('draft', 'Draft'),('pending_approval', 'Pending Approval'),('modification', 'Modification'),('approved','Approved'),('canceled','Canceled')],
        default = 'draft'
    )