# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.exceptions import except_orm, Warning, RedirectWarning


class ResPartner(models.Model):
    _inherit = "res.partner"

    fiscal_code = fields.Char('Fiscal code')
    pec = fields.Char('Electronic Invoicing (only in Italy)')
    sdi = fields.Char('Electronic Invoicing (only in Italy)')
    b2b_reg=fields.Boolean('b2b registration',default=False)
    b2b_confirmed=fields.Boolean('User enabled',default=False)

    #password = fields.Char(string='Password')
    #conf_password = fields.Char(string='Confirm Password')


    def enable_user(self):
        if self.b2b_confirmed:
            raise Warning('User already created !')
        b2b_user=self.env['res.users'].search([('partner_id','=',self.id)])
        if b2b_user:
            b2b_user.write({'active':True})
        # data = {
        #     'name': self.name,
        #     'login': self.name.lower().replace(' ', '.'),
        #     'partner_id': self.id,
        #     'password': self.name.lower().replace(' ', '.')
        # }
        # uid = self.env['res.users'].sudo().create(data)
        self.write({'b2b_confirmed':True})



