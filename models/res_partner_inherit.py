# models/res_partner_inherit.py

from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    list_ids = fields.One2many('content.plan.client.list', 'partner_id', string='Lists')