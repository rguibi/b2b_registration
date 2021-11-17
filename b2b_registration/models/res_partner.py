# -*- coding: utf-8 -*-
import werkzeug
from odoo import fields, models
from odoo.exceptions import except_orm, Warning, RedirectWarning


class ResPartner(models.Model):
    _inherit = "res.partner"

    fiscal_code = fields.Char('Fiscal code')
    pec = fields.Char('Electronic Invoicing (only in Italy)')
    sdi = fields.Char('Electronic Invoicing (only in Italy)')
    b2b_reg=fields.Boolean('b2b registration',default=False)
    b2b_confirmed=fields.Boolean('User enabled',default=False)

    password = fields.Char(string='Password')
    conf_password = fields.Char(string='Confirm Password')


    def enable_user(self):
        if self.b2b_confirmed:
            raise Warning('User already created !')
        b2b_user=self.env['res.users'].search([('partner_id','=',self.id),('active','=',False)])

        if b2b_user:
            b2b_user.write({'active':True})
            self.write({'b2b_confirmed':True})
            # template = self.ref('auth_signup.mail_template_user_signup_account_enabled',raise_if_not_found=False)
            # if b2b_user and template:
            #     template.sudo().with_context(
            #         lang=b2b_user.lang,
            #         auth_login=werkzeug.url_encode({'auth_login': b2b_user.email}),
            #     ).send_mail(b2b_user.id, force_send=True)



