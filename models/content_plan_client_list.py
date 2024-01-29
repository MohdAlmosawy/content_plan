# models/content_plan_client_list.py

from odoo import models, fields

class ContentPlanClientList(models.Model):
    _name = 'content.plan.client.list'
    _description = 'Content Plan Client List'

    name = fields.Char(string='Name', required=True)
    partner_id = fields.Many2one('res.partner', string='Client', required=True)
    item_ids = fields.One2many('content.plan.client.item', 'list_id', string='Items')