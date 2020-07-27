# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

class purchaseOrderLineInherit(models.Model):
    _inherit = 'purchase.order.line'

    e_mult_std =  fields.Float(digits=(1,4), string="Mult STD", help="Multiplicador solicitado al proveedor" )
    #fields.Float(digits=(1,4), string="Mult STD", help="Multiplicador solicitado al proveedor")
    e_precio_lista = fields.Monetary(digits=(10, 2),string="P.L", help="Precio de Lista X Mult STD")


    @api.onchange('product_qty','e_mult_std')
    def _onchange_mult_std(self):
         self.price_unit = (self.e_mult_std * self.e_precio_lista )


    @api.onchange('product_id','partner_id')
    def _default_mult(self):
        print(self.price_unit,'price unit')
        print(self.partner_id.id, self.partner_id.name)
        for proveedor in self.product_id.seller_ids:
            print(proveedor.name,proveedor.id, self.partner_id.name,self.partner_id.id)
            if proveedor.id == self.partner_id.id:
                print('iguales',proveedor.id, self.partner_id.id)
                self.e_mult_std = proveedor.e_mult_std
                print(proveedor.e_mult_std)
                return
        self.e_mult_std = 1

        return

    @api.onchange('product_qty', 'product_uom')
    def _onchange_quantity(self):
        super(purchaseOrderLineInherit,self)._onchange_quantity()
        self.e_precio_lista = self.price_unit


class productSupplierinfoInherit(models.Model):
    _inherit = 'product.supplierinfo'

    e_mult_std = fields.Float(Default=1, digits=(1,4), string="Mult STD", help="Multiplicador solicitado al proveedor")

    @api.onchange('product_tmpl_id')
    def _default_precio_lista(self):
        print('Default mul')
        print(self.product_tmpl_id,self.product_tmpl_id.name,self.product_tmpl_id.e_igi)
        self.price = self.product_tmpl_id.e_precio_de_lista
