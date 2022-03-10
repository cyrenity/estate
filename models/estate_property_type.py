# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Realestate Property Type"

    name = fields.Char('Property Type Name', required=True)
    active = fields.Boolean('Active', default=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    
    _sql_constraints = [
        ('unique_type', 'unique(name)', "Property type already exists.")
    ]

