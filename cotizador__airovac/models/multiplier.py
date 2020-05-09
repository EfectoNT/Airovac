# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api

class StepMultiplier(models.Model):
    _name = 'step.multiplier'
    _description = "Etapa de cotización"

    name = fields.Char(string="Estapa", required = True)
    description = fields.Text(string="Descripción")
    step_multiplier_line_ids = fields.One2many(
        'step.multiplier.line', 'step_multiplier_id')




class StepMultiplierLine(models.Model):
    _name = 'step.multiplier.line'
    _description = "Etapa de cotización Linea"



    name = fields.Char(string="Multiplicadores por marca")
    marca = fields.Selection(lambda self : self.categorys_by_name(),string="Marca",store=True, required=True)
    e_multiplicador = fields.Float(digits=(1, 2), string="Multiplicador", help="")
    step_multiplier_id = fields.Many2one('step.multiplier',
                                ondelete='cascade', string="Etapa",
                                required=True)



    @api.onchange('marca')
    def _onchange_marca(self):
        print("marca")
        print(self.marca)


    def categorys_by_name(self):

        #sql_lines = ('SELECT marca '
        #       'FROM step_multiplier_line '
        #       'WHERE marca IS NOT NULL ')

        sql = ('SELECT categ_id '
               'FROM product_template')

        self.env.cr.execute(sql)
        #self.env.cr.execute(sql_lines)
        category_model = self.env['product.category']
        result = []

        #lines = self.env['step.multiplier.line'].search([('step_multiplier_id', '=' ,self.step_multiplier_id.id)]).marca
        #print(lines)
        for categ_id in self.env.cr.fetchall():
            category = category_model.browse(categ_id)
            print(category.id,category.name)
            tupla = (str(category.id),category.name)
            print(tupla)
            print('tupla')
            result.append(tupla)

        print(result)
        return result







