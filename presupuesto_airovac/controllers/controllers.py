# -*- coding: utf-8 -*-
# from odoo import http


# class PresupuestoAirovac(http.Controller):
#     @http.route('/presupuesto_airovac/presupuesto_airovac/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/presupuesto_airovac/presupuesto_airovac/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('presupuesto_airovac.listing', {
#             'root': '/presupuesto_airovac/presupuesto_airovac',
#             'objects': http.request.env['presupuesto_airovac.presupuesto_airovac'].search([]),
#         })

#     @http.route('/presupuesto_airovac/presupuesto_airovac/objects/<model("presupuesto_airovac.presupuesto_airovac"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('presupuesto_airovac.object', {
#             'object': obj
#         })
