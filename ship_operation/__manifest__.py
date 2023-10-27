# -*- coding: utf-8 -*-
{
    'name': "Ship Operation",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Abdullah/IOTS",
    'website': "http://www.IOTS.com",
    'category': 'iots',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'naval_fleet', 'custom_maintenance_to_ships', 'hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/ship_operation.xml',
        'views/res_partner.xml',
        'views/ship_history.xml',
        'views/ship_info.xml',
        'views/ship_berth.xml',
        'views/hr_employee.xml',

        'reports/report_view.xml',
        'reports/shipment_report.xml',
        'reports/report_view_op.xml',
        'reports/shipment_report_op.xml',

    ],

}
