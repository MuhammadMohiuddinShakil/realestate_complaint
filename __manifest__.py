# __manifest__.py

{
    'name': 'RealEstate Complaint Management',
    'version': '1.0',
    'summary': 'Complaint management system for RealEstateX',
    'description': 'Module to manage complaints submitted by tenants of RealEstateX',
    'author': 'Muhammad Mohiuddin',
    'category': 'Real Estate',
    'depends': ['base', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/sequence.xml',
        'data/mail_template_data.xml',
        'data/solved_mail_template_data.xml',
        'data/dropped_template_data.xml',
        'views/complaint_form.xml',
        'views/website_complaint_form.xml',
        'views/menu.xml',
        'report/work_order_report.xml',

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
