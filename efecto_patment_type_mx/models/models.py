# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class efecto_patment_type(models.Model):
#     _name = 'efecto_patment_type.efecto_patment_type'
#     _description = 'efecto_patment_type.efecto_patment_type'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
