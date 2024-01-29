# models/content_plan_client_item.py

from odoo import models, fields

class ContentPlanClientItem(models.Model):
    _name = 'content.plan.client.item'
    _description = 'Content Plan Client Item'

    name = fields.Char(string='Name', required=True)
    partner_id = fields.Many2one('res.partner', string='Client', required=True)