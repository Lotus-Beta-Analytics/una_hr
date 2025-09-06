# -*- coding: utf-8 -*-
{
    'name': 'HR Employee Timeoff Enhancement',
    'version': '17.0.1.0.0',
    'summary': 'Adds confirmation status tracking and dynamic buttons to HR Employee form',
    'description': """
        This module enhances the HR Employee form by adding:
        - A dynamic visual status indicator (Confirmed, Pending, Not Confirmed)
        - Buttons to confirm or unconfirm an employee
        - Auto-update of last confirmation date
    """,
    'category': 'Human Resources',
    'author': 'Lotus Beta Analytics',
    'website': 'https://yourcompany.example.com',
    'depends': ['hr', 'hr_holidays'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/mail_template.xml',
        'views/hr_leave_approval_wizard_view.xml',
        'views/hr_timeoff_views.xml',
        
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
