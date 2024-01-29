# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Content Plan',
    'version': '1.0',
    'summary': 'Custom module for managing social media plans',
    'description': 'Module to create and manage social media plans for clients.',
    'author': 'TecPill - Sayed Mohd Ebrahim',
    'license': 'OPL-1',
    'depends': ['base', 'mail'],  # Add dependencies if needed
    'data': [
        './security/ir.model.access.csv',
        './report/content_plan_templates.xml',
        './report/content_plan_reports.xml',
        'views/content_plan_notes_views.xml',
        'views/content_plan_contents_view.xml',
        'views/content_plan_views.xml',
        'views/content_plan_date_occasions_views.xml',
        'views/content_plan_contents_type_views.xml',
        'views/content_plan_client_list_views.xml',
        'views/content_plan_menus.xml',
        # Add more data files if needed
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
