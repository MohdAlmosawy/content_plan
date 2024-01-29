# models/res_partner_inherit.py

from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    item_ids = fields.One2many('content.plan.client.item', 'partner_id', string='Items')