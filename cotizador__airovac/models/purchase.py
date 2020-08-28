# -*- coding: utf-8 -*-
import datetime
from odoo.exceptions import UserError

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

class purchaseOrderLineInherit(models.Model):
    _inherit = 'purchase.order.line'

    e_mult_std =  fields.Float(digits=(1,4), string="Mult STD", help="Multiplicador solicitado al proveedor" )
    #fields.Float(digits=(1,4), string="Mult STD", help="Multiplicador solicitado al proveedor")
    e_precio_lista = fields.Monetary(digits=(10, 2),string="P.L", help="Precio de Lista X Mult STD")


    @api.onchange('product_qty','e_mult_std','e_precio_lista')
    def _onchange_mult_std(self):
         self.price_unit = (self.e_mult_std * self.e_precio_lista )


    @api.onchange('product_id')
    def _default_mult(self):
        if not self.order_id.currency_id:
            raise UserError(
                'ELIJA UNA TARIFA')
        #print(self.order_id.currency_id.name)

        moneda_usar = self.order_id
        convertido = 0

        if moneda_usar.currency_id.name == 'USD':
            convertido = self.product_id.e_precio_de_lista
            print('Son usd')
        if moneda_usar.currency_id.name == 'MXN':
            dolars = self.env['res.currency'].search(
                [('name', '=', 'USD')],
                limit=1)
            convertido = self.product_id.e_precio_de_lista / (dolars.rate * 1)
        else:
            dolars = self.env['res.currency'].search(
                [('name', '=', 'USD')],
                limit=1)

            otra_moneda = self.env['res.currency'].search(
                [('name', '=', self.order_id.currency_id.name)],
                limit=1)

            pesos = self.product_id.e_precio_de_lista / (dolars.rate * 1)
            convertido = pesos * otra_moneda.rate

        #print("convertido bebe",convertido)

        self.write({'e_precio_lista': convertido,
                    'e_mult_std':1})

        #print(self.e_precio_lista)
        return




class productSupplierinfoInherit(models.Model):
    _inherit = 'product.supplierinfo'

    #e_mult_std = fields.Float(Default=1, digits=(1,4), string="Mult STD", help="Multiplicador solicitado al proveedor")

    @api.onchange('product_tmpl_id')
    def _default_precio_lista(self):
        print('Default mul')
        print(self.product_tmpl_id,self.product_tmpl_id.name,self.product_tmpl_id.e_igi)
        self.price = self.product_tmpl_id.e_precio_de_lista

