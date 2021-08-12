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
    @http.route('/b2b_registration', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):

        qcontext = self.get_auth_signup_qcontext()
        qcontext['industries'] = request.env['res.partner.industry'].sudo().search([])
        qcontext['countries'] = request.env['res.country'].sudo().search([])

        if 'redirect' in kw:
            kw.pop('redirect')
            kw['b2b_reg']=1
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
        response = request.render('b2b_registration.register', qcontext)
        response.headers['X-Frame-Options'] = 'DENY'
        return response
