from odoo import fields, models, api
from hijridate import Hijri, Gregorian
import logging
import datetime

_logger = logging.getLogger(__name__)

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
        _logger.info("Computing Hijri date triggered")
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

    @api.onchange('date')
    def _compute_notes_with_occasions(self):
        _logger.info("Computing notes with occasions triggered")
        for content in self:
            occasion_names = []
            try:
                _logger.info("Fetching date occasions")
                date_occasions = self.env['content.plan.date.occasions'].search([])
                _logger.info(f"date_occasions: {date_occasions}")

                for occasion in date_occasions:
                    _logger.info("Checking occasion for content date")
                    if content.date and isinstance(content.date, datetime.date):
                        _logger.info(f"content.date.strftime: {content.date.strftime('%m-%d')}")
                        _logger.info(f"occasion.day_month: {occasion.day_month}")
                        if content.date.strftime('%m-%d') == occasion.day_month:
                            _logger.info("Occasion found for content date")
                            occasion_names.append(occasion.name)

                    _logger.info("Checking occasion for content hijri date")
                    _logger.info(f"content.hijri_date: {content.hijri_date}")
                    _logger.info(f"occasion.hijri_day_month: {occasion.hijri_day_month}")
                    if content.hijri_date[-5:] == occasion.hijri_day_month:
                        _logger.info("Occasion found for content hijri date")
                        occasion_names.append(occasion.name)

                _logger.info("Joining occasion names")
                content.notes = ', '.join(occasion_names)
            except Exception as e:
                content.notes = ''
                _logger.error(f"An error occurred: {e}")
                raise exceptions.UserError(f"An error occurred: {e}")