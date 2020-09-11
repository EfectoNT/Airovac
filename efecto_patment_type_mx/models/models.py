# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.crm.models.digest import Digest


class efecto_patment_type(models.Model):
    _inherit = 'account.payment'

    efecto_payment_type = fields.Float(digits=(1, 4),default=1, string="tipo de cambio", help="tipo de cambio")

