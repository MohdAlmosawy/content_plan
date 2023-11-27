from odoo import fields,models

class ContentPlanContentsType(models.Model):
    _name ="content.plan.contents.type"
    _description="type of content"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'The name of the content type must be unique!'),
    ]
