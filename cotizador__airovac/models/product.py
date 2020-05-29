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
    e_mult_min = fields.Float(digits=(1, 4),default = 1, string="Mult. Min", help="e_mult_min")
    e_precio_de_lista = fields.Float(digits=(10, 2), string="Precio de Lista", help="Precio de lista")
    e_product_class  = fields.Many2one('producte.class',
                                         string="Clase de producto",
                                         )
    e_tiempo_estimado = fields.Char(string="Tiempo Estimado",
                                        help="Tiempo estimado de entrega")

    @api.onchange('e_product_class')
    def _e_product_class(self):
        print('onchangue')
        self.write({'e_mult_min': self.e_product_class.e_mult_min})

    @api.onchange('e_mult_min')
    def _change_mult_min(self):
        print('onchangue emult')
        if self.e_mult_min < 0:
            self.write({'e_mult_min': self._origin.e_mult_min})
            return {
                'warning': {
                    'title': "Cuidado",
                    'message': "El multiplicador mínimo debe ser mayor que 0.0",
                }
            }



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
    _description = "Marca del producto"

    name = fields.Char(string="Marca del producto", required = True)
    e_mult_min = fields.Float(digits=(1, 2),default=1, string="Multiplicador mínimo", help="Multiplicador, si no existe el multiplicador default 1")
    products_ids = fields.One2many('product.template', 'e_product_class',
                                      string="Productos ",
                                      )

    @api.onchange('e_mult_min')
    def _onchange_(self):
        if self.e_mult_min < 0:
            self.write({'e_mult_min': self._origin.e_mult_min})
            return {
                'warning': {
                    'title': "Cuidado",
                    'message': "El multiplicador mínimo debe ser mayor que 0.0",
                }
            }

        # for clase in self:
        #     print(clase.ids)
        #
        #     print('PRODUCTS',clase.products_ids.ids )
        #     lista = self.env['product.template'].search(
        #         [('id', 'in', clase.products_ids.ids)])
        #
        #     for producto in lista:
        #         print('en lista',producto.name)
        #         producto.write({'e_mult_min': clase.e_mult_min})
        #

