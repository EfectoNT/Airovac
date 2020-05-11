# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    e_etiqueta_title_a = fields.Text(string="Titulo de Etiqueta A")
    e_etiqueta_title_b = fields.Text(string="Titulo de Etiqueta B")
    e_desciption = fields.Char(string="Descripción")

    e_g_m_p = fields.Monetary(compute='_compute_e_g_m_p',string="G.M. del Proyecto",readonly="True")
    e_costo_total_obra = fields.Monetary(compute='_compute_e_costo_total_obra',string="Costo Total Obra",readonly="True")
    e_costo_total_imp_obra = fields.Monetary(string="Costo Total Imp Obra",readonly="True")

    step_multiplier_id = fields.Many2one('step.multiplier',
                                         ondelete='cascade',
                                         string="Etapa del proyecto",
                                         )

    hide_fields = fields.Boolean(default = True)

    def mostrar_detalles(self):
        for order in self:
            if not order.hide_fields:
                order.update({'hide_fields': True})
                print("True",order.hide_fields)
                return
        order.update({'hide_fields': False})
        print("False", order.hide_fields)


    @api.onchange('step_multiplier_id')
    def _default_precio_lista(self):
        print(self)
        for line in self.order_line:
            print(line.e_multiplicador)
            #step_multiplier_model = self.env['step.multiplier']
            #step_multiplier = step_multiplier_model.browse(self.step_multiplier_id.id)
            print(self.step_multiplier_id.name)
            self.e_g_m_p = 0
            self.e_costo_total_obra = 0
            self.e_costo_total_imp_obra = 0

            for mults in self.step_multiplier_id.step_multiplier_line_ids:
                print(line.product_id.categ_id.id , mults.marca)
                print(line.e_multiplicador, mults.e_multiplicador)
                print('para el if')
                self.e_g_m_p += line.e_g_m_l
                self.e_costo_total_obra += line.e_costo_total
                self.e_costo_total_imp_obra += line.e_costo_total_imp

                if line.product_id.categ_id.id == int(mults.marca):
                    print('dentro el if')
                    line.e_multiplicador = mults.e_multiplicador
                    print(line.e_multiplicador , line.e_precio_de_lista, line.e_descuento)
                    line.price_unit = line.e_multiplicador * line.e_precio_de_lista * (1 - (line.e_descuento / 100))

    @api.onchange('amount_untaxed')
    def _default_precio_lista(self):
        for line in self.order_line:
            print(self.step_multiplier_id.name)
            line.e_estimado_pro_l = (line.price_subtotal * 100)/ self.amount_untaxed

    @api.depends('order_line.e_g_m_l')
    def _compute_e_g_m_p(self):
        print("que pedo carnal")
        for order in self:
            e_g_m_p = 0.0
            for line in order.order_line:
                e_g_m_p += line.e_g_m_l
            print(e_g_m_p)
            order.update({'e_g_m_p': e_g_m_p})

    @api.depends('order_line.e_costo_total')
    def _compute_e_costo_total_obra(self):
        print("compute_e_costo_total")
        for order in self:
            e_costo_total_obra = 0.0
            for line in order.order_line:
                e_costo_total_obra += line.e_costo_total
            print(e_costo_total_obra)
            order.update({'e_costo_total_obra': e_costo_total_obra})


    @api.depends('order_line.e_costo_total_imp')
    def _compute_e_costo_total_imp(self):
        print("que pedo carnal")
        for order in self:
            e_costo_total_imp_obra = 0.0
            for line in order.order_line:
                e_costo_total_imp_obra += line.e_costo_total_imp
            print('costo total impor',e_costo_total_imp_obra)
            order.update({'e_costo_total_imp_obra': e_costo_total_imp_obra})





