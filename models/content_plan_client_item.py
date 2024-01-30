# models/content_plan_client_item.py

from odoo import models, fields, api

class ContentPlanClientItem(models.Model):
    _name = 'content.plan.client.item'
    _description = 'Content Plan Client Item'

    name = fields.Char(string='Name', required=True)
    list_id = fields.Many2one('content.plan.client.list', string='List', default=lambda self: self._default_list_id())
    last_used_in = fields.Many2one('content.plan.contents', compute='_compute_usage_history', string='Last Used In')
    used_in_plans = fields.Many2many('content.plan.contents', compute='_compute_usage_history', string='Used In Plans')
    color = fields.Integer('Color Index', compute='_compute_color')

    @api.model
    def _default_list_id(self):
        return self.env.context.get('active_id')

    @api.depends('name')
    def _compute_usage_history(self):
        for record in self:
            plans = self.env['content.plan.contents'].search([('item_ids', 'in', record.id)])
            record.used_in_plans = plans
            record.last_used_in = plans and plans[0] or False

    @api.depends('last_used_in')
    def _compute_color(self):
        for record in self:
            # Check if the item has been used
            if record.last_used_in:
                record.color = 4  # Red
            else:
                record.color = 2  # Green