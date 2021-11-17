
odoo.define('website.show_company', function (require) {
'use strict';
console.log('start')
var publicWidget = require('web.public.widget');

publicWidget.registry.ShowCompany = publicWidget.Widget.extend({
    selector: '#is_company',
    events: {
        'click': '_onShowCompany',
    },

    /**
     * @override
     */

 destroy: function () {
        this._super(...arguments);
        $('body').off(".ShowCompany");
    },
    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * @private
     */
     _onShowCompany: function (ev) {
         console.log('begin')
            let company_name = $(ev.currentTarget).next();
            console.log(ev)
            if(ev.currentTarget.checked) {
                $('#div_company_name').removeClass('o_hidden');
                $('#div_vat').removeClass('o_hidden');
                $('#div_fiscal_code').removeClass('o_hidden');
                $('#div_pec').removeClass('o_hidden');
                $('#div_sdi').removeClass('o_hidden');
            } else {
                $('#div_company_name').addClass('o_hidden');
                $('#div_vat').addClass('o_hidden');
                $('#div_fiscal_code').addClass('o_hidden');
                $('#div_pec').addClass('o_hidden');
                $('#div_sdi').addClass('o_hidden');
            }
        },
});

return publicWidget.registry.ShowCompany;

});
