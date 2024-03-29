from odoo import fields, models, api
from hijridate import Hijri, Gregorian
import logging
import datetime

_logger = logging.getLogger(__name__)

class ContentPlanContents(models.Model):
    _name = "content.plan.contents"
    _description = "Plan Contents"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    content_plan_id = fields.Many2one("content.plan", string="Content Plan")

    date = fields.Date(string='Publishing Date', tracking=True)
    hijri_date = fields.Char(string='Hijri', compute='_compute_hijri_date', readonly=True)
    content_plan_contents_type_id = fields.Many2one("content.plan.contents.type",string="Post type", tracking=True)
    content_title = fields.Char(string='Title', tracking=True)
    content = fields.Text(string='Content', tracking=True)
    caption = fields.Text(string='Post Caption', tracking=True) 
    partner_id = fields.Many2one('res.partner', string='Partner', related='content_plan_id.partner_id', readonly=True)
    list_id = fields.Many2many('content.plan.client.list', string='List', domain="[('partner_id', '=', partner_id)]", tracking=True)
    item_ids = fields.Many2many('content.plan.client.item', string='Items', domain="[('list_id', '=', list_id)]", tracking=True)
    notes = fields.Text(string='Notes', tracking=True)

    display_name = fields.Char(compute='_compute_display_name')

    @api.depends('content_title', 'date')
    def _compute_display_name(self):
        for record in self:
            record.display_name = '%s (%s)' % (record.content_title, record.date)

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
    def _populate_notes_with_occasions(self):
        for content in self:
            occasion_names = []
            try:
                date_occasions = self.env['content.plan.date.occasions'].search([])

                for occasion in date_occasions:
                    if content.date and isinstance(content.date, datetime.date) and \
                    content.date.strftime('%m-%d') == occasion.day_month:
                        occasion_names.append(occasion.name)

                    if content.hijri_date and content.hijri_date[-5:] == occasion.hijri_day_month:
                        occasion_names.append(occasion.name)

                content.notes = ', '.join(occasion_names)
            except Exception as e:
                content.notes = ''
                _logger.error(f"An error occurred: {e}")
                raise exceptions.UserError(f"An error occurred: {e}")

    def open_content_plan_contents_form(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'content.plan.contents',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'current',
        }