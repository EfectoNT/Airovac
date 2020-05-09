# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

class productTemplateInherit(models.Model):
    _inherit = 'product.template'

    e_igi = fields.Float(digits=(3, 2),string="IGI%", help="Porcentaje de IGI")
    e_importation = fields.Float(digits=(3, 2),string="STD Importación%", help="Porcentaje de Importación")
    #e_precio_list = fields.Float(digits=(10,2), string="Precio de Lista", help="Precio de lista")
    e_te_max = fields.Integer(string="T.E MIN")
    e_te_min = fields.Integer(string="T.E MAX")
    e_etiqueta_a = fields.Text(string="Etiqueta A")
    e_etiqueta_b = fields.Text(string="Etiqueta B")
    e_mult_min = fields.Float(digits=(1, 2), string="Mult. Min", help="e_mult_min")
    e_precio_de_lista = fields.Float(digits=(10, 2), string="Precio de Lista", help="Precio de lista")
    e_product_class  = fields.Many2one('producte.class',
                                         string="Clase de producto",
                                         )

class productSupplierinfoInherit(models.Model):
    _inherit = 'product.supplierinfo'

    e_mult_std = fields.Float(Default=1, digits=(1,4), string="Mult STD", help="Multiplicador solicitado al proveedor")

    @api.onchange('product_tmpl_id')
    def _default_precio_lista(self):
        print('Default mul')
        print(self.product_tmpl_id,self.product_tmpl_id.name,self.product_tmpl_id.e_igi)
        self.price = self.product_tmpl_id.e_precio_de_lista


class ProductuEClass(models.Model):
    _name = 'producte.class'
    _description = "Clase de producto"

    name = fields.Char(string="Clase de producto", required = True)
