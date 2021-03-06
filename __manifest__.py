{
    'name': 'B2B registration form',
    'version': '13.0.1.0.0',
    'category': 'Website',
    'summary': 'Auth signup form with extra fields',
    'description': """
        This module add extra fields to auth sign up page
    """,
    'sequence': 1,
    'author': 'Rguibi',
    'website': 'http://rguibi.com',
    'depends': ['website','contacts'],
    'data': [
        #'views/auth_signup_extend_views.xml',
        'views/res_partner_view.xml',
        #'views/reg.xml',
        'views/template_register.xml',
        'views/b2b_request.xml',
    ],
    'images': [
        'static/description/auth_signup_banner.png',
    ],
    'demo': [],
    'price':10,
    'currency': 'EUR',
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3'
}
