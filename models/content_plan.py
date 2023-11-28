from odoo import fields, models, api

class ContentPlan(models.Model):
    _name="content.plan"
    _description= "Content Plan"

    active = fields.Boolean(default=True)
    plan_title = fields.Char(required=True)
    description = fields.Text()
    partner_id = fields.Many2one('res.partner',string="Client",index= True,copy = False)
    status = fields.Selection(
        string="Status",
        selection= [('draft', 'Draft'),('pending_approval', 'Pending Approval'),('modification', 'Modification'),('approved','Approved'),('canceled','Canceled')],
        default = 'draft'
    )
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")

    contents_ids = fields.One2many('content.plan.contents','content_plan_id',string="Contents")

    prevent_modification = fields.Boolean(
        string="Prevent Modification",
        default=False,
        help="Set to True to prevent modifications when the plan is pending approval."
    )

    # def name_get(self):
    #     result = []
    #     for record in self:
    #         name = record.plan_title or 'Unnamed Content Plan'
    #         result.append((record.id, name))
    #     return result

    def action_send_approval(self):
        for plan in self:
            if plan.status == 'draft':
                plan.status = 'pending_approval'
                plan.prevent_modification = True
        return True

    def action_reset_to_draft(self):
        for plan in self:
            if plan.status == 'pending_approval':
                plan.status = 'draft'
                plan.prevent_modification = False
        return True
