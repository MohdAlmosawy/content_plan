from odoo import models, fields

class ContentPlanClientItem(models.Model):
    _name = 'content.plan.client.item'
    _description = 'Client Item'

    client_id = fields.Many2one('res.partner', string='Client')
    name = fields.Char(string='Item Name', required=True)
