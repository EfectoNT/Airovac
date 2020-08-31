import base64
from itertools import groupby
import re
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from io import BytesIO
import requests
from pytz import timezone

from lxml import etree
from lxml.objectify import fromstring
from zeep import Client
from zeep.transports import Transport

from odoo import _, api, fields, models, tools
from odoo.tools.xml_utils import _check_with_xsd
from odoo.tools import DEFAULT_SERVER_TIME_FORMAT
from odoo.tools import float_round
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_repr

from odoo.addons.l10n_mx_edi.tools.run_after_commit import run_after_commit

class AccountMoveFree(models.Model):
    _inherit = 'account.move'

    l10n_mx_edi_cfdi_name = fields.Char(string='CFDI name', copy=False, readonly=False,
                                        help='The attachment name of the CFDI editado.')

class AccountMoveLineEfecto(models.Model):
    _inherit = "account.move.line"

    @api.onchange('product_id')
    def _onchange_product_id_convert(self):

        #print(self.order_id.currency_id.name)

        moneda_usar = self.account_id.currency_id
        convertido = 0

        if moneda_usar.name == 'USD':
            convertido = self.product_id.e_precio_de_lista
            print('Son usd')
        if moneda_usar.name == 'MXN':
            dolars = self.env['res.currency'].search(
                [('name', '=', 'USD')],
                limit=1)
            if(self.product_id.e_precio_de_lista == 0):
                convertido = 1
            else:
                convertido = self.product_id.e_precio_de_lista / (dolars.rate * 1)
        else:
            dolars = self.env['res.currency'].search(
                [('name', '=', 'USD')],
                limit=1)

            otra_moneda = self.env['res.currency'].search(
                [('name', '=', self.account_id.currency_id.name)],
                limit=1)

            pesos = self.product_id.e_precio_de_lista / (dolars.rate * 1)
            convertido = pesos * otra_moneda.rate

        #print("convertido bebe",convertido)



        #print(self.e_precio_lista)
        return




