from odoo import models, fields, api
from odoo.exceptions import UserError


class RequestMaintenance(models.TransientModel):
    _name = 'report.daily.wizard'
    _description = 'Report Daily wizard'

    name = fields.Many2one('ship.info')
    date = fields.Datetime(default=fields.datetime.now())
    running_hours = fields.Float(string='Running Hours')
    fuel_consumption = fields.Float(string='Fuel Consumption')

    def create_report_daily(self):
        request = self.env['ship.report'].create(
            {'name': self.name.id, 'date': self.date, 'running_hours': self.running_hours,
             'fuel_consumption': self.fuel_consumption})

    @api.constrains('fuel_consumption')
    def check_tank_capacity(self):
        tug_name = self.env['ship.info'].browse(self.name.id)
        if self.fuel_consumption > tug_name.tank_capacity or self.fuel_consumption > tug_name.fuel_exist_in_tank:
            raise UserError(
                'Your Enter Value of Fuel consumption more than Tank Capacity or more than fuel exist in Tank')
