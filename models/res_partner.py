# -*- coding: utf-8 -*-

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    fiscal_code = fields.Char('Fiscal code')
    pec = fields.Char('Electronic Invoicing (only in Italy)')
    sdi = fields.Char('Electronic Invoicing (only in Italy)')

