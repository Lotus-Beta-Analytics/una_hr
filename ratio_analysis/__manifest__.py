# -*- coding: utf-8 -*-
{
    'name': "Ratio Analysis Report",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account','account_reports'],

    # always loaded
    'data': [
        'views/views.xml',
        'views/assets.xml',
        # 'views/report_ratio_qweb.xml',
        # 'views/ratio_analysis_report.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'ratio_analysis/static/src/js/report_ratio_patch.js',
        ],
    },

    'installable': True,
    'application': False,
    
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}

