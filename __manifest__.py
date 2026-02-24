{
    'name': 'Prelium — Partner Notes',
    'version': '19.0.1.0.0',
    'category': 'Sales/CRM',
    'summary': 'Gestion de notes internes sur les partenaires avec priorite, categorie, statut et chatter',
    'author': 'Prelium',
    'license': 'LGPL-3',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/prelium_partner_notes_category_views.xml',
        'views/prelium_partner_notes_note_views.xml',
        'views/res_partner_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
}
