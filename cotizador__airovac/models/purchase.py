# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

class purchaseOrderLineInherit(models.Model):
    _inherit = 'purchase.order.line'

    e_mult_std =  fields.Float(digits=(1,4), string="Mult STD", help="Multiplicador solicitado al proveedor" )
    #fields.Float(digits=(1,4), string="Mult STD", help="Multiplicador solicitado al proveedor")
    e_cost_exwork = fields.Float(digits=(10, 2),string="Precio ExWorks", help="Precio de Lista X Mult STD")
    @api.onchange('product_qty','e_mult_std','price_unit')
    def _onchange_mult_std(self):
         self.e_cost_exwork = self.e_mult_std * self.price_unit
         print("update e_cost_exwork")

    @api.onchange('product_id')
    def _default_mult(self):
        print('Default mul')
        for x in self.product_id.seller_ids:
            if x.name == self.partner_id:
                print(x.name, self.partner_id)
                print('en el if')
                self.e_mult_std = x.e_mult_std
                print(x.e_mult_std)
                return
        print('Ceros')
        return

    @api.depends('product_qty', 'price_unit', 'taxes_id')
    def _compute_amount(self):
        for line in self:
            vals = line._prepare_compute_all_values()
            taxes = line.taxes_id.compute_all(
                vals['price_unit'],
                vals['currency_id'],
                vals['product_qty'],
                vals['product'],
                vals['partner'])
            line.update({
                'price_tax': sum(
                    t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'] * line.e_mult_std,
            })

