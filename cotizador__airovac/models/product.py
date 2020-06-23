# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import UserError

class productTemplateInherit(models.Model):
    _inherit = 'product.template'

    e_igi = fields.Float(digits=(3, 4),string="IGI%", help="Porcentaje de IGI")
    e_importation = fields.Float(digits=(3, 4),string="STD Importación%", help="Porcentaje de Importación")
    #e_precio_list = fields.Float(digits=(10,2), string="Precio de Lista", help="Precio de lista")
    e_te_max = fields.Integer(string="T.E MAX",help="Tiempo maximo de entrega en semanas")
    e_te_min = fields.Integer(string="T.E MIN",help="Tiempo minimo de entrega en semanas")
    e_etiqueta_a = fields.Text(string="Etiqueta A")
    e_etiqueta_b = fields.Text(string="Etiqueta B")
    e_mult_min = fields.Float(digits=(10,4),default = 1, string="Mult. Min", help="e_mult_min")
    e_precio_de_lista = fields.Monetary(digits=(10, 2), string="Precio de Lista", help="Precio de lista")
    e_product_class  = fields.Many2one('producte.class',
                                         string="Marca",
                                         )
    e_tiempo_estimado = fields.Char(string="Tiempo Estimado",
                                        help="Tiempo estimado de entrega")

    e_revision_p_l = fields.Char(string="Revisión de P.L")

    @api.onchange('e_te_max')
    def e_change_e_te_max(self):
        if self.e_te_max < self.e_te_min:
            raise UserError(
                     'El tiempo máximo de entrega tiene que ser mayor que el tiempo mínimo')
        if self.e_te_max >= self.e_te_min :
            self.update({'sale_delay': (self.e_te_max * 7)})
        else:
            self.update({'sale_delay': (self.e_te_min * 7)})


    @api.onchange('e_te_min')
    def e_change_e_te_min(self):
        if self.e_te_min > self.e_te_max:
            raise UserError(
                'El tiempo mínimo de entrega tiene que ser menor que el tiempo máximo')




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

    @api.onchange('e_precio_de_lista')
    def _onchange_p_l(self):
        # flag = self.env['res.users'].has_group(
        #     'cotizador__airovac.group_nom_options')
        # print(flag, 'cambio precio de lista')
        # if not flag:
        #     raise UserError(
        #         'No tienes los permisos necesarios para hacer esta acción')

        self.write({'list_price':self.e_precio_de_lista})

    @api.onchange('list_price')
    def _onchange_price_sale(self):
        # flag = self.env['res.users'].has_group(
        #     'cotizador__airovac.group_nom_options')
        #
        # print(flag, 'cambio list price')
        # if not flag:
        #     raise UserError(
        #         'No tienes los permisos necesarios para hacer esta acción')

        self.write({'e_precio_de_lista': self.list_price})

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
    e_mult_min = fields.Float(digits=(1, 4),default=1, string="Multiplicador mínimo", help="Multiplicador, si no existe el multiplicador default 1")
    products_ids = fields.One2many('product.template', 'e_product_class',
                                      string="Productos"
                                      )

    e_num_products = fields.Integer(compute='_calculate_products')



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

    @api.depends('products_ids')
    def _calculate_products(self):
        for record in self:
            record.e_num_products = len(record.products_ids)

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

