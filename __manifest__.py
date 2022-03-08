{
    'name': "Realestate",
    'version': '1.3',
    'depends': ['base'],
    'author': "bitVizor Consulting <info@bitvizor.com>",
    'category': 'Sales/CRM',
    'installable': True,
    'application': True,
    'description': """
        Realestate App by IQAAI Marketing
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'data/estate_property_data.xml',
    ],
}
