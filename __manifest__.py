# -*- coding: utf-8 -*-
{
    'name': "sd_hse_import",

    'summary': """
        """,

    'description': """
        
    """,

    'author': "Arash Homayounfar",
    'website': "https://gilaneh.com",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Service Desk/Service Desk',
    'application': True,
    'version': '1.0.6',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website', 'sd_hse'],
    # pip install openpyxl

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'wizard/import_wizard.xml',
    ],
    'assets': {
        # 'website.assets_editor': [
        #     'static/src/**/*',
        # ],

        'web.assets_frontend': [

            'sd_hse_import/static/src/css/style.scss',
            # 'sd_hse_import/static/src/js/website_form_sd_hse.js'
        ],
        'web.assets_backend': [

            'sd_hse_import/static/src/css/style.scss',
            'sd_hse_import/static/src/js/sd_hse_import_sheet_names.js'
        ],
        'web.report_assets_common': [

            'sd_hse_import/static/src/css/report_styles.css',
            # 'sd_hse_import/static/src/js/website_form_sd_hse.js'
        ],

    },

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'license': 'LGPL-3',

}
