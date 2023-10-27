from odoo import models, fields


class ShipReport(models.Model):
    _name = 'ship.report'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'ship Report'

    name = fields.Many2one('ship.info', string='Ship Name')
    date = fields.Datetime(default=fields.datetime.now())
    running_hours = fields.Float(string='Running Hours')
    fuel_consumption = fields.Float(string='Fuel Consumption')
    add_fuel = fields.Float(string='Add Fuel')
