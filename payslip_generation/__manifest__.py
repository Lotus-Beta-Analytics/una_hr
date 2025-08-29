# -*- coding: utf-8 -*-
{
    'name': "Employee Payslip Button",

    'summary': """
        Employee Payslip Generation Button""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Daniel",
    'website': "https://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr','mail'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
