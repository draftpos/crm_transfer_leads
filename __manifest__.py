# -*- coding: utf-8 -*-
{
    'name': 'CRM Transfer Leads & User Disable',
    'version': '1.0',
    'summary': 'Transfer CRM lead ownership between salespersons, batch reassign leads, and safely disable offboarded users with zero lead loss.',
    'description': """
CRM Leads Transfer Ownership & User Disabling
=============================================
This module provides advanced tools for managing CRM sales representative ownership:
- Interactive Lead Transfer Wizard to reassign leads from a source salesperson to a target salesperson.
- Action to Transfer Leads & immediately Disable / Archive the source user.
- Pre-built Batch Migration runner for company-wide ownership restructurings.
- Dynamic filtering to show only active salespersons who currently have leads.
- Full audit chatter tracking without modifying historical creation dates, notes, or activities.
    """,
    'author': 'DraftPOS / Havano Solutions',
    'website': 'https://draftpos.com',
    'category': 'Sales/CRM',
    'depends': ['crm', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/crm_lead_transfer_wizard_views.xml',
        'views/crm_lead_views.xml',
        'views/res_users_views.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
