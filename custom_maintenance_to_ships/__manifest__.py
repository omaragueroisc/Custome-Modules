# -*- coding: utf-8 -*-
{
    'name': "Custom Maintenance module To Maintenance ships",

    'summary': """
        Custom  maintenance module for Maintenance ships
        """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Abdullah",
    'website': "http://www.yourcompany.com",

    'category': 'maintenance',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/maintenance_views.xml',
    ],

}
