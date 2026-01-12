{
    'name': 'Custom Asset Depreciation Label',
    'version': '1.0',
    'summary': 'Customize depreciation journal entry labels',
    'description': """
        Automatically sets depreciation journal entry label to:
        "BEING DEPRECIATION AT THE MONTH ENDED [MONTH_NAME]"
    """,
    'category': 'Accounting/Accounting',
    'author': 'Daniel Chukwu',
    'website': 'https://www.yourcompany.com',
    'depends': ['base','account','account_asset'],
    'data': [
        # Optional: views if you need to modify any UI
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}