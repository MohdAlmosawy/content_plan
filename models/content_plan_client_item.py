# models/content_plan_client_item.py

from odoo import models, fields, api

class ContentPlanClientItem(models.Model):
    _name = 'content.plan.client.item'
    _description = 'Content Plan Client Item'

    name = fields.Char(string='Name', required=True)
    list_id = fields.Many2one('content.plan.client.list', string='List', default=lambda self: self._default_list_id())

    @api.model
    def _default_list_id(self):
        return self.env.context.get('active_id')