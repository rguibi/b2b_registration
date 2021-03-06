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
        values = {key: qcontext.get(key) for key in ('login', 'name', 'password', 'phone', 'street', 'email'
                                                     ,'company_name','vat','fiscal_code','industry_id','pec','sdi','zip', 'city', 'country_id','b2b_reg')}
        values.update({'country_id': int(qcontext.get('country_id'))})
        print(values)
        if not values:
            raise UserError(_("The form was not properly filled in."))
        if values.get('password') != qcontext.get('conf_password'):
            raise UserError(_("Passwords do not match; please retype them."))
        supported_lang_codes = [code for code, _ in request.env['res.lang'].get_installed()]
        lang = request.context.get('lang', '').split('_')[0]
        if lang in supported_lang_codes:
            values['lang'] = lang

        _logger.error("im here")
        self._signup_with_values(qcontext.get('token'), values)
        _logger.error("im here_________________________________")
        request.env.cr.commit()

    @http.route('/b2b_registration', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()
        qcontext['industries'] = request.env['res.partner.industry'].sudo().search([])
        qcontext['countries'] = request.env['res.country'].sudo().search([])
        _logger.error(qcontext.get('token'))
        # if not qcontext.get('token') and not qcontext.get('signup_enabled'):
        #     raise werkzeug.exceptions.NotFound()
        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                _logger.error("im here2")
                if 'email' in qcontext:
                    qcontext['login'] = qcontext['email']
                qcontext['b2b_reg'] = 1
                self.do_signup(qcontext)
                # Send an account creation confirmation email
                user_sudo = request.env['res.users'].sudo().search([('login', '=', qcontext.get('login'))])
                template = request.env.ref('auth_signup.mail_template_user_signup_account_created',
                                           raise_if_not_found=False)
                _logger.error("im here3")
                if user_sudo and template:
                    template.sudo().with_context(
                        lang=user_sudo.lang,
                        auth_login=werkzeug.url_encode({'auth_login': user_sudo.email}),
                    ).send_mail(user_sudo.id, force_send=True)
                #user_sudo.write({'active': 0})
                _logger.error("im here4")
                return request.render('website.homepage', {})
            except UserError as e:
                qcontext['error'] = e.name or e.value
            except (SignupError, AssertionError) as e:
                if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
                    qcontext["error"] = _("Another user is already registered using this email address.")
                else:
                    _logger.error("%s", e)
                    qcontext['error'] = _("Could not create a new account.")
        response = request.render('b2b_registration.register', qcontext)
        response.headers['X-Frame-Options'] = 'DENY'
        return response