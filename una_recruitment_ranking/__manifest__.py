{
    "name": "Recruitment Applicant Ranking",
    "version": "1.1",
    "category": "Human Resources",
    "summary": "Rank applicants based on job fit criteria with dashboard stats",
    "depends": ["hr_recruitment"],
    "data": [
        "security/group.xml",
        "security/ir.model.access.csv",
        "views/hr_certification_views.xml",
        "views/hr_job_views.xml",
        "views/hr_applicant_views.xml"
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}
