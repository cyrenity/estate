# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "A Realestate Property"

    name = fields.Char('Property Name', required=True, translate=True)
    description = fields.Text('Description', required=True, translate=True)
    postcode = fields.Char('Postcode', required=False)
    date_availability = fields.Date('Availability Date', required=True, default=lambda self: fields.Datetime.add( fields.Datetime.today(), months=3), copy=False)
    expected_price = fields.Float('Expected Price', required=False)
    selling_price = fields.Float('Selling Price', required=False, copy=False, readonly=True)
    bed_rooms = fields.Integer('Bedrooms', required=True, default=2)
    living_area = fields.Integer('Living Area', required=True, default=0)
    facades = fields.Integer('Facades', required=True, default=0)
    garage = fields.Boolean('Garage', required=True, default=False)
    garden = fields.Boolean('Garden', required=True, default=False)
    garden_area = fields.Integer('Garden Area', required=True, default=0)
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('east', 'East'), ('south', 'South'), ('west', 'West')],
        help="Select garden orientation")
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
            string='State',
            selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
            default='new'
            )

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    
    buyer = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson = fields.Many2one("res.users", string="Sales Person", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float(compute="_compute_total_area")
    best_offer = fields.Float(compute="_compute_best_offer")    
    
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price >=0)', 'The expected price must a positive number.'),
        ('check_selling_price', 'CHECK(selling_price >=0 OR selling_price=null)', 'The selling price must a positive number.'),
    ]
    
    @api.depends("living_area", "garden_area", "garden")
    def _compute_total_area(self):
        for record in self:
            if record.garden:
                record.total_area = record.living_area + record.garden_area
            else:
                record.total_area = record.living_area
                
                
    @api.depends("offer_ids")
    def _compute_best_offer(self):
        for record in self:
            try:
                record.best_offer = max(record.offer_ids.mapped("price"))
            except ValueError:
                record.best_offer = 0
                
    @api.onchange("garden")
    def _onchange_partner_id(self):
        self.garden_area = 10
        self.garden_orientation = "north"
        
    def action_cancel_property(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(_('A Sold property can not be canceled.'))
        return self.write({'state': 'canceled'})
    
    def action_sold_property(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError(_('A Canceled property can not be sold.'))
        return self.write({'state': 'sold'})
