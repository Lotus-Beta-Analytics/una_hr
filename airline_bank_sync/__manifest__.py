# -*-  coding: utf-8 -*-
{
    'name': 'Airline Bank Statement Sync',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Sync Bank Statements from API',
    'author': 'Daniel Chukwu',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'data/cron.xml',
    ],
    'installable': True,
    'application': False,
}
