from odoo import fields, models, api
from hijridate import Hijri, Gregorian

class ContentPlanContents(models.Model):
    _name = "content.plan.contents"
    _description = "Plan Contents"

    content_plan_id = fields.Many2one("content.plan", string="Content Plan")

    date = fields.Date(string='Publishing Date')
    hijri_date = fields.Char(string='Hijri', compute='_compute_hijri_date', readonly=True)
    content_plan_contents_type_id = fields.Many2one("content.plan.contents.type",string="Post type")
    content_title = fields.Char(string='Title')
    content = fields.Text(string='Content')
    caption = fields.Text(string='Post Caption') 
    notes = fields.Text(string='Notes')

    @api.depends('date')
    def _compute_hijri_date(self):
        for record in self:
            # Convert Gregorian date to Hijri
            gregorian_date = record.date
            if gregorian_date:
                gregorian_date_str = gregorian_date.strftime("%Y-%m-%d")
                gregorian_date_parts = gregorian_date_str.split("-")
                year = int(gregorian_date_parts[0])
                month = int(gregorian_date_parts[1])
                day = int(gregorian_date_parts[2])

                # Check if the Gregorian date is within the supported range
                try:
                    hijri_date_obj = Gregorian(year, month, day).to_hijri()
                    hijri_date_str = f"{hijri_date_obj}"
                    record.hijri_date = hijri_date_str

                except OverflowError as e:
                    # Catch the OverflowError specifically for out-of-range dates
                    error_msg = str(e)
                    if error_msg == "date out of range":
                        record.hijri_date = "Out of Supported Range"
                        _logger.warning("Gregorian date is out of supported range")
                    else:
                        _logger.error(f"Error calculating Hijri date: {e}")
                        raise  # Re-raise the OverflowError for other issues
            else:
                record.hijri_date = ""