class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'


    e_igi = fields.Float(digits=(3, 2), string="IGI %",help="Porcentaje de IGI")
    e_importation = fields.Float(digits=(3, 2), string="IMPOR %",help="Porcentaje de Importación")
    e_etiqueta_line_a = fields.Text(string="Etiqueta A")
    e_etiqueta_line_b = fields.Text(string="Etiqueta B")
    e_te_line_max = fields.Integer(string="T.E MIN")
    e_te_line_min = fields.Integer(string="T.E MAX")
    e_precio_de_lista = fields.Float(digits=(10, 2), string="P . L", help="Precio de lista")
    e_multiplicador = fields.Float(digits=(1, 2), string="Multiplicador", help="Multiplicador, si no existe el multiplicador por etapa se asigna el multiplicador minimo de venta")
    e_descuento = fields.Integer(string="Des %")
    price_unit =fields.Float(digits=(3, 2),default= 100 , string="Punto de Venta",help="P.L * Multiplicador * (1 - Descuento)")
    e_costo_total =fields.Monetary(string="Costo Total")
    e_provedor = fields.Many2one('product.supplierinfo',string="Proveedor")
    e_mult_std = fields.Float(digits=(1, 2), string="Mult std", help="Exwork mult")
    e_costo_unitario = fields.Float(digits=(1, 2),Default = 0, string="Costo Unitario", help="(1 + IGI + Impotación) * (PL * Mult. STD)")
    e_costo_total = fields.Float(digits=(1, 2),Default = 0, store=True, string="Costo Total", help="Costo Unitario * Cantidad")
    e_costo_total_imp = fields.Float(digits=(1, 2),Default = 0, store=True, string="Costo Total", help="Importacion * (PL * Mult. STD) * Cantidad")
    e_g_m_l = fields.Float(digits=(1, 2),Default = 0, store=True, string="G . M ", help="COSTO TOTAL / Subtotal")
    e_estimado_pro_l = fields.Float(digits=(1, 2), Default=0, store=True, string="S.T.P %", help="% Sobre total de propuesta")
    e_asociar = fields.Boolean( Default=False,string="asociar",help="aver que pedo")

    display_type = fields.Selection([
        ('line_section_procuct', "Sección de producto"),
        ('line_section', "Section"),
        ('line_note', "Note")], default=False, help="Technical field for UX purpose.")


    @api.onchange('e_costo_unitario', 'product_uom_qty')
    def compute_costo_total(self):
        return (self.e_costo_unitario * self.product_uom_qty)

    def _set_mul_default(self):
        print('set default')
        if not self.order_id.step_multiplier_id.id:
            print('Sin etapa de proyecto')
            if not self.product_id.id:
                print('Sin etapa de proyecto y sin producto')
                return 0
            else:
                print('Sin etapa de proyecto y con producto')
                print('oni')
                return  self.product_id.e_mult_min
        else:
            if not self.product_id.id:
                print('Con etapa de proyecto y sin producto')
                return 0
            else:
                for mults in self.order_id.step_multiplier_id.step_multiplier_line_ids:
                    print(self.product_id.categ_id.id , mults.marca)
                    print(self.e_multiplicador, mults.e_multiplicador)
                    print('para el if')
                    if self.product_id.categ_id.id == int(mults.marca):
                        print('dentro el if')
                        return mults.e_multiplicador
                return  self.product_id.e_mult_min
        return 0

    @api.onchange('product_id')
    def _default_precio_lista(self):
        self.e_precio_de_lista = self.product_id.e_precio_de_lista
        self.e_etiqueta_line_a = self.product_id.e_etiqueta_a
        self.e_etiqueta_line_b = self.product_id.e_etiqueta_b
        self.e_te_line_max = self.product_id.e_te_max
        self.e_te_line_min = self.product_id.e_te_min
        self.e_igi = self.product_id.e_igi
        self.e_importation = self.product_id.e_importation
        self.e_multiplicador = self._set_mul_default()
        self.price_unit = self.e_multiplicador * self.e_precio_de_lista * (1 - (self.e_descuento / 100))

    @api.onchange('e_multiplicador','e_descuento')
    def change_price_unit(self):
        self.price_unit = self.e_multiplicador * self.e_precio_de_lista * (
                    1 - (self.e_descuento / 100))

    #@api.onchange('e_descuento')
    #def change_descuento(self):
    #    self.price_unit = self.e_multiplicador * self.e_precio_de_lista * (
    #        1 - (self.e_descuento / 100))

    @api.onchange('product_uom_qty')
    def _onchange_quantity(self):
        print('node debe da cambiar')

    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        if not self.product_uom or not self.product_id:
            self.price_unit = 0.0
            return
        if self.order_id.pricelist_id and self.order_id.partner_id:
            price = self.price_unit
            product = self.product_id.with_context(
                lang=self.order_id.partner_id.lang,
                partner=self.order_id.partner_id,
                quantity=self.product_uom_qty,
                date=self.order_id.date_order,
                pricelist=self.order_id.pricelist_id.id,
                uom=self.product_uom.id,
                fiscal_position=self.env.context.get('fiscal_position')
            )
            self.price_unit = self.env['account.tax']._fix_tax_included_price_company(price, product.taxes_id, self.tax_id, self.company_id)



    @api.onchange('product_id','e_igi','e_importation','e_mult_std')
    def compute_costo_unitario(self):
        self.e_costo_unitario =  (1 + self.e_igi + self.e_importation) * ( self.e_mult_std * self.e_precio_de_lista)

    @api.onchange('e_costo_unitario','product_uom_qty')
    def compute_costo_total(self):
        self.e_costo_total = ( self.e_costo_unitario * self.product_uom_qty)

    @api.onchange('e_importation','product_uom_qty','e_mult_std')
    def compute_costo_total_imp(self):
        self.e_costo_total_imp = self.e_importation * (self.e_precio_de_lista * self.e_mult_std) * self.product_uom_qty

    @api.onchange('e_costo_total','price_unit','product_uom_qty')
    def compute_g_m_l(self):
        if self.e_costo_total == 0 or  self.price_unit == 0 or  self.product_uom_qty == 0:
            return 0
        self.e_g_m_l = self.e_costo_total / (self.price_unit * self.product_uom_qty)




