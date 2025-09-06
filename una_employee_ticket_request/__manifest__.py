{
    'name': 'Employee Ticket Request',
    'version': '1.0',
    'category': 'Human Resources',
    'summary': 'Custom module for managing employee travel ticket requests',
    'author': 'Endybest',
    'depends': ['hr', 'mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/reject_ticket_wizard_views.xml',
        'views/ticket_request_views.xml',
        'data/ticket_email_templates.xml',
        
        # 'data/mail_template.xml',
    ],
    'installable': True,
    'application': True,
}
