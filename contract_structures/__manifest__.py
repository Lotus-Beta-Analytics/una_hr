# -*- coding: utf-8 -*-
{
    'name': "UNA Salary Contract Update",

    'summary': """
        Employee Contract Info Update
    """,

    'description': """
        UNA Salary Contract Update
    """,

    'author': "Lotus Beta Analytics",
    'website': "https://www.lotusbetaanalytics.com",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr', 'hr_payroll',],

    # always loaded
    'data': [
        'views/hr_contract_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': False,
}
