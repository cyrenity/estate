# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Realestate Property Offer"
    
    price = fields.Float('Offer Amount', required=True)
    
    status = fields.Selection(
        string='Offer Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        help="Select status")
    
    partner_id = fields.Many2one("res.partner", string="Partner", copy=False)
    property_id = fields.Many2one("estate.property", string="Property")
    
    
