{
    'name': 'HR Job Application Extension',
    'version': '1.0',
    'depends': ['website_hr_recruitment'],
    'author': 'Your Name',
    'category': 'Recruitment',
    'summary': 'Extends job application form with cover letter upload, certification, and skills.',

    'depends': [
        'website',
        'web',                    # ✅ This is essential
        'website_hr_recruitment',
    ],

    
    'data': [
        'security/ir.model.access.csv',
        'security/groups.xml',
        'views/website_hr_recruitment_apply_inherit.xml',
        
    
    ],
    'installable': True,
    'application': False,
}
