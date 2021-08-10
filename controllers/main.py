# -*- coding: utf-8 -*-

import logging
import werkzeug
from odoo import http, _
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.exceptions import UserError
from odoo.http import request

_logger = logging.getLogger(__name__)


class AuthSignupHome(AuthSignupHome):
    def do_signup(self, qcontext):
        """ Shared helper that creates a res.partner out of a token """
        values = {key: qcontext.get(key) for key in ('login', 'name', 'password', 'phone', 'street', 'street2',
                                                     'zip', 'city', 'state_id', 'country_id', 'birthday')}
        values.update({'country_id': int(qcontext.get('country_id'))})
        print('auto')
        if not values:
            raise UserError(_("The form was not properly filled in."))
        if values.get('password') != qcontext.get('confirm_password'):
            raise UserError(_("Passwords do not match; please retype them."))
        supported_lang_codes = [code for code, _ in request.env['res.lang'].get_installed()]
        lang = request.context.get('lang', '').split('_')[0]
        if lang in supported_lang_codes:
            values['lang'] = lang
        print('ready')
        #self._signup_with_values(qcontext.get('token'), values)
        print('why')
        request.env.cr.commit()

    @http.route('/b2b_registration', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):

        qcontext = self.get_auth_signup_qcontext()
        qcontext['industries'] = request.env['res.partner.industry'].sudo().search([])
        qcontext['countries'] = request.env['res.country'].sudo().search([])

        if 'redirect' in kw:
            kw.pop('redirect')

        if 'token' in kw:
            kw.pop('token')

        print(kw)




        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                print('first')
                # Send an account creation confirmation email
                if 'country_id' in kw:
                    kw['country_id']=int(qcontext.get('country_id'))

                part_user=request.env['res.partner'].create(kw)
                #return self.web_login(*args, **kw)
                return request.render('website.homepage', {})
            except UserError as e:
                qcontext['error'] = e.name or e.value
            except (SignupError, AssertionError) as e:
                print(e)
                # if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
                #     qcontext["error"] = _("Another user is already registered using this email address.")
                # else:
                #     _logger.error("%s", e)
                #     qcontext['error'] = _("Could not create a new account.")

        response = request.render('b2b_registration.register', qcontext)
        response.headers['X-Frame-Options'] = 'DENY'
        return response
