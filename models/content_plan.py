from odoo import fields, models, api
from hijridate import Hijri, Gregorian

class ContentPlan(models.Model):
    _name="content.plan"
    _description= "Content Plan"

    active = fields.Boolean(default=True)
    plan_title = fields.Char(required=True)
    description = fields.Text()
    partner_id = fields.Many2one('res.partner',string="Client",index= True,copy = False)
    status = fields.Selection(
        string="Status",
        selection= [('draft', 'Draft'),('pending_approval', 'Pending Approval'),('modification', 'Modification'),('approved','Approved'),('canceled','Canceled')],
        default = 'draft'
    )
    start_date = fields.Date(string="Start Date")
    hijri_start_date = fields.Char(string='Hijri Start', compute='_compute_hijri_date', readonly=True)
    end_date = fields.Date(string="End Date")
    hijri_end_date = fields.Char(string='Hijri End', compute='_compute_hijri_date', readonly=True)

    contents_ids = fields.One2many('content.plan.contents','content_plan_id',string="Contents")

    prevent_modification = fields.Boolean(
        string="Prevent Modification",
        default=False,
        help="Set to True to prevent modifications when the plan is pending approval."
    )

    # def name_get(self):
    #     result = []
    #     for record in self:
    #         name = record.plan_title or 'Unnamed Content Plan'
    #         result.append((record.id, name))
    #     return result

    def action_send_approval(self):
        for plan in self:
            if plan.status == 'draft' or plan.status == 'modification':
                plan.status = 'pending_approval'
                plan.prevent_modification = True
        return True

    def action_reset_to_draft(self):
        for plan in self:
            if plan.status == 'canceled':
                plan.status = 'draft'
                plan.prevent_modification = False
        return True

    def action_approved(self):
        for plan in self:
            if plan.status == 'pending_approval':
                plan.status = 'approved'
                plan.prevent_modification = True
        return True

    def modification_requested(self):
        for plan in self:
            if plan.status == 'pending_approval':
                plan.status = 'modification'
                plan.prevent_modification = False
        return True

    def action_cancel(self):
        for plan in self:
            if plan.status == 'draft' or plan.status == 'approved':
                plan.status = 'canceled'
                plan.prevent_modification = True
        return True

    @api.depends('start_date', 'end_date')
    def _compute_hijri_date(self):
        for record in self:
            # Convert Gregorian start_date to Hijri
            start_date = record.start_date
            if start_date:
                start_date_str = start_date.strftime("%Y-%m-%d")
                start_date_parts = start_date_str.split("-")
                start_year = int(start_date_parts[0])
                start_month = int(start_date_parts[1])
                start_day = int(start_date_parts[2])

                try:
                    hijri_start_date_obj = Gregorian(start_year, start_month, start_day).to_hijri()
                    hijri_start_date_str = f"{hijri_start_date_obj}"
                    record.hijri_start_date = hijri_start_date_str

                except OverflowError as e:
                    record.hijri_start_date = "Out of Supported Range"
                    _logger.warning("Gregorian start_date is out of supported range")
            
            else:
                record.hijri_start_date = ""

            # Convert Gregorian end_date to Hijri
            end_date = record.end_date
            if end_date:
                end_date_str = end_date.strftime("%Y-%m-%d")
                end_date_parts = end_date_str.split("-")
                end_year = int(end_date_parts[0])
                end_month = int(end_date_parts[1])
                end_day = int(end_date_parts[2])

                try:
                    hijri_end_date_obj = Gregorian(end_year, end_month, end_day).to_hijri()
                    hijri_end_date_str = f"{hijri_end_date_obj}"
                    record.hijri_end_date = hijri_end_date_str

                except OverflowError as e:
                    record.hijri_end_date = "Out of Supported Range"
                    _logger.warning("Gregorian end_date is out of supported range")
            
            else:
                record.hijri_end_date = ""
