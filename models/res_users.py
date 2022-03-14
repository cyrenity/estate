# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class Users(models.Model):    
    _inherit = 'res.users'
    
    property_ids = fields.One2many('estate.property', inverse_name='salesperson', domain="[('state', 'in', ('offer_received', 'new'))]")