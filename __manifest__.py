# -*- coding: utf-8 -*-
{
    'name': "Employee Payslip",

    'summary': "Employee payslip management and reporting system",

    'description': """
Employee Payslip Module
======================

This module provides comprehensive employee payslip management functionality including:
* Employee payslip creation and management
* Custom payslip reporting
* Payslip data access and security
    """,

    'author': "Ejoor Emmanuel",
    'website': "https://www.linkedin.com/in/ejooremanuel/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resources',
    'version': '1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr_payroll'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}

