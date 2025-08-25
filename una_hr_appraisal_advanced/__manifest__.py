{
    'name': 'Advanced Appraisal with Strategic Objectives and Competencies',
    'version': '1.0',
    'summary': 'Enhanced appraisal with strategic objectives, KPIs, weights, ratings, comments, and weighted scoring',
    'category': 'Human Resources',
    'author': 'endybest',
    'depends': ['hr_appraisal', 'website_slides', 'website'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/appraisal_views.xml',
        'views/appraisal_config_views.xml',
        'views/appraisal_bulk_objective_wizard.xml',
        'data/hr_appraisal_email_template.xml',
        
        # 'views/consultations.xml',
    ],
    'installable': True,
    'application': False,
}
