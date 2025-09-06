# -*- coding: utf-8 -*-
{
    'name': 'HR Employee Enhancement',
    'version': '17.0.1.0.0',
    'summary': 'Adds confirmation status tracking and dynamic buttons to HR Employee form',
    'description': """
        This module enhances the HR Employee form by adding:
        - A dynamic visual status indicator (Confirmed, Pending, Not Confirmed)
        - Buttons to confirm or unconfirm an employee
        - Auto-update of last confirmation date
    """,
    'category': 'Human Resources',
    'author': 'Your Name or Company',
    'website': 'https://odoo.una.example.com',
    'depends': ['hr','survey'],
    


    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/mail_template_employee_confirmation.xml',
        'views/hr_employee_views.xml',
        'views/hr_employee_next_kin_view.xml',
        'views/department.xml',
        'views/public.xml',
    
       
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
