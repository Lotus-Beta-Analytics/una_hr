# -*- coding: utf-8 -*-
{
    'name': "Employee Onboarding Details",

    'summary': """
        Details of Onboarded Employees""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Daniel",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    

    # any module necessary for this one to work correctly
    'depends': ['hr_skills','base','hr','mail'],


    # always loaded
    'data': [
        'security/user_access.xml',
        'security/ir.model.access.csv',
        'views/onboarding_upload_styles.xml',
        'views/employee_details_views.xml',
        'views/onboarding_upload_wizard.xml',
        'views/hr_employee_public_views.xml',
        'data/res_bank_data.xml',
        'data/onboarding_reminder_templates.xml',
        'data/onboarding_cron.xml',
        
    ],

    'assets': {
        'web.assets_backend': [
            'una_employee_details/static/src/js/onboarding_reminder_popup.js',
        ],
    },

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
