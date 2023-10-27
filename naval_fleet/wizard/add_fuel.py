from odoo import models, fields, api
from odoo.exceptions import UserError


class AddFuel(models.TransientModel):
    _name = 'add.fuel.wizard'
    _description = 'Add Fuel wizard'

    name = fields.Many2one('ship.info')
    date = fields.Datetime(default=fields.datetime.now())
    add_fuel = fields.Float(string='Add Fuel')

    def add_fuel_func(self):
        request = self.env['ship.report'].create(
            {'name': self.name.id, 'date': self.date, 'add_fuel': self.add_fuel})
        # tug_name = self.env['ship.info'].browse(self.name.id)
        # print(tug_name)
        # tug_name.update({'fuel_exist_in_tank': (self.add_fuel + tug_name.fuel_exist_in_tank)})

    @api.constrains('add_fuel')
    def check_tank_capacity(self):
        tug_name = self.env['ship.info'].browse(self.name.id)
        if self.add_fuel > tug_name.tank_capacity or self.add_fuel > (
                tug_name.tank_capacity - tug_name.fuel_exist_in_tank):
            raise UserError('Your Enter Value of Add Fuel more than Tank Capacity')
