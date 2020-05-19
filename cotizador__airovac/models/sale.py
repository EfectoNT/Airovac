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
    e_costo_total_imp_obra = fields.Monetary(compute='_compute_e_costo_total_imp',string="Costo Total Imp Obra",readonly="True")

    step_multiplier_id = fields.Many2one('step.multiplier',
                                         ondelete='cascade',
                                         string="Etapa del proyecto",
                                         )

    hide_fields = fields.Boolean(default = True)
    contador = fields.Integer(default = 0, compute = '_compute_contador_paquetes')
    cambio_etapa = fields.Boolean(default = True,store=True, compute = '_compute_cambio_etapa',string="Hay cambio")
    cambio_etapa_chebox = fields.Boolean(default = False, string="Habilitar cambio de etapa")
    breakdown = fields.Boolean(default=True, string="Imprimir Desglosado")

    @api.depends('order_line.e_multiplicador')
    def _compute_cambio_etapa(self):
        print("compute etapa")
        for order in self:
            for line in order.order_line:
                if line.mult_is_changed():
                    print("ubo un cambio",line.mult_is_changed())
                    order.write({'cambio_etapa': True})
                    return
            order.write({'cambio_etapa': False})

    @api.onchange('cambio_etapa')
    def _onchange_cambio_etapa(self):
        print("onchange cambio etapa")
        for order in self:
            print(order.cambio_etapa)
            if order.cambio_etapa:
                  order.write({'cambio_etapa_chebox':False})
                  return
        order.write({'cambio_etapa_chebox': True})


    @api.onchange('cambio_etapa_chebox')
    def _onchangue_cambio_etapa_chebox(self):
        for order in self:
            print(order.cambio_etapa_chebox,order.cambio_etapa)
            if  order.cambio_etapa_chebox :
                order.write({'cambio_etapa': False})
                return {
                    'warning': {
                        'title': "Cuidado",
                        'message': "Al cambiar de etapa el Multiplicador sera sobre escrito",
                    }
                }

    def mostrar_detalles(self):
        for order in self:
            if not order.hide_fields:
                order.write({'hide_fields': True})
                #print("True",order.hide_fields)
                return
        order.write({'hide_fields': False})
        #print("False", order.hide_fields)


    @api.onchange('step_multiplier_id')
    def _onchange_step_multiplier_id(self):
        print('Hola')
        for order in self:
            for line in order.order_line:
                print("holi")
                mult = self.env['step.multiplier.line'].search([('e_step_multiplier_id','=',order.step_multiplier_id.id),('e_marca','=',line.product_id.categ_id.id)])
                print(mult.e_multiplicador)
                if mult.e_multiplicador > 0.0:
                    line.write({'e_multiplicador': mult.e_multiplicador,'price_unit' : mult.e_multiplicador * line.e_precio_de_lista * (1 - (line.e_descuento / 100))})
                else:
                    line.write({'e_multiplicador': 1, 'price_unit' :  1 * line.e_precio_de_lista * (1 - (line.e_descuento / 100))})
            order.write({'cambio_etapa': False})



    @api.onchange('amount_untaxed')
    def _onchange_amount_untaxed(self):
        for order in self:
            for line in order.order_line:
                line.write({'e_estimado_pro_l': (line.price_subtotal * 100)/ self.amount_untaxed})


    @api.depends('order_line.e_g_m_l')
    def _compute_e_g_m_p(self):
        #print("que pedo carnal")
        for order in self:
            e_g_m_p = 0.0
            for line in order.order_line:
                e_g_m_p += line.e_g_m_l
            #print(e_g_m_p)
            order.write({'e_g_m_p': e_g_m_p})





    @api.depends('order_line.e_costo_total')
    def _compute_e_costo_total_obra(self):
        #print("compute_e_costo_total")
        for order in self:
            e_costo_total_obra = 0.0
            for line in order.order_line:
                e_costo_total_obra += line.e_costo_total
            #print(e_costo_total_obra)
            order.write({'e_costo_total_obra': e_costo_total_obra})


    @api.depends('order_line.e_costo_total_imp')
    def _compute_e_costo_total_imp(self):
        #print("que pedo carnal")
        for order in self:
            e_costo_total_imp_obra = 0.0
            for line in order.order_line:
                e_costo_total_imp_obra += line.e_costo_total_imp
            #print('costo total impor',e_costo_total_imp_obra)
            order.write({'e_costo_total_imp_obra': e_costo_total_imp_obra})


    @api.depends('order_line.e_asociar','order_line.sequence','order_line.price_subtotal')
    def _compute_contador_paquetes(self):
        print("**********")
        for order in self:

            contador_one = 0

            for line in order.order_line:
                #print("linea",line.id,line.e_asociar)
                if line.e_asociar:
                    contador_one +=1



            #print("Contador_one",contador_one)
            if contador_one % 2 == 0 :
                contador  = 0
                grupo = 1
                colored = 1
                sigue = False
                total_group = 0
                div = 0
                aux = None
                for line in order.order_line:
                    #print(contador,'A',line.e_asociar,grupo,sigue)

                    if line.e_asociar:
                        contador +=1
                        if contador % 2 != 0 and aux is None:
                            aux = line.id
                            div = line.product_uom_qty
                            #print('Asignando Aux',aux.id,total_group)

                        total_group += line.price_unit * line.product_uom_qty
                        line.write({'grupo': grupo,'colored': colored,'e_p_unit_a': 0,'e_subtotal_no_des':0 })


                        #print(contador, 'B', line.e_asociar, grupo, sigue)

                        if contador % 2 == 0:
                             if div > 0:

                                 order_line = self.env['sale.order.line'].browse([aux])
                                 #print('Antes de operar puc')
                                 #print(order_line.id, total_group,div)
                                 op =  total_group / div
                                 #print('op', op)
                                 order_line.write({'e_p_unit_a': op, 'principal': 1,'e_subtotal_no_des':op * div  })
                             aux = None
                             total_group = 0
                             div = 0
                             sigue = False
                             grupo += 1
                             if grupo % 2 ==0:
                               colored = 2
                             else:
                                colored = 1
                            #print(contador, 'C', line.e_asociar, grupo, sigue)
                        else:
                            sigue = True
                            #total_group += line.price_subtotal
                            #print(aux.grupo,total_group,line.price_subtotal)
                            #print(contador, 'D', line.e_asociar, grupo, sigue)
                    else:
                        if sigue:
                            total_group += line.price_unit * line.product_uom_qty
                            #print('En sige Aux id',aux.id,aux.grupo, total_group, line.price_subtotal)
                            #if line.e_p_unit_a > 0 and line.principal > 0:
                            #    line.write({'grupo': grupo, 'colored': colored})
                            #else:
                            line.write({'grupo': grupo, 'colored' : colored,'e_p_unit_a': 0, 'principal': 0,'e_subtotal_no_des':0})
                            #print(contador, 'E', line.e_asociar, grupo, sigue)
                        else:
                            if line.e_p_unit_a > 0 or line.principal > 0:
                                line.write({'grupo': 0, 'colored': 0,
                                            'e_p_unit_a': line.price_unit, 'principal': 0,'e_subtotal_no_des':line.price_subtotal})
                            else:
                                line.write({'grupo': 0, 'colored': 0,'e_p_unit_a': line.price_unit,'e_subtotal_no_des':line.price_subtotal})
                            #print(contador, 'F', line.e_asociar, grupo, sigue,line.colored)
                    #lista.append(line)

            # lista.reverse()
            # for line_s in lista:
            #     print(line_s.id,line_s.colored)

            order.write({'contador': contador_one})
            #print('Aver we el contador', contador_one)



