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
        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()
        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                # Send an account creation confirmation email
                if 'country_id' in kw:
                    kw['country_id']=int(qcontext.get('country_id'))
                if kw['password']!=kw['conf_password']:
                    raise UserError(_("Passwords do not match; please retype them."))
                b2b_part=request.env['res.partner'].create(kw)
                if b2b_part:
                    data = {
                        'name':b2b_part.name,
                        'login': b2b_part.email,
                        'partner_id': b2b_part.id,
                        'password': b2b_part.password,
                        'active':0,
                    }
                    b2b_user=request.env['res.users'].sudo().create(qcontext)
                    #if b2b_user:
                        #b2b_part.write({'password':"",'conf_password':""})
                #return self.web_login(*args, **kw)
                return request.render('website.homepage', {})
            except UserError as e:
                qcontext['error'] = e.name or e.value
            except (SignupError, AssertionError) as e:
                if request.env["res.users"].sudo().search([("login", "=", qcontext.get("email"))]):
                    qcontext["error"] = _("Another user is already registered using this email address.")
                else:
                    _logger.error("%s", e)
                    qcontext['error'] = _("Could not create a new account.")
        response = request.render('b2b_registration.register', qcontext)
        response.headers['X-Frame-Options'] = 'DENY'
        return response
