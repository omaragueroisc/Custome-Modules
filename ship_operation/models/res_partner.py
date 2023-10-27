# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResPartnerChanges(models.Model):
    _inherit = 'res.partner'

    imo = fields.Char(string="IMO")
    loa = fields.Char(string='LOA')
    grt = fields.Char(string='Grt')
    vessel_type = fields.Char(string='Vessel Type')
    flag = fields.Char(string='FLAG')
    nrt = fields.Char(string='NRT')
    dwt = fields.Char(string='DWT')
    call_sign = fields.Char()
    year_of_build = fields.Integer()
    company_type = fields.Selection(string='Company Type',
                                    selection=[('person', 'Vessel'), ('company', 'Agent')],
                                    compute='_compute_company_type', inverse='_write_company_type', store=True)
