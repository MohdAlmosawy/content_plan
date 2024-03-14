from odoo import fields, models, api
from hijridate import Hijri, Gregorian
import logging
from datetime import datetime
import datetime
from dateutil.relativedelta import relativedelta
import json


_logger = logging.getLogger(__name__)

class ContentPlan(models.Model):
    _name="content.plan"
    _description= "Content Plan"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(default=True)
    plan_title = fields.Char(tracking=True, compute='_compute_plan_title', readonly=True)
    description = fields.Text(tracking=True)
    partner_id = fields.Many2one('res.partner',string="Client",index= True,copy = False, tracking=True, required=True)

    plan_notes = fields.Text(string="Plan Notes", tracking=True, compute='_compute_plan_notes', readonly=True)
    
    status = fields.Selection(
        string="Status",
        selection= [('draft', 'Draft'),('pending_approval', 'Pending Approval'),('modification', 'In Modification'),('approved','Approved'),('canceled','Canceled')],
        default = 'draft',
        tracking=True
    )
    start_date = fields.Date(string="Start Date", required=True)
    hijri_start_date = fields.Char(string='Hijri Start', compute='_compute_hijri_date', readonly=True)
    end_date = fields.Date(string="End Date", required=True)
    hijri_end_date = fields.Char(string='Hijri End', compute='_compute_hijri_date', readonly=True)

    occasions = fields.Text(string='Occasions', compute='_compute_occasions')
    occasions_display = fields.Char(compute='_compute_occasions_display')
    hijri_occasions = fields.Text(string='Hijri Occasions', compute='_compute_occasions')
    hijri_occasions_display = fields.Char(compute='_compute_hijri_occasions_display')

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

    @api.depends('start_date', 'end_date')
    def _compute_occasions(self):
        for record in self:
            try:
                record.occasions = []  # Assign a default value
                start_date = record.start_date
                end_date = record.end_date
                date_range = []
                current_date = start_date
                while current_date <= end_date:
                    date_range.append(current_date)
                    current_date += relativedelta(days=1)

                occasions = self.env['content.plan.date.occasions'].search([])
                occasion_info = []
                hijri_occasion_info = []
                for date in date_range:
                    for occasion in occasions:
                        if date.strftime("%m-%d") == occasion.day_month :
                            occasion_info.append((occasion.day_month, occasion.name))
                        if str(Gregorian(date.year, date.month, date.day).to_hijri())[-5:] == occasion.hijri_day_month:
                            hijri_occasion_info.append((occasion.hijri_day_month, occasion.name))

                record.occasions = occasion_info
                record.hijri_occasions = hijri_occasion_info
            except Exception as e:
                # Handle exception
                pass

    @api.depends('occasions')
    def _compute_occasions_display(self):
        for record in self:
            occasions_list = eval(record.occasions)
            record.occasions_display = '\n'.join([f"{occ[0]} : {occ[1]}" for occ in occasions_list])

    
    @api.depends('hijri_occasions')
    def _compute_hijri_occasions_display(self):
        for record in self:
            try:
                if record.hijri_occasions:
                    # Extracting the content within the brackets
                    data_str = record.hijri_occasions[2:-2]  # Assuming the format is always "('05-24', 'today is the day 2')"
                    # Splitting the string to get individual tuples
                    data_list = data_str.split("), (")
                    # Convert each tuple string to a tuple, remove single quotes, and format for display
                    hijri_occasions_list = [tuple(entry.replace("'", "").split(", ")) for entry in data_list]
                    record.hijri_occasions_display = '\n'.join([f"{hij_occ[0]} : {hij_occ[1]}" for hij_occ in hijri_occasions_list])
                else:
                    record.hijri_occasions_display = ''  # Handle the case where hijri_occasions is empty or None
            except Exception as e:
                record.hijri_occasions_display = 'Invalid data format or processing error'  # Set a default value or error message

    @api.depends('partner_id')
    def _compute_plan_notes(self):
        for record in self:
            if record.partner_id:
                related_notes = self.env['content.plan.notes'].search([('partner_id', '=', record.partner_id.id)])
                record.plan_notes = related_notes.plan_notes if related_notes else ''
            else:
                record.plan_notes = ''

    @api.depends('partner_id', 'start_date', 'end_date')
    def _compute_plan_title(self):
        for record in self:
            if record.partner_id and record.start_date and record.end_date:
                partner_name = record.partner_id.name
                if record.start_date.month == record.end_date.month:
                    record.plan_title = f"{record.end_date.year} : {record.start_date.month} | {partner_name} Content Plan"
                else:
                    record.plan_title = f"{record.end_date.year} : {record.start_date.month} - {record.end_date.month} | {partner_name} Content Plan"
            else:
                record.plan_title = 'New Plan'

    def action_approved(self):
        task_stages = ['To Do', 'Processing', 'Review', 'Adjustments', 'Scheduling', 'Closed']
        for plan in self:
            if plan.status == 'pending_approval':
                plan.status = 'approved'
                plan.prevent_modification = True
                # Create the new project
                new_project = self.env['project.project'].create({
                    'name': plan.plan_title,
                    'user_id': None,
                    'partner_id': plan.partner_id.id,
                    'description': plan.description,
                    'date_start': plan.start_date,
                    # Add other necessary fields as required for your setup
                })

                # Log to help diagnose the issue with stage reuse
                _logger.info("Checking for existing task stages to link with the new project.")

                # Create a mail.message for the new project creation
                self.env['mail.message'].create({
                    'body': f"This project was created from approving the plan <a href='#' data-oe-model='content.plan' data-oe-id='{plan.id}'>{plan.plan_title}</a>",
                    'record_name': new_project.name,
                    'model': 'project.project',
                    'res_id': new_project.id,
                    'message_type': 'notification',
                    'subtype_id': self.env.ref('mail.mt_note').id,
                })

                for task_stage in task_stages:
                    # Search for an existing stage across all projects, excluding archived stages
                    existing_stage = self.env['project.task.type'].search([('name', '=', task_stage), ('active', '=', True)], limit=1)
                    if existing_stage:
                        _logger.info(f"Existing '{task_stage}' stage found, reusing it for the project.")
                    else:
                        _logger.info(f"No existing '{task_stage}' stage found, creating a new one.")
                        # If the stage doesn't exist in any project, create it
                        existing_stage = self.env['project.task.type'].create({
                            'name': task_stage,
                            # Initially, do not link the stage to any specific project, allowing it to be used globally
                        })
                    # Ensure the stage is linked to the new project, regardless of whether it was newly created or pre-existing
                    if new_project.id not in existing_stage.project_ids.ids:
                        existing_stage.write({'project_ids': [(4, new_project.id)]})
                        _logger.info(f"Linked '{task_stage}' stage to '{new_project.name}' project.")

                # Handling the creation of tasks within the newly created project
                to_do_stage = self.env['project.task.type'].search([('name', '=', 'To Do'), ('project_ids', 'in', new_project.id), ('active', '=', True)], limit=1)
                if not to_do_stage:
                    # Fallback: search for a global 'To Do' stage if not found specifically for the new project
                    to_do_stage = self.env['project.task.type'].search([('name', '=', 'To Do'), ('project_ids', '=', False), ('active', '=', True)], limit=1)

                if plan.contents_ids:
                    for content in plan.contents_ids:
                        # Search for the tag
                        tag = self.env['project.tags'].search([('name', '=', content.content_plan_contents_type_id.name)], limit=1)
                        if not tag:
                            tag = self.env['project.tags'].create({'name': content.content_plan_contents_type_id.name})

                        self.env['project.task'].create({
                            'name': content.content_title,
                            'project_id': new_project.id,
                            'stage_id': to_do_stage.id if to_do_stage else None,
                            'user_ids': None,
                            'tag_ids': [(4, tag.id)],
                            'description': f"<h3>Publishing Date</h3>: {content.date}<br><h3>Content</h3>: {content.content}<br><h3>Caption</h3>: {content.caption}<br><h3>Notes</h3>: {content.notes}",
                            # Add other necessary fields as needed
                        })

        return True






    def get_portal_url(self):
        # Define the logic to generate the URL for each plan
        base_url = '/my/plans/'  # Replace this with your actual base URL for plan details
        # Assuming plan_details() takes an argument 'plan_id'
        return f"{base_url}{self.id}/details"  # Example: '/my/plans/123/details'