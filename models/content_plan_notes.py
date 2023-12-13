from odoo import fields, models, api

class ContentPlanNotes(models.Model):
    _name="content.plan.notes"
    _description= "Client Content Plan Notes"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    partner_id = fields.Many2one('res.partner',string="Client",index= True,copy = False, tracking=True)
    plan_notes = fields.Text(string="Plan Notes", tracking=True)