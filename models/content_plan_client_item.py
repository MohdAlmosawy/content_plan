# models/content_plan_client_item.py 

from odoo import models, fields, api
from datetime import datetime, timedelta, date

class ContentPlanClientItem(models.Model):
    _name = 'content.plan.client.item'
    _description = 'Content Plan Client Item'

    name = fields.Char(string='Name', required=True)
    list_id = fields.Many2one('content.plan.client.list', string='List', default=lambda self: self._default_list_id())
    used_in_contents = fields.Many2many('content.plan.contents', compute='_compute_usage_history', store=True, string='Used In Contents')
    color = fields.Integer('Color Index', compute='_compute_color')

    @api.model
    def _default_list_id(self):
        return self.env.context.get('active_id')

    @api.depends('name')
    def _compute_usage_history(self):
        for record in self:
            contents = self.env['content.plan.contents'].search([('item_ids', 'in', record.id)], order='date desc')
            record.used_in_contents = contents

    @api.depends('used_in_contents.date')
    def _compute_color(self):
        color_mapping = [1, 2, 3, 4, 10]  # Red, Orange, Yellow, Light Blue, Green
        all_items = self.env['content.plan.client.item'].search([])

        # Store the second most recent use date of each item
        most_recent_use = {}
        for item in all_items:
            dates = [fields.Date.from_string(content.date) for content in item.used_in_contents if content.date]
            dates = sorted(set(dates))  # Unique and sorted
            most_recent_use[item.id] = dates[-2] if len(dates) > 1 else None

        # Get the unique dates to improve color distribution
        unique_dates = sorted(set(filter(None, most_recent_use.values())), reverse=True)  # Sort in descending order

        if len(unique_dates) <= 1:
            for record in self:
                record.color = color_mapping[0] if most_recent_use.get(record.id) else color_mapping[-1]
            return

        for record in self:
            last_used_date = most_recent_use.get(record.id)

            if last_used_date:
                date_index = unique_dates.index(last_used_date)
                color_index = int((date_index / (len(unique_dates) - 1)) * (len(color_mapping) - 1))
                record.color = color_mapping[color_index]
            else:
                record.color = color_mapping[-1]