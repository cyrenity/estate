# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from datetime import datetime, timedelta

from odoo.exceptions import UserError, ValidationError


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
    validity = fields.Integer("Offer Validity", default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    
    
    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'The offer price must a positive number.'),
    ]
        
        
    @api.constrains('price')
    def _check_offer_price(self):
        for record in self:
            if (100 * float(record.price)/float(record.property_id.expected_price)) < 90:
                raise ValidationError("The offer price should be atleast 90% of the expected price.")

    
    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                record.validity = (record.date_deadline - record.create_date.date()).days
                
                
    def action_accept_offer(self):
        for record in self:
            if record.property_id.state not in('sold', 'canceled'):
                record.property_id.selling_price = record.price
                record.property_id.state = 'sold'
                record.property_id.buyer = record.partner_id
            else:
                raise UserError("Cannot accept an offer for a Sold/Canceled Property")
        return self.write({'status': 'accepted'})
    
    def action_refuse_offer(self):
        for record in self:
            if record.property_id.state in('sold', 'canceled'):
                raise UserError("Cannot refuse an offer for a Sold/Canceled Property")
        return self.write({'status': 'refused'})