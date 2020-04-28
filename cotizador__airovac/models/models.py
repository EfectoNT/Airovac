# -*- coding: utf-8 -*-

from odoo import models, fields, api
class productTemplateInherit(models.Model):
    _inherit = 'product.template'

    igi = fields.Float(digits=(2, 4),string="IGI%", help="Porcentaje de IGI")
    importation = fields.Float(digits=(2, 4),string="STD Importación%", help="Porcentaje de Importación")
    precio_list = fields.Float(digits=(2, 4), string="Precio de Lista", help="Precio de lista")
    te_max = fields.Integer(string="T.E MIN")
    te_min = fields.Integer(string="T.E MAX")
    etiqueta_a = fields.Char(string="Etiqueta A")
    etiqueta_b = fields.Char(string="Etiqueta B")


# class cotizador__airovac(models.Model):
#     _name = 'cotizador__airovac.cotizador__airovac'
#     _description = 'cotizador__airovac.cotizador__airovac'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
