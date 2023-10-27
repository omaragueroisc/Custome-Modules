# -*- coding: utf-8 -*-
{
    'name': "Ship",

    'summary': """
        Ship Repair and manage""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Abdullah/ITOS",
    'website': "http://www.itos.com",
    'category': 'Ship',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/request_maintenance.xml',
        'wizard/report_daily.xml',
        'wizard/print_report_daily.xml',
        'wizard/add_fuel.xml',
        'views/sequence.xml',
        'views/ship_info.xml',
        'views/ship_certificate.xml',
        'views/ship_report.xml',
        'report/report_daily_template.xml',
        'report/report.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
