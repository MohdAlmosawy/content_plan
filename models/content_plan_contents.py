from odoo import fields, models

class ContentPlanContents(models.Model):
    _name = "content.plan.contents"
    _description = "Plan Contents"

    content_plan_id = fields.Many2one("content.plan", string="Content Plan")

    date = fields.Date(string='Publishing Date')
    content_plan_contents_type_id = fields.Many2one("content.plan.contents.type",string="Post type")
    content_title = fields.Char(string='Title')
    content = fields.Text(string='Content')
    notes = fields.Text(string='Notes')