class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'


    e_igi = fields.Float(digits=(3, 2), string="IGI %",help="Porcentaje de IGI")
    e_importation = fields.Float(digits=(3, 2), string="IMPOR %",help="Porcentaje de Importación")
    e_etiqueta_line_a = fields.Text(string="Etiqueta A")
    e_etiqueta_line_b = fields.Text(string="Etiqueta B")
    e_te_line_max = fields.Integer(string="T.E MIN")
    e_te_line_min = fields.Integer(string="T.E MAX")
    e_precio_de_lista = fields.Float(digits=(10, 2), string="P . L", help="Precio de lista")
    e_multiplicador = fields.Float(digits=(1, 2),default=0, string="Multiplicador", help="Multiplicador, si no existe el multiplicador por etapa se asigna el multiplicador minimo de venta")
    e_descuento = fields.Integer(string="Des %")
    price_unit =fields.Float(digits=(3, 2), string="Punto de Venta",help="P.L * Multiplicador * (1 - Descuento)")
    e_costo_total =fields.Monetary(string="Costo Total")

    e_costo_unitario = fields.Float(digits=(1, 2),Default = 0, string="Costo Unitario", help="(1 + IGI + Impotación) * (PL * Mult. STD)")
    e_costo_total = fields.Float(digits=(1, 2),Default = 0, store=True, string="Costo Total", help="Costo Unitario * Cantidad")
    e_costo_total_imp = fields.Float(digits=(1, 2),Default = 0, store=True, string="C . T Import", help="Importacion * (PL * Mult. STD) * Cantidad")
    e_g_m_l = fields.Float(digits=(1, 2),Default = 0, store=True, string="G . M ", help="COSTO TOTAL / Subtotal")
    e_estimado_pro_l = fields.Float(digits=(1, 2), Default=0, store=True, string="S.T.P %", help="% Sobre total de propuesta")
    e_asociar = fields.Boolean( Default=False,string="asociar",help="Asocia productos con accesorios cada dos checkboxes")
    e_p_unit_a = fields.Monetary(Default=0,string="P.U con Accesorios",help="Precio unitario con accesorios")
    e_subtotal_no_des = fields.Monetary(Default=0,string="Subtutal",help="Sub tutal no desglosado")


    #campos no visibles, usados para el calculo de productos con accesorios :3
    sequence = fields.Integer("Sequence")
    grupo = fields.Integer(default=0)
    colored = fields.Integer(default=0)
    principal = fields.Integer(default=0)
    e_partida = fields.Char(string="Partida")


    e_provedor = fields.Many2one('product.supplierinfo', string="Proveedor")
    e_mult_std = fields.Float(digits=(1, 2),default = 1.0, string="Mult std",
                              help="Exwork mult")


    @api.onchange('e_costo_unitario', 'product_uom_qty')
    def compute_costo_total(self):
        return (self.e_costo_unitario * self.product_uom_qty)

    def _set_mul_default(self):
        if self.order_id.step_multiplier_id.id:
            mult = self.env['step.multiplier.line'].search(
                [('e_step_multiplier_id', '=', self.order_id.step_multiplier_id.id),
                 ('e_marca', '=', self.product_id.categ_id.id)])
            print(mult,"aquitoy",len(mult))
            if mult.e_multiplicador > 0.0 :
                print('mult.e_multiplicador > 0')
                return mult.e_multiplicador

        return 1.0

    def mult_is_changed(self):
        if self.order_id.step_multiplier_id.id:
            mult = self.env['step.multiplier.line'].search(
                [(
                 'e_step_multiplier_id', '=', self.order_id.step_multiplier_id.id),
                 ('e_marca', '=', self.product_id.categ_id.id)])
            print(mult.e_multiplicador)
            if (mult.e_multiplicador != self.e_multiplicador) or (mult.e_multiplicador == 0 and self.e_multiplicador != 1):
                return True
        if not self.order_id.step_multiplier_id.id:
            if self.e_multiplicador != 1:
                return True
        return False




    @api.onchange('e_multiplicador', 'e_descuento','e_precio_de_lista')
    def change_price_unit(self):
        print('al cambiar el multiplicador', self._set_mul_default(),
              self.product_id.e_precio_de_lista,
              self.price_unit)
        flag = self.env['res.users'].has_group('sales_team.group_sale_manager')
        if self.e_multiplicador < self.product_id.e_mult_min and not flag:
                self.e_multiplicador = self.product_id.e_precio_de_lista
                self.update({'price_unit': self.e_multiplicador * self.product_id.e_precio_de_lista * (
                                        1 - (self.e_descuento / 100))})
                return {
                    'warning': {
                        'title': "Cuidado",
                        'message': "No puedes ofrecer un producto por debajo de su multiplicador minimo",
                        'type': 'notification'
                    }
                }
        if self.e_multiplicador < self.product_id.e_mult_min and  flag:
                self.update({'price_unit': self.e_multiplicador * self.product_id.e_precio_de_lista * (
                                        1 - (self.e_descuento / 100))})
                return {
                    'warning': {
                        'title': "Cuidado",
                        'message': "Has ofrecido el producto x por debajo de su multiplicador minimo",
                        'type': 'notification'
                    }
                }


        self.update({'price_unit': self.e_multiplicador * self.product_id.e_precio_de_lista * (
                                    1 - (self.e_descuento / 100))})








    @api.onchange('product_id')
    def _default_precio_lista(self):
        self.write({'e_precio_de_lista':self.product_id.e_precio_de_lista,
                    'e_etiqueta_line_a': self.product_id.e_etiqueta_a,
                    'e_etiqueta_line_b': self.product_id.e_etiqueta_b,
                    'e_te_line_max' : self.product_id.e_te_max,
                    'e_te_line_min' : self.product_id.e_te_min,
                    'e_igi' : self.product_id.e_igi,
                    'e_importation' : self.product_id.e_importation,
                    'e_multiplicador' :  self._set_mul_default()
                    })

        #self.update({})
        #'price_unit': self._set_mul_default() * self.product_id.e_precio_de_lista * (
        #        1 - (self.e_descuento / 100))
        print(self._set_mul_default(),self.product_id.e_precio_de_lista,self.price_unit)

        return {'domain':{'e_provedor': [('product_tmpl_id', '=',self.product_id.id)]}}

        #self.e_precio_de_lista = self.product_id.e_precio_de_lista
        #self.e_etiqueta_line_a = self.product_id.e_etiqueta_a
        #self.e_etiqueta_line_b = self.product_id.e_etiqueta_b
        #self.e_te_line_max = self.product_id.e_te_max
        #self.e_te_line_min = self.product_id.e_te_min
        #self.e_igi = self.product_id.e_igi
        #self.e_importation = self.product_id.e_importation
        #self.e_multiplicador = self._set_mul_default()
        #self.price_unit = self.e_multiplicador * self.e_precio_de_lista * (1 - (self.e_descuento / 100))



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
            print(self.price_unit)
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
            print('aver que pedo',self._set_mul_default(), self.product_id.e_precio_de_lista,
                  self.price_unit)



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

    @api.onchange('e_costo_total', 'price_unit', 'product_uom_qty')
    def compute_g_m_l(self):
        if self.e_costo_total == 0 or self.price_unit == 0 or self.product_uom_qty == 0:
            return 0
        self.e_g_m_l = self.e_costo_total / (
                    self.price_unit * self.product_uom_qty)

    @api.onchange('e_provedor')
    def _onchange_e_mult_std(self):
        self.write({'e_mult_std' : self.e_provedor.e_mult_std})





    # @api.onchange('sequence')
    # def onchange_egml(self):
    #     print(self.sequence)
    #
    # @api.onchange('e_asociar')
    # def onchange_asociar(self):
    #     print('+++++++++++++++++++++++++++++')
    #
