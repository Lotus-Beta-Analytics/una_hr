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
    'depends': ['base','hr','mail'],

    # always loaded
    'data': [
        'security/user_access.xml',
        'security/ir.model.access.csv',
        'views/employee_details_views.xml',
        'views/onboarding_upload_wizard.xml',
        'views/hr_employee_public_views.xml',
        'data/prompts.xml',
        'data/crons.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
