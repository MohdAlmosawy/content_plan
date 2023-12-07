from odoo import models, fields

class ContentPlanDateOccasions(models.Model):
    _name = 'content.plan.date.occasions'
    _description = 'Recurring Occasions on Dates'

    name = fields.Char(string='Occasion Name')
    day_month = fields.Char(string='Day and Month')  # Store day and month for Gregorian date
    hijri_day_month = fields.Char(string='Hijri Day and Month')  # Store day and month for Hijri date
