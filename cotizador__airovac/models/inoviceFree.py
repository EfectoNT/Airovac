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

class EfectoAccountMoveLine(models.Model):
    _inherit = "account.move.line"

    efecto_mx_edi_customs_number = fields.Char(
        string='Fechas de los numeros de pedimento')


class AccountMoveFree(models.Model):
    _inherit = 'account.move'

    l10n_mx_edi_cfdi_name = fields.Char(string='CFDI name', copy=False, readonly=False,
                                        help='The attachment name of the CFDI editado.')


    def post(self):
        # OVERRIDE PARA FECHAS
        for move in self.filtered(lambda move: move.is_invoice()):
            for line in move.line_ids:
                stock_moves = line.mapped('sale_line_ids.move_ids').filtered(lambda r: r.state == 'done' and not r.scrapped)
                if not stock_moves:
                    continue
                landed_costs = self.env['stock.landed.cost'].sudo().search([
                    ('picking_ids', 'in', stock_moves.mapped('move_orig_fifo_ids.picking_id').ids),
                    ('l10n_mx_edi_customs_number', '!=', False),
                ])
                if not landed_costs:
                    continue
                line.l10n_mx_edi_customs_number = ','.join(list(set(landed_costs.mapped('l10n_mx_edi_customs_number'))))
                line.efecto_mx_edi_customs_number = ','.join(list(set(landed_costs.mapped('date'))))
        super(AccountMoveFree, self).post()

