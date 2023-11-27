# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Content Plan',
    'version': '1.0',
    'summary': 'Custom module for managing social media plans',
    'description': 'Module to create and manage social media plans for clients.',
    'author': 'TecPill - Sayed Mohd Ebrahim',
    'depends': ['base'],  # Add dependencies if needed
    'data': [
        './security/ir.model.access.csv',
        'views/content_plan_views.xml',
        'views/content_plan_menus.xml',
        # Add more data files if needed
    ],
    'installable': True,
    'application': True,
}
