from odoo import fields, models

class ContentPlanContents(models.Model):
    _name = "content.plan.contents"
    _description = "Content Plan Contents"

    date = fields.Date(string='Publishing Date')
    content_plan_contents_type_id = fields.Many2one("content.plan.contents.type",string="Post type")
    content = fields.Text(string='Content')
    notes = fields.Text(string='Notes')